"""Generate src/data/foods.json.

Usage: python3 scripts/build_foods.py [path/to/sr28] [--review]

Sources, in order of preference for each nutrient of each food:
  1. USDA Foundation Foods (newest lab data), if scripts/update_from_fdc.py has
     matched the food and fetched values (scripts/foundation_map.json + foundation_cache.json)
  2. USDA SR Legacy / SR28 (bundled in data-sources/sr28; final release, never changes)
  3. NIH Office of Dietary Supplements tables (biotin, iodine, omega-3 only)
"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from foodlist import FOODS, SERVINGS, ODS

ROOT = os.path.join(os.path.dirname(__file__), '..')
_args = [a for a in sys.argv[1:] if not a.startswith('--')]
SR = _args[0] if _args else os.path.join(ROOT, 'data-sources', 'sr28')
MAP_FILE = os.path.join(os.path.dirname(__file__), 'foundation_map.json')
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'foundation_cache.json')
foundation_map, foundation = {}, {'foods': {}}
if os.path.exists(MAP_FILE) and os.path.exists(CACHE_FILE):
    foundation_map = json.load(open(MAP_FILE))
    foundation = json.load(open(CACHE_FILE))

# ABBREV.txt column index for each nutrient (SR28 documentation, Table 6).
COL = {
    'protein': 4, 'carbs': 7, 'fiber': 8,
    'calcium': 10, 'iron': 11, 'magnesium': 12, 'phosphorus': 13, 'potassium': 14,
    'zinc': 16, 'copper': 17, 'manganese': 18, 'selenium': 19,
    'vitC': 20, 'b1': 21, 'b2': 22, 'b3': 23, 'b5': 24, 'b6': 25,
    'b9': 29,      # folate, DFE
    'choline': 30, 'b12': 31,
    'vitA': 33,    # RAE
    'vitE': 40,    # alpha-tocopherol
    'vitD': 41,    # µg
    'vitK': 43,
}
GMWT1, GMDESC1 = 48, 49

def rows(name):
    with open(os.path.join(SR, name), encoding='latin-1') as fh:
        for line in fh:
            yield [x.strip('~') for x in line.rstrip('\r\n').split('^')]

abbrev = {r[0]: r for r in rows('ABBREV.txt')}
des = {r[0]: r for r in rows('FOOD_DES.txt')}
nutrients = json.load(open(os.path.join(ROOT, 'src/data/nutrients.json')))['nutrients']
DV = {n['id']: n['dv'] for n in nutrients}

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def rnd(x):
    if x == 0: return 0
    if x >= 100: return round(x)
    if x >= 10: return round(x, 1)
    if x >= 1: return round(x, 2)
    return round(x, 3)

out, seen, problems = [], set(), []
for ndb, name, form, cat, skey, allergens, tip in FOODS:
    if ndb not in abbrev:
        problems.append(f'missing NDB {ndb} {name}')
        continue
    a = abbrev[ndb]
    grams, label = SERVINGS[skey]
    if grams is None:  # sprouts: 1/4 of USDA's 1-cup weight
        assert a[GMDESC1].startswith('1 cup'), (ndb, a[GMDESC1])
        grams = round(float(a[GMWT1]) / 4)
        label = f'¼ cup ({grams} g)'
    per100, src = {}, {}
    for nid, col in COL.items():
        v = a[col]
        if v != '':            # empty = not measured by USDA; 0 = measured zero
            per100[nid] = rnd(float(v))
    for nid, table in ODS.items():
        if ndb in table and nid not in per100:
            amt, g = table[ndb]
            per100[nid] = rnd(amt / g * 100)
            src[nid] = 'ods'
    # Newest USDA lab values replace older ones wherever Foundation Foods reports them.
    fnd = None
    m = foundation_map.get(slug(name), {})
    if m.get('status') in ('auto', 'confirmed') and str(m.get('fdcId')) in foundation['foods']:
        rec = foundation['foods'][str(m['fdcId'])]
        for nid, v in rec['per100'].items():
            if nid in COL or nid in ODS:
                per100[nid] = rnd(v)
                src[nid] = 'fnd'
        fnd = {'fdcId': m['fdcId'], 'name': m.get('foundation', ''), 'published': rec.get('published', '')}
    pct = {nid: v * grams / 100 / DV[nid] * 100 for nid, v in per100.items()}
    high = [n for n, p in pct.items() if p >= 20]
    good = [n for n, p in pct.items() if 10 <= p < 20]
    fid = slug(name)
    assert fid not in seen, fid
    seen.add(fid)
    item = {
        'id': fid, 'name': name, 'form': form, 'category': cat, 'allergens': allergens,
        'usda': ndb, 'usdaName': des[ndb][2],
        'serving': {'g': grams, 'label': label},
        'per100': per100, 'high': high, 'good': good,
    }
    if src: item['src'] = src
    if fnd: item['foundation'] = fnd
    if tip: item['tip'] = tip
    out.append(item)

categories = {
    'vegetable': 'Vegetable', 'herb': 'Herb or flavouring', 'mushroom': 'Mushroom', 'seaweed': 'Seaweed',
    'fruit': 'Fruit', 'nut': 'Nut', 'seed': 'Seed', 'legume': 'Bean or legume', 'grain': 'Grain',
    'dairy': 'Dairy', 'egg': 'Egg', 'poultry': 'Poultry', 'meat': 'Meat', 'fish': 'Fish', 'shellfish': 'Shellfish',
}
doc = {
    'source': {
        'main': 'USDA National Nutrient Database for Standard Reference, Release 28 (SR Legacy in FoodData Central). Values per 100 g of edible portion.',
        'ods': 'Biotin, iodine and omega-3 values from NIH Office of Dietary Supplements fact sheets (Table 2 in each), converted to per 100 g. Only foods listed there have these values.',
        'fnd': 'Where marked, values come from USDA Foundation Foods, which USDA updates every April and October.',
        'foundationFetched': foundation.get('fetchedAt'),
        'foundationRelease': foundation.get('release'),
        'levels': "Rich source: one serving gives 20% or more of the FDA Daily Value. Good source: 10-19%. Servings are FDA reference amounts (21 CFR 101.12).",
    },
    'categories': categories,
    'foods': out,
}
json.dump(doc, open(os.path.join(ROOT, 'src/data/foods.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print(f'{len(out)} foods written' + (f", {sum(1 for f in out if 'foundation' in f)} with Foundation Foods values" if foundation['foods'] else ''))
for p in problems: print('PROBLEM', p)
# For manual review: our name vs USDA's description
if '--review' in sys.argv:
    for f in out: print(f"{f['usda']}  {f['name']:<32} | {f['usdaName']}")
