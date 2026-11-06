# Nutrayo

Nutrayo is a periodic table of nutrients. Each tile is a nutrient; select one to see which raw foods are rich in it, or search a food to light up every nutrient it provides. Diet and allergy filters apply across the whole site, and you can like or hide any food.

It is a static website built with [Vite](https://vite.dev) and plain JavaScript. There is no server or database: food data ships as JSON, and your likes, hidden foods and filters are saved in your browser.

## Running it

Requires [Node.js](https://nodejs.org) 20.19+ or 22.12+.

```bash
npm install      # first time only
npm run dev      # http://localhost:5173
npm run build    # builds the site into dist/
npm run preview  # serves dist/ at http://localhost:4173
```

Pushing to `main` on GitHub builds and publishes the site to GitHub Pages through `.github/workflows/deploy.yml` (repository Settings > Pages > Source: GitHub Actions).

## Pages

| Page           | File            | What it shows                                                                                                                                                         |
| -------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Table          | `index.html`    | The periodic table of 28 nutrients. Select a tile for its foods, ranked by % Daily Value per serving. Search a food to see what it provides, or browse foods by type. |
| My foods       | `my-foods.html` | What your liked foods cover: food types you haven't liked anything from yet, nutrients covered and missing, and foods to fill each gap.                               |
| Examples       | `examples.html` | Ingredient combinations and the nutrients each one covers.                                                                                                            |
| Why we need it | `why.html`      | What each nutrient does, what happens without enough, and where the data comes from.                                                                                  |
| Contact        | `contact.html`  | Developer details and an email link for feedback, questions and collaborations.                                                                                       |

Shared across pages: the diet and allergy bar (Vegetarian, Vegan, Lactose, Gluten and others), the **Saved** drawer listing liked and hidden foods with **Clear all** and **Undo**, and a footer with data sources.

## Project files

```
index.html, my-foods.html, examples.html, why.html, contact.html
vite.config.js              build settings; writes the header, filter bar, footer and contact
                            details into each page at build time so they load without a flash
package.json                dependencies (Vite) and npm scripts
.github/workflows/deploy.yml  builds and publishes to GitHub Pages on every push to main

src/
  config.js                 contact details (name, email, LinkedIn, website) used across the site
  styles.css                all styles: colour tokens, light and dark mode, layouts for every screen size
  data/
    nutrients.json          the 28 nutrients: symbol, table position, unit, Daily Value, role, shortage signs
    foods.json              284 foods with nutrient amounts per 100 g (generated; see Data below)
    examples.json           the ingredient combinations on the Examples page
  lib/
    data.js                 loads and indexes the data; % Daily Value and amount helpers
    filters.js              diet and allergy rules
    coverage.js             which nutrients a set of foods covers and which are missing
    store.js                filters, liked and hidden foods; saves through a backend
    backends/local.js       saves to this browser (localStorage)
    backends/supabase.example.js  unused template for saving to a Supabase account
  components/
    markup.js               header, navigation, filter bar, footer and contact markup
    shell.js                mounts the header, filter bar and Saved drawer on each page
    ui.js                   food rows, like and hide buttons, nutrient symbols
  pages/
    table.js, myfoods.js, examples.js, why.js, contact.js   one script per page

scripts/
  foodlist.py               the food list: USDA record numbers, names, serving sizes, allergens, tips
  build_foods.py            generates src/data/foods.json from the sources below
  update_from_fdc.py        fetches the newest USDA Foundation Foods values
  foundation_map.json       which Nutrayo foods match which Foundation foods (created by the updater)
  foundation_cache.json     the Foundation values last fetched (created by the updater)

data-sources/sr28/          USDA SR Legacy (SR28) source files, read by build_foods.py
docs/supabase-schema.sql    database tables matching supabase.example.js
```

## Data

| What                    | Source                                                                                                                                                                                  |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nutrient amounts        | USDA FoodData Central: **Foundation Foods** where a food has been matched (marked † in the app), otherwise **SR Legacy**. Each food keeps its USDA record number.                       |
| Biotin, iodine, omega-3 | NIH Office of Dietary Supplements fact sheets, where USDA has no value. Foods not listed there show "not measured".                                                                     |
| Daily Values            | FDA Nutrition Facts label values. Omega-3 has no FDA value, so 1.6 g (the NIH adequate intake of ALA for men) is used.                                                                  |
| Serving sizes           | FDA reference amounts, 21 CFR 101.12: 85 g vegetables, 140 g fresh fruit, 30 g nuts and seeds, 90 g cooked beans, 140 g cooked grains, 85 g cooked meat and fish, 4 g herbs, and so on. |

A **rich source** gives 20% or more of the Daily Value in one serving; a **good source** gives 10–19%. These are FDA's "high in" and "good source of" thresholds. Produce, nuts and seeds use raw values; beans, grains, meat and fish use plain cooked values.

### Updating the data

`src/data/foods.json` is already generated, so the site runs without Python. The scripts need Python 3.9+ and no extra packages. On Windows, use `python` instead of `python3`.

Fetch the newest Foundation Foods values (USDA releases them every April and October). A free API key is available at https://fdc.nal.usda.gov/api-key-signup.

```bash
python3 scripts/update_from_fdc.py --api-key YOUR_KEY
python3 scripts/update_from_fdc.py --step review     # answer uncertain matches one by one
python3 scripts/update_from_fdc.py --api-key YOUR_KEY # fetch values for the ones you confirmed
```

Foods are matched automatically only when the match is unambiguous; everything else goes to the review step. Your answers are saved in `scripts/foundation_map.json` and kept on later runs. Instead of an API key, you can pass the Foundation Foods CSV download with `--csv path/to/file.zip`.

After editing `scripts/foodlist.py` to add or change foods, regenerate the data:

```bash
python3 scripts/build_foods.py --review
```

`--review` prints each food next to USDA's own description so you can check the mapping.

Allergen tags used in `foodlist.py`: `lactose`, `dairy`, `gluten`, `egg`, `peanut`, `treenut`, `soy`, `fish`, `shellfish`, `sesame`. Diets are worked out from each food's category.

## Contact

Kaustubh Hari Sethi: kaustubhsethi14@gmail.com, [LinkedIn](https://www.linkedin.com/in/kaustubh-hari-sethi/), [kaustubhsethi.com](https://kaustubhsethi.com/)

Nutrayo provides general information, not medical advice.
