"""Pull the newest USDA Foundation Foods values into Nutrayo.

USDA's SR Legacy dataset (the base data) is final and never changes. USDA's
Foundation Foods dataset is re-released every April and October with new lab
analyses. This script matches Nutrayo's foods to Foundation Foods and, wherever
Foundation Foods reports a nutrient, uses that newer value instead.

Usage (from the project folder):

    python3 scripts/update_from_fdc.py --api-key YOUR_KEY

Get a free key at https://fdc.nal.usda.gov/api-key-signup (DEMO_KEY also works,
but is limited to 30 requests an hour; a full run needs about 20).

Offline alternative: download "Foundation Foods" as CSV from
https://fdc.nal.usda.gov/download-datasets and pass the zip (or unzipped folder):

    python3 scripts/update_from_fdc.py --csv FoodData_Central_foundation_food_csv_2026-10-29.zip

Steps (all run by default, or pick one with --step):
  match   match each Nutrayo food to a Foundation food -> scripts/foundation_map.json
  review  go through uncertain matches one by one (not part of "all"; asks questions)
  fetch   download nutrient values for matched foods   -> scripts/foundation_cache.json
  build   regenerate src/data/foods.json (runs scripts/build_foods.py)

Only Python 3.9+ standard library is needed.
"""
import argparse, csv, io, json, os, re, subprocess, sys, time, urllib.error, urllib.request, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from foodlist import FOODS  # noqa: E402


def read_json(path):
    """Read JSON as UTF-8. Files saved by older versions on Windows used the
    Windows encoding, so fall back to it; the next save rewrites them as UTF-8."""
    raw = open(path, 'rb').read()
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        text = raw.decode('cp1252', errors='replace')
    return json.loads(text)


def write_json(path, data, **kw):
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(data, fh, ensure_ascii=False, **kw)


def clean(text):
    """Tidy USDA names: collapse odd spacing such as non-breaking spaces."""
    return ' '.join(str(text).split())


def iso_date(text):
    """USDA dates come as YYYY-MM-DD or M/D/YYYY; return YYYY-MM-DD so they sort correctly."""
    t = str(text or '').strip()
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', t)
    if m:
        return f'{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}'
    m = re.match(r'^(\d{4}-\d{2}-\d{2})', t)
    return m.group(1) if m else t

MAP_FILE = os.path.join(HERE, 'foundation_map.json')
CACHE_FILE = os.path.join(HERE, 'foundation_cache.json')
SR_DIR = os.path.join(ROOT, 'data-sources', 'sr28')
PY = 'python' if os.name == 'nt' else 'python3'
BASE_URL = os.environ.get('FDC_BASE_URL', 'https://api.nal.usda.gov/fdc/v1')

# ---------------------------------------------------------------------------
# Nutrients: how to read each Nutrayo nutrient from a Foundation Foods record.
# Keys are FDC nutrient numbers (stable across API and CSV). Units are what
# Nutrayo stores; values in other units are converted.
# ---------------------------------------------------------------------------
UNIT = {'protein': 'g', 'carbs': 'g', 'fiber': 'g', 'omega3': 'g',
        'calcium': 'mg', 'iron': 'mg', 'magnesium': 'mg', 'phosphorus': 'mg', 'potassium': 'mg',
        'zinc': 'mg', 'copper': 'mg', 'manganese': 'mg', 'selenium': 'ug', 'iodine': 'ug',
        'vitC': 'mg', 'b1': 'mg', 'b2': 'mg', 'b3': 'mg', 'b5': 'mg', 'b6': 'mg', 'b7': 'ug',
        'b9': 'ug', 'choline': 'mg', 'b12': 'ug', 'vitA': 'ug', 'vitE': 'mg', 'vitD': 'ug', 'vitK': 'ug'}
DIRECT = {'protein': '203', 'calcium': '301', 'iron': '303', 'magnesium': '304', 'phosphorus': '305',
          'potassium': '306', 'zinc': '309', 'copper': '312', 'iodine': '314', 'manganese': '315',
          'selenium': '317', 'vitE': '323', 'vitC': '401', 'b1': '404', 'b2': '405', 'b3': '406',
          'b5': '410', 'b6': '415', 'b7': '416', 'b12': '418', 'choline': '421', 'vitK': '430'}
TO_BASE = {'g': 1.0, 'mg': 1e-3, 'ug': 1e-6, 'µg': 1e-6, 'mcg': 1e-6}


def convert(amount, unit_from, unit_to):
    f, t = (unit_from or '').strip().lower(), unit_to.lower()
    if f in ('', t):
        return amount
    if f in TO_BASE and t in TO_BASE:
        return amount * TO_BASE[f] / TO_BASE[t]
    raise ValueError(f'cannot convert {unit_from} to {unit_to}')


def derive(raw):
    """raw: {nutrient_number: (amount, unit, name)} for one food, per 100 g.
    Returns {nutrayo_id: value} with only the nutrients Foundation reports."""
    def get(num, unit):
        if num in raw and raw[num][0] is not None:
            return convert(raw[num][0], raw[num][1], unit)
        return None

    def by_name(pattern, unit):
        for amt, u, name in raw.values():
            if amt is not None and name and re.search(pattern, name, re.I):
                return convert(amt, u, unit)
        return None

    out = {}
    for nid, num in DIRECT.items():
        v = get(num, UNIT[nid])
        if v is not None:
            out[nid] = v
    # Carbohydrate: by difference (205), else by summation (205.2)
    v = get('205', 'g')
    out_c = v if v is not None else get('205.2', 'g')
    if out_c is not None:
        out['carbs'] = out_c
    # Fiber: total dietary (291), else the AOAC 2011.25 total
    v = get('291', 'g')
    if v is None:
        v = by_name(r'^(total dietary fiber|fiber, total dietary)', 'g')
    if v is not None:
        out['fiber'] = v
    # Folate as DFE (435); else food folate + 1.7 x folic acid; else total folate
    v = get('435', 'ug')
    if v is None and get('432', 'ug') is not None:
        v = get('432', 'ug') + 1.7 * (get('431', 'ug') or 0)
    if v is None:
        v = get('417', 'ug')
    if v is not None:
        out['b9'] = v
    # Vitamin A as RAE (320); else retinol + carotenoids (IOM 2001 factors)
    v = get('320', 'ug')
    if v is None:
        parts = [get('319', 'ug'), get('321', 'ug'), get('322', 'ug'), get('334', 'ug')]
        if any(p is not None for p in parts):
            r, b, a, c = (p or 0 for p in parts)
            v = r + b / 12 + a / 24 + c / 24
    if v is not None:
        out['vitA'] = v
    # Vitamin D total (328); else D2 + D3
    v = get('328', 'ug')
    if v is None and (get('325', 'ug') is not None or get('326', 'ug') is not None):
        v = (get('325', 'ug') or 0) + (get('326', 'ug') or 0)
    if v is not None:
        out['vitD'] = v
    # Omega-3: ALA (851, else 18:3 total 619) + EPA (629) + DHA (621), as in the NIH tables
    ala = get('851', 'g')
    if ala is None:
        ala = get('619', 'g')
    parts = [ala, get('629', 'g'), get('621', 'g')]
    if any(p is not None for p in parts):
        out['omega3'] = sum(p or 0 for p in parts)
    return out


# ---------------------------------------------------------------------------
# Data access: FoodData Central API, or a downloaded CSV release
# ---------------------------------------------------------------------------
class Api:
    def __init__(self, key):
        self.key = key
        self.calls = 0

    def request(self, path, body, allow_400=False):
        url = f'{BASE_URL}{path}?api_key={self.key}'
        data = json.dumps(body).encode()
        for attempt in range(4):
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            try:
                self.calls += 1
                with urllib.request.urlopen(req, timeout=60) as r:
                    return json.loads(r.read().decode())
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    sys.exit('USDA says the rate limit is used up (HTTP 429). With DEMO_KEY that is 30 requests an hour; '
                             'get a free key at https://fdc.nal.usda.gov/api-key-signup and pass it with --api-key.')
                if e.code == 400 and allow_400:
                    return None
                if e.code in (401, 403):
                    sys.exit(f'USDA rejected the API key (HTTP {e.code}). Check the key passed with --api-key.')
                if e.code >= 500 and attempt < 3:
                    time.sleep(2 ** attempt)
                    continue
                sys.exit(f'USDA API error HTTP {e.code} on {path}: {e.read()[:300]!r}')
            except urllib.error.URLError as e:
                if attempt < 3:
                    time.sleep(2 ** attempt)
                    continue
                sys.exit(f'Could not reach {BASE_URL}: {e.reason}')

    def foundation_list(self):
        foods, page, size = [], 1, 200
        while True:
            batch = self.request('/foods/list', {'dataType': ['Foundation'], 'pageSize': size, 'pageNumber': page}, allow_400=True)
            if batch is None:  # page size not accepted: start again with smaller pages
                if size == 50:
                    sys.exit('USDA rejected the food list request (HTTP 400).')
                foods, page, size = [], 1, 50
                continue
            if not batch:
                break
            foods += [{'fdcId': f['fdcId'], 'description': clean(f['description']),
                       'published': iso_date(f.get('publicationDate') or f.get('publishedDate'))}
                      for f in batch if f.get('dataType', 'Foundation') == 'Foundation']
            page += 1  # keep going until USDA returns an empty page (it may cap the page size)
            if page > 500:
                sys.exit('Stopped after 500 pages of results; something is wrong with the food list.')
        return foods

    def nutrients(self, fdc_ids):
        """{fdcId: {number: (amount, unit, name)}} using full records (abridged ones have no nutrients)."""
        out = {}
        ids = list(fdc_ids)
        for i in range(0, len(ids), 20):
            for food in self.request('/foods', {'fdcIds': ids[i:i + 20]}) or []:
                out[food['fdcId']] = {'published': iso_date(food.get('publicationDate')),
                                      'raw': normalise_nutrients(food.get('foodNutrients') or [])}
        return out


def normalise_nutrients(items):
    """Accept every nutrient shape FDC returns (nested 'nutrient', flat 'nutrientNumber', abridged 'number')."""
    raw = {}
    for n in items:
        nested = n.get('nutrient') or {}
        number = nested.get('number') or n.get('nutrientNumber') or n.get('number')
        amount = n.get('amount', n.get('value'))
        unit = nested.get('unitName') or n.get('unitName') or ''
        name = nested.get('name') or n.get('nutrientName') or n.get('name') or ''
        if number is None or amount is None:
            continue
        raw[clean_number(number)] = (float(amount), unit, name)
    return raw


def clean_number(num):
    s = str(num).strip()
    return s[:-2] if s.endswith('.0') else s


class Csv:
    """Reads a FoodData Central 'Foundation Foods' CSV download (zip or folder)."""

    def __init__(self, path):
        self.path = path
        self.zip = zipfile.ZipFile(path) if path.endswith('.zip') else None
        names = [os.path.basename(path.rstrip('/'))] + (self.zip.namelist()[:5] if self.zip else [])
        found = [m.group(1) for n in names for m in [re.search(r'(\d{4}-\d{2}-\d{2})', n)] if m]
        self.release_date = found[0] if found else None

    def open(self, name):
        if self.zip:
            matches = [n for n in self.zip.namelist() if n.endswith('/' + name) or n == name]
            if not matches:
                sys.exit(f'{name} not found in {self.path}. Is this the Foundation Foods CSV download?')
            return io.TextIOWrapper(self.zip.open(matches[0]), encoding='utf-8-sig')
        for dirpath, _, files in os.walk(self.path):
            if name in files:
                return open(os.path.join(dirpath, name), encoding='utf-8-sig')
        sys.exit(f'{name} not found under {self.path}. Is this the Foundation Foods CSV download?')

    def rows(self, name, needed):
        reader = csv.DictReader(self.open(name))
        missing = [c for c in needed if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f'{name} is missing columns {missing}. USDA may have changed the file format; columns found: {reader.fieldnames}')
        return reader

    def foundation_list(self):
        if not hasattr(self, '_foods'):
            self._foods = [{'fdcId': int(r['fdc_id']), 'description': clean(r['description']), 'published': iso_date(r.get('publication_date'))}
                           for r in self.rows('food.csv', ['fdc_id', 'data_type', 'description'])
                           if r['data_type'] == 'foundation_food']
        return self._foods

    def nutrients(self, fdc_ids):
        wanted = set(fdc_ids)
        meta = {r['id']: (clean_number(r['nutrient_nbr']), r['unit_name'], r['name'])
                for r in self.rows('nutrient.csv', ['id', 'name', 'unit_name', 'nutrient_nbr'])}
        published = {f['fdcId']: f['published'] for f in self.foundation_list()}
        out = {i: {'published': published.get(i, ''), 'raw': {}} for i in wanted}
        for r in self.rows('food_nutrient.csv', ['fdc_id', 'nutrient_id', 'amount']):
            fid = int(r['fdc_id'])
            if fid in wanted and r['amount'] not in ('', None) and r['nutrient_id'] in meta:
                num, unit, name = meta[r['nutrient_id']]
                out[fid]['raw'][num] = (float(r['amount']), unit, name)
        return out


# ---------------------------------------------------------------------------
# Matching Nutrayo foods to Foundation foods
# ---------------------------------------------------------------------------
STATE_WORDS = {'raw', 'cooked', 'boiled', 'roasted', 'baked', 'broiled', 'braised', 'simmered', 'grilled',
               'fried', 'steamed', 'canned', 'dried', 'dry', 'frozen', 'smoked', 'pan-broiled', 'heat'}
STOP = {'and', 'or', 'with', 'without', 'of', 'the', 'in', 'all', 'types', 'type', 'includes', 'salt',
        'added', 'fresh', 'regular', 'mature', 'seeds', 'whole', 'solids', 'drained', 'separable',
        'only', 'meat', 'lean', 'commercial', 'varieties', 'species', 'mixed', 'nfs', 'not', 'specified',
        'broilers', 'fryers', 'fluid', 'to', 'a', 'as', 'for', 'on'}
# Extra words a Foundation name may carry without describing a different food.
BENIGN = {'mature', 'halves', 'button', 'boneless', 'skinless', 'grade', 'large', 'peeled', 'whole',
          'organic', 'conventional', 'fresh', 'pieces', 'florets', 'leaves', 'stalks', 'wild', 'caught', 'farm', 'raised'}


def _norm(w):
    return w.rstrip('s') if len(w) > 3 else w


def tokens(desc):
    d = desc.lower().replace('dry heat', '').replace('moist heat', '')  # cooking methods, not "dried"
    return {_norm(w) for w in re.findall(r"[a-z][a-z\-]*", d)}


STOP = {_norm(w) for w in STOP}
STATE_WORDS = {_norm(w) for w in STATE_WORDS}
BENIGN = {_norm(w) for w in BENIGN}


def confident(ours, theirs):
    """Same state, every word of ours present in theirs, and theirs adds only harmless words."""
    if state(ours) != state(theirs) or not same_food(ours, theirs):
        return False
    a, b = tokens(ours) - STOP - STATE_WORDS, tokens(theirs) - STOP - STATE_WORDS
    return bool(a) and a <= b and (b - a) <= BENIGN


def state(desc):
    t = tokens(desc)
    s = {w for w in t if w in STATE_WORDS}
    if s & {'boiled', 'roasted', 'baked', 'broiled', 'braised', 'simmered', 'grilled', 'steamed', 'pan-broiled'}:
        s.add('cooked')
    s.discard('heat')
    return frozenset(s) if s else frozenset({'raw'})  # USDA omits "raw" on some raw items


def head(desc):
    return desc.lower().split(',')[0].strip().rstrip('s')


def same_food(ours, theirs):
    """The main food name (text before the first comma) must match: pumpkin is not pumpkin seeds."""
    return head(ours) == head(theirs)


def score(ours, theirs):
    if state(ours) != state(theirs):
        return 0.0
    a, b = tokens(ours) - STOP - STATE_WORDS, tokens(theirs) - STOP - STATE_WORDS
    if not a or not b:
        return 0.0
    s = len(a & b) / len(a | b)
    if head(ours) == head(theirs):
        s += 0.25
    return min(s, 1.0)


def step_match(source, sr_names):
    foundation = source.foundation_list()
    if not foundation:
        sys.exit('No Foundation foods were returned. Nothing to match.')
    old = read_json(MAP_FILE) if os.path.exists(MAP_FILE) else {}
    new = {}
    for e in old.values():  # tidy names saved by earlier runs
        if e.get('foundation'):
            e['foundation'] = clean(e['foundation'])
        for c in e.get('candidates', []):
            c['description'] = clean(c['description'])
    for ndb, name, *_ in FOODS:
        fid = slug(name)
        prev = old.get(fid, {})
        if prev.get('status') in ('confirmed', 'rejected'):
            new[fid] = prev  # your decisions are kept across runs
            continue
        ours = sr_names[ndb]
        ranked = sorted(((score(ours, f['description']), f) for f in foundation), key=lambda x: -x[0])
        a = tokens(ours) - STOP - STATE_WORDS
        close = lambda f: len(a & (tokens(f['description']) - STOP - STATE_WORDS)) / max(len(a), 1) >= 0.75
        ranked = [(s, f) for s, f in ranked if s > 0 and close(f) and same_food(ours, f['description'])][:3]
        entry = {'name': name, 'srLegacy': ours,
                 'candidates': [{'fdcId': f['fdcId'], 'description': f['description'], 'score': round(s, 2)} for s, f in ranked]}
        sure = [f for s, f in ranked if confident(ours, f['description'])]
        if len(sure) == 1:
            entry.update(status='auto', fdcId=sure[0]['fdcId'], foundation=sure[0]['description'])
        elif ranked:
            entry['status'] = 'review'
        else:
            entry['status'] = 'none'
        new[fid] = entry
    # A Foundation food matched automatically to two of our foods is ambiguous: send both to review.
    seen = {}
    for fid, e in new.items():
        if e.get('status') == 'auto':
            seen.setdefault(e['fdcId'], []).append(fid)
    for fids in seen.values():
        if len(fids) > 1:
            for fid in fids:
                new[fid]['status'] = 'review'
                new[fid].pop('fdcId'); new[fid].pop('foundation')
    auto = sum(1 for e in new.values() if e.get('status') == 'auto')
    review = [fid for fid, e in new.items() if e.get('status') == 'review']
    write_json(MAP_FILE, new, indent=1)
    kept = sum(1 for e in new.values() if e.get('status') == 'confirmed')
    print(f'match: {len(foundation)} Foundation foods; {auto} matched automatically, {kept} confirmed earlier, '
          f'{len(review)} need a look, {sum(1 for e in new.values() if e["status"] == "none")} have no Foundation match.')
    if review:
        print(f'  To go through them one by one, run:  {PY} scripts/update_from_fdc.py --step review')


def step_fetch(source):
    if not os.path.exists(MAP_FILE):
        sys.exit('Run the match step first.')
    mapping = read_json(MAP_FILE)
    use = {e['fdcId'] for e in mapping.values() if e.get('status') in ('auto', 'confirmed') and e.get('fdcId')}
    data = source.nutrients(use)
    for fid, e in mapping.items():
        if e.get('status') == 'confirmed' and e.get('foundation') and state(e['srLegacy']) != state(e['foundation']):
            print(f'  check: "{e["srLegacy"]}" is {"/".join(sorted(state(e["srLegacy"])))}, but the Foundation food you confirmed, '
                  f'"{e["foundation"]}", is {"/".join(sorted(state(e["foundation"])))}. Nutrient amounts differ a lot between raw, dry and cooked.')
    cache = {'fetchedAt': time.strftime('%Y-%m-%d'), 'release': None, 'foods': {}}
    empty = 0
    for fdc_id in sorted(use):
        rec = data.get(fdc_id) or data.get(str(fdc_id))
        values = derive(rec['raw']) if rec else {}
        if not values:
            empty += 1
            continue
        cache['foods'][str(fdc_id)] = {'published': rec.get('published', ''), 'per100': values}
    dates = sorted(iso_date(v['published']) for v in cache['foods'].values() if v.get('published'))
    cache['release'] = getattr(source, 'release_date', None) or (dates[-1] if dates else None)
    write_json(CACHE_FILE, cache, indent=1)
    print(f'fetch: nutrient values for {len(cache["foods"])} Foundation foods'
          + (f' ({empty} returned no usable nutrients and were skipped)' if empty else '') + '.')


def step_review():
    if not os.path.exists(MAP_FILE):
        sys.exit('Run the updater first so there are matches to review.')
    mapping = read_json(MAP_FILE)
    todo = [fid for fid, e in mapping.items() if e.get('status') == 'review' and e.get('candidates')]
    if not todo:
        print('Nothing to review.')
        return
    print(f'{len(todo)} foods to review. For each, type a number to use that Foundation food,')
    print('n if none of them is the same food, Enter to decide later, or q to stop.\n')
    done = 0
    for i, fid in enumerate(todo, 1):
        e = mapping[fid]
        print(f'[{i}/{len(todo)}] {e["name"]}  (USDA SR Legacy: {e["srLegacy"]})')
        for k, c in enumerate(e['candidates'], 1):
            print(f'   {k}. {c["description"]}')
        while True:
            ans = input('   Use which? ').strip().lower()
            if ans in ('', 'q', 'n') or (ans.isdigit() and 1 <= int(ans) <= len(e['candidates'])):
                break
            print(f'   Type 1-{len(e["candidates"])}, n, Enter or q.')
        if ans == 'q':
            break
        if ans == 'n':
            e['status'] = 'rejected'
            done += 1
        elif ans:
            c = e['candidates'][int(ans) - 1]
            e.update(status='confirmed', fdcId=c['fdcId'], foundation=c['description'])
            done += 1
        write_json(MAP_FILE, mapping, indent=1)  # saved after every answer
        print()
    print(f'Saved {done} decisions. Run the updater again to fetch values for confirmed foods:')
    print(f'  {PY} scripts/update_from_fdc.py --api-key YOUR_KEY')


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def sr_descriptions():
    names = {}
    with open(os.path.join(SR_DIR, 'FOOD_DES.txt'), encoding='latin-1') as fh:
        for line in fh:
            parts = [x.strip('~') for x in line.rstrip('\r\n').split('^')]
            names[parts[0]] = parts[2]
    return names


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group()
    src.add_argument('--api-key', default=os.environ.get('FDC_API_KEY'), help='FoodData Central API key (or set FDC_API_KEY)')
    src.add_argument('--csv', help='Foundation Foods CSV download (.zip or folder)')
    ap.add_argument('--step', choices=['match', 'review', 'fetch', 'build', 'all'], default='all')
    args = ap.parse_args()

    if args.step == 'review':
        step_review()
        return

    if args.step in ('match', 'fetch', 'all'):
        if args.csv:
            source = Csv(args.csv)
        else:
            key = args.api_key or 'DEMO_KEY'
            if key == 'DEMO_KEY':
                print('Using DEMO_KEY (30 requests an hour). A free personal key is at https://fdc.nal.usda.gov/api-key-signup')
            source = Api(key)
        if args.step in ('match', 'all'):
            step_match(source, sr_descriptions())
        if args.step in ('fetch', 'all'):
            step_fetch(source)
        if isinstance(source, Api):
            print(f'({source.calls} API requests)')
    if args.step in ('build', 'all'):
        subprocess.run([sys.executable, os.path.join(HERE, 'build_foods.py')], check=True)


if __name__ == '__main__':
    main()
