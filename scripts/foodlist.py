# Curated single ingredients, mapped to USDA SR28 / SR Legacy NDB numbers.
# (ndb, display name, form shown to users, category, serving key, allergens, tip)
#
# Serving keys follow FDA reference amounts (21 CFR 101.12, Table 2); meat and
# poultry use the 85 g cooked amount that USDA FSIS uses for the same foods.

SERVINGS = {
    'F':  (140, '140 g'),          # fresh fruit
    'DF': (40,  '40 g'),           # dried fruit
    'AV': (50,  '50 g'),           # avocado
    'V':  (85,  '85 g'),           # vegetables
    'P':  (110, '110 g'),          # potatoes, sweet potatoes, yams
    'H':  (4,   '4 g'),            # herbs and flavouring vegetables
    'SP': (None, '¼ cup'),         # sprouts: ¼ of USDA's 1-cup weight
    'N':  (30,  '30 g'),           # nuts, seeds, peanuts
    'L':  (90,  '90 g'),    # beans and lentils, prepared
    'TF': (85,  '85 g'),           # tofu, tempeh
    'GC': (140, '140 g'),   # grains, prepared
    'GD': (45,  '45 g'),       # grains, dry
    'OT': (40,  '40 g'),       # hot cereal grains (oats), dry
    'E':  (50,  '1 large egg'),
    'M':  (244, '1 cup (240 mL)'),
    'C':  (30,  '30 g'),           # cheese
    'CT': (110, '110 g'),          # cottage cheese
    'Y':  (170, '170 g'),          # yogurt
    'MT': (85,  '85 g'),    # meat, poultry, fish, shellfish
    'CN': (85,  '85 g'),           # canned fish
    'OL': (15,  '15 g'),           # olives
    'SW': (5,   '5 g'),        # dried seaweed products
}

PLANT_MILK_TIP = ("Packaged drink: values depend on the producer. Most of the calcium, vitamin D and B12 "
                  "is added by the maker and varies by brand, so check the carton. These are USDA's figures for one typical product.")

SPROUT_TIP = "Raw sprouts carry a higher risk of food poisoning. FDA advises children, older adults and pregnant people to eat them cooked."

FOODS = [
    # ---------------- Vegetables ----------------
    ('11001', 'Alfalfa sprouts', 'Raw', 'vegetable', 'SP', [], SPROUT_TIP),
    ('11003', 'Amaranth leaves', 'Raw', 'vegetable', 'V', [], None),
    ('11007', 'Artichoke', 'Raw', 'vegetable', 'V', [], None),
    ('11959', 'Arugula', 'Raw', 'vegetable', 'V', [], None),
    ('11011', 'Asparagus', 'Raw', 'vegetable', 'V', [], None),
    ('11026', 'Bamboo shoots', 'Raw', 'vegetable', 'V', [], None),
    ('11052', 'Green beans', 'Raw', 'vegetable', 'V', [], None),
    ('11086', 'Beet greens', 'Raw', 'vegetable', 'V', [], None),
    ('11080', 'Beetroot', 'Raw', 'vegetable', 'V', [], None),
    ('11116', 'Bok choy', 'Raw', 'vegetable', 'V', [], None),
    ('11090', 'Broccoli', 'Raw', 'vegetable', 'V', [], None),
    ('11096', 'Broccoli rabe', 'Raw', 'vegetable', 'V', [], None),
    ('11994', 'Chinese broccoli (gai lan)', 'Raw', 'vegetable', 'V', [], None),
    ('11098', 'Brussels sprouts', 'Raw', 'vegetable', 'V', [], None),
    ('11104', 'Burdock root', 'Raw', 'vegetable', 'V', [], None),
    ('11109', 'Green cabbage', 'Raw', 'vegetable', 'V', [], None),
    ('11112', 'Red cabbage', 'Raw', 'vegetable', 'V', [], None),
    ('11114', 'Savoy cabbage', 'Raw', 'vegetable', 'V', [], None),
    ('11119', 'Napa cabbage', 'Raw', 'vegetable', 'V', [], None),
    ('11124', 'Carrot', 'Raw', 'vegetable', 'V', [], None),
    ('11135', 'Cauliflower', 'Raw', 'vegetable', 'V', [], None),
    ('11141', 'Celeriac', 'Raw', 'vegetable', 'V', [], None),
    ('11143', 'Celery', 'Raw', 'vegetable', 'V', [], None),
    ('11147', 'Swiss chard', 'Raw', 'vegetable', 'V', [], None),
    ('11149', 'Chayote', 'Raw', 'vegetable', 'V', [], None),
    ('11161', 'Collard greens', 'Raw', 'vegetable', 'V', [], None),
    ('11167', 'Sweet corn', 'Raw', 'vegetable', 'V', [], None),
    ('11203', 'Garden cress', 'Raw', 'vegetable', 'V', [], None),
    ('11205', 'Cucumber', 'Raw, with peel', 'vegetable', 'V', [], None),
    ('11207', 'Dandelion greens', 'Raw', 'vegetable', 'V', [], None),
    ('11222', 'Moringa leaves', 'Raw', 'vegetable', 'V', [], None),
    ('11209', 'Eggplant', 'Raw', 'vegetable', 'V', [], None),
    ('11213', 'Curly endive', 'Raw', 'vegetable', 'V', [], None),
    ('11151', 'Belgian endive', 'Raw', 'vegetable', 'V', [], None),
    ('11957', 'Fennel bulb', 'Raw', 'vegetable', 'V', [], None),
    ('11974', 'Grape leaves', 'Raw', 'vegetable', 'V', [], None),
    ('43392', 'Hearts of palm', 'Raw', 'vegetable', 'V', [], None),
    ('11226', 'Jerusalem artichoke', 'Raw', 'vegetable', 'V', [], None),
    ('11233', 'Kale', 'Raw', 'vegetable', 'V', [], None),
    ('11241', 'Kohlrabi', 'Raw', 'vegetable', 'V', [], None),
    ('11246', 'Leeks', 'Raw', 'vegetable', 'V', [], None),
    ('11248', 'Lentil sprouts', 'Raw', 'vegetable', 'SP', [], SPROUT_TIP),
    ('11250', 'Butterhead lettuce', 'Raw', 'vegetable', 'V', [], None),
    ('11251', 'Romaine lettuce', 'Raw', 'vegetable', 'V', [], None),
    ('11253', 'Green leaf lettuce', 'Raw', 'vegetable', 'V', [], None),
    ('11252', 'Iceberg lettuce', 'Raw', 'vegetable', 'V', [], None),
    ('11254', 'Lotus root', 'Raw', 'vegetable', 'V', [], None),
    ('11043', 'Mung bean sprouts', 'Raw', 'vegetable', 'SP', [], SPROUT_TIP),
    ('11270', 'Mustard greens', 'Raw', 'vegetable', 'V', [], None),
    ('11963', 'Nopales (cactus pads)', 'Raw', 'vegetable', 'V', [], None),
    ('11278', 'Okra', 'Raw', 'vegetable', 'V', [], None),
    ('11282', 'Onion', 'Raw', 'vegetable', 'V', [], None),
    ('11291', 'Spring onions', 'Raw', 'vegetable', 'V', [], None),
    ('11298', 'Parsnip', 'Raw', 'vegetable', 'V', [], None),
    ('11304', 'Green peas', 'Raw', 'vegetable', 'V', [], None),
    ('11300', 'Snow peas', 'Raw', 'vegetable', 'V', [], None),
    ('11333', 'Green bell pepper', 'Raw', 'vegetable', 'V', [], None),
    ('11821', 'Red bell pepper', 'Raw', 'vegetable', 'V', [], None),
    ('11951', 'Yellow bell pepper', 'Raw', 'vegetable', 'V', [], None),
    ('11674', 'Potato', 'Baked, with skin', 'vegetable', 'P', [], None),
    ('11508', 'Sweet potato', 'Baked', 'vegetable', 'P', [], None),
    ('11602', 'Yam', 'Cooked', 'vegetable', 'P', [], None),
    ('11422', 'Pumpkin', 'Raw', 'vegetable', 'V', [], None),
    ('11427', 'Purslane', 'Raw', 'vegetable', 'V', [], None),
    ('11952', 'Radicchio', 'Raw', 'vegetable', 'V', [], None),
    ('11429', 'Radish', 'Raw', 'vegetable', 'V', [], None),
    ('11430', 'Daikon radish', 'Raw', 'vegetable', 'V', [], None),
    ('11435', 'Rutabaga', 'Raw', 'vegetable', 'V', [], None),
    ('11457', 'Spinach', 'Raw', 'vegetable', 'V', [], None),
    ('11477', 'Zucchini', 'Raw', 'vegetable', 'V', [], None),
    ('11482', 'Acorn squash', 'Raw', 'vegetable', 'V', [], None),
    ('11485', 'Butternut squash', 'Raw', 'vegetable', 'V', [], None),
    ('11492', 'Spaghetti squash', 'Raw', 'vegetable', 'V', [], None),
    ('11954', 'Tomatillo', 'Raw', 'vegetable', 'V', [], None),
    ('11529', 'Tomato', 'Raw', 'vegetable', 'V', [], None),
    ('11564', 'Turnip', 'Raw', 'vegetable', 'V', [], None),
    ('11568', 'Turnip greens', 'Raw', 'vegetable', 'V', [], None),
    ('11588', 'Water chestnuts', 'Raw', 'vegetable', 'V', [], None),
    ('11591', 'Watercress', 'Raw', 'vegetable', 'V', [], None),
    ('11603', 'Jicama', 'Raw', 'vegetable', 'V', [], None),
    ('11212', 'Edamame', 'Cooked', 'legume', 'V', ['soy'], None),

    # ---------------- Herbs and flavourings (FDA serving is 4 g) ----------------
    ('11215', 'Garlic', 'Raw', 'herb', 'H', [], None),
    ('11216', 'Ginger root', 'Raw', 'herb', 'H', [], None),
    ('11677', 'Shallots', 'Raw', 'herb', 'H', [], None),
    ('11979', 'Jalapeño', 'Raw', 'herb', 'H', [], None),
    ('11972', 'Lemongrass', 'Raw', 'herb', 'H', [], None),
    ('11156', 'Chives', 'Fresh', 'herb', 'H', [], None),
    ('11165', 'Cilantro (coriander leaves)', 'Fresh', 'herb', 'H', [], None),
    ('11297', 'Parsley', 'Fresh', 'herb', 'H', [], None),
    ('02044', 'Basil', 'Fresh', 'herb', 'H', [], None),
    ('02045', 'Dill', 'Fresh', 'herb', 'H', [], None),
    ('02065', 'Spearmint', 'Fresh', 'herb', 'H', [], None),
    ('02064', 'Peppermint', 'Fresh', 'herb', 'H', [], None),
    ('02049', 'Thyme', 'Fresh', 'herb', 'H', [], None),
    ('02063', 'Rosemary', 'Fresh', 'herb', 'H', [], None),
    ('11990', 'Wasabi root', 'Raw', 'herb', 'H', [], None),

    # ---------------- Mushrooms ----------------
    ('11260', 'White button mushrooms', 'Raw', 'mushroom', 'V', [], None),
    ('11938', 'White mushrooms, UV-exposed', 'Raw', 'mushroom', 'V', [],
     'Mushrooms grown under UV light are labelled as such. Ordinary mushrooms have very little vitamin D.'),
    ('11266', 'Cremini mushrooms', 'Raw', 'mushroom', 'V', [], None),
    ('11265', 'Portabella mushrooms', 'Raw', 'mushroom', 'V', [], None),
    ('11238', 'Shiitake mushrooms', 'Raw', 'mushroom', 'V', [], None),
    ('11987', 'Oyster mushrooms', 'Raw', 'mushroom', 'V', [], None),
    ('11993', 'Maitake mushrooms', 'Raw', 'mushroom', 'V', [], None),
    ('11950', 'Enoki mushrooms', 'Raw', 'mushroom', 'V', [], None),
    ('11239', 'Chanterelle mushrooms', 'Raw', 'mushroom', 'V', [], None),
    ('11240', 'Morel mushrooms', 'Raw', 'mushroom', 'V', [], None),

    # ---------------- Seaweed ----------------
    ('11446', 'Laver (nori)', 'Raw', 'seaweed', 'V', [],
     'USDA lists fresh laver. Dried nori is much more concentrated: NIH lists 116 µg iodine in 2 tbsp of flakes (5 g).'),
    ('11445', 'Kelp', 'Raw', 'seaweed', 'V', [],
     'Kelp can contain far more iodine than the safe daily limit, and the amount varies a lot. USDA does not list iodine for it.'),
    ('11669', 'Wakame', 'Raw', 'seaweed', 'V', [], None),
    ('11667', 'Spirulina', 'Dried', 'seaweed', 'SW', [], None),

    # ---------------- Fruit ----------------
    ('09001', 'Acerola cherry', 'Raw', 'fruit', 'F', [], None),
    ('09003', 'Apple', 'Raw, with skin', 'fruit', 'F', [], None),
    ('09021', 'Apricot', 'Raw', 'fruit', 'F', [], None),
    ('09037', 'Avocado', 'Raw', 'fruit', 'AV', [], None),
    ('09040', 'Banana', 'Raw', 'fruit', 'F', [], None),
    ('09042', 'Blackberries', 'Raw', 'fruit', 'F', [], None),
    ('09050', 'Blueberries', 'Raw', 'fruit', 'F', [], None),
    ('09060', 'Starfruit', 'Raw', 'fruit', 'F', [], None),
    ('09062', 'Cherimoya', 'Raw', 'fruit', 'F', [], None),
    ('09070', 'Sweet cherries', 'Raw', 'fruit', 'F', [], None),
    ('09063', 'Sour cherries', 'Raw', 'fruit', 'F', [], None),
    ('09433', 'Clementine', 'Raw', 'fruit', 'F', [], None),
    ('09078', 'Cranberries', 'Raw', 'fruit', 'F', [], None),
    ('09083', 'Blackcurrants', 'Raw', 'fruit', 'F', [], None),
    ('09422', 'Durian', 'Raw', 'fruit', 'F', [], None),
    ('09088', 'Elderberries', 'Raw', 'fruit', 'F', [], 'Raw elderberries can make you sick. Cook them before eating.'),
    ('09334', 'Feijoa', 'Raw', 'fruit', 'F', [], None),
    ('09089', 'Figs', 'Raw', 'fruit', 'F', [], None),
    ('09107', 'Gooseberries', 'Raw', 'fruit', 'F', [], None),
    ('09111', 'Grapefruit', 'Raw', 'fruit', 'F', [],
     'Grapefruit interacts with some medicines, including some statins. Check with a pharmacist.'),
    ('09132', 'Grapes', 'Raw', 'fruit', 'F', [], None),
    ('09139', 'Guava', 'Raw', 'fruit', 'F', [], None),
    ('09144', 'Jackfruit', 'Raw', 'fruit', 'F', [], None),
    ('09146', 'Jujube', 'Raw', 'fruit', 'F', [], None),
    ('09148', 'Kiwi, green', 'Raw', 'fruit', 'F', [], None),
    ('09520', 'Kiwi, gold', 'Raw', 'fruit', 'F', [], None),
    ('09149', 'Kumquat', 'Raw', 'fruit', 'F', [], None),
    ('09150', 'Lemon', 'Raw, without peel', 'fruit', 'F', [], None),
    ('09159', 'Lime', 'Raw', 'fruit', 'F', [], None),
    ('09164', 'Lychee', 'Raw', 'fruit', 'F', [], None),
    ('09172', 'Longan', 'Raw', 'fruit', 'F', [], None),
    ('09176', 'Mango', 'Raw', 'fruit', 'F', [], None),
    ('09181', 'Cantaloupe', 'Raw', 'fruit', 'F', [], None),
    ('09184', 'Honeydew melon', 'Raw', 'fruit', 'F', [], None),
    ('09190', 'Mulberries', 'Raw', 'fruit', 'F', [], None),
    ('09191', 'Nectarine', 'Raw', 'fruit', 'F', [], None),
    ('09200', 'Orange', 'Raw', 'fruit', 'F', [], None),
    ('09226', 'Papaya', 'Raw', 'fruit', 'F', [], None),
    ('09231', 'Passion fruit', 'Raw', 'fruit', 'F', [], None),
    ('09236', 'Peach', 'Raw', 'fruit', 'F', [], None),
    ('09252', 'Pear', 'Raw', 'fruit', 'F', [], None),
    ('09340', 'Asian pear', 'Raw', 'fruit', 'F', [], None),
    ('09263', 'Persimmon', 'Raw', 'fruit', 'F', [], None),
    ('09266', 'Pineapple', 'Raw', 'fruit', 'F', [], None),
    ('09277', 'Plantain', 'Raw', 'fruit', 'F', [], 'Plantains are usually cooked before eating.'),
    ('09279', 'Plum', 'Raw', 'fruit', 'F', [], None),
    ('09286', 'Pomegranate', 'Raw', 'fruit', 'F', [], None),
    ('09287', 'Prickly pear', 'Raw', 'fruit', 'F', [], None),
    ('09295', 'Pomelo', 'Raw', 'fruit', 'F', [], None),
    ('09296', 'Quince', 'Raw', 'fruit', 'F', [], None),
    ('09302', 'Raspberries', 'Raw', 'fruit', 'F', [], None),
    ('09307', 'Rhubarb', 'Raw stalks', 'fruit', 'F', [], 'Eat only the stalks. Rhubarb leaves are poisonous.'),
    ('09313', 'Sapodilla', 'Raw', 'fruit', 'F', [], None),
    ('09314', 'Mamey sapote', 'Raw', 'fruit', 'F', [], None),
    ('09315', 'Soursop', 'Raw', 'fruit', 'F', [], None),
    ('09316', 'Strawberries', 'Raw', 'fruit', 'F', [], None),
    ('09322', 'Tamarind', 'Raw pulp', 'fruit', 'F', [], None),
    ('09218', 'Tangerine', 'Raw', 'fruit', 'F', [], None),
    ('09326', 'Watermelon', 'Raw', 'fruit', 'F', [], None),
    ('09421', 'Medjool dates', 'Dried', 'fruit', 'DF', [], None),
    ('09094', 'Dried figs', 'Dried', 'fruit', 'DF', [], None),
    ('09298', 'Raisins', 'Dried', 'fruit', 'DF', [], None),
    ('09291', 'Prunes', 'Dried', 'fruit', 'DF', [], None),
    ('09032', 'Dried apricots', 'Dried', 'fruit', 'DF', [], None),
    ('09193', 'Black olives', 'Ripe, canned', 'fruit', 'OL', [], None),

    # ---------------- Nuts and seeds ----------------
    ('12061', 'Almonds', 'Raw', 'nut', 'N', ['treenut'], None),
    ('12078', 'Brazil nuts', 'Raw', 'nut', 'N', ['treenut'],
     'Selenium in Brazil nuts varies with the soil. A handful can go over the safe daily limit of 400 µg, so keep it to one or two a day.'),
    ('12087', 'Cashews', 'Raw', 'nut', 'N', ['treenut'], None),
    ('12098', 'Chestnuts', 'Raw, peeled', 'nut', 'N', ['treenut'], None),
    ('12120', 'Hazelnuts', 'Raw', 'nut', 'N', ['treenut'], None),
    ('12131', 'Macadamia nuts', 'Raw', 'nut', 'N', ['treenut'], None),
    ('12142', 'Pecans', 'Raw', 'nut', 'N', ['treenut'], None),
    ('12147', 'Pine nuts', 'Dried', 'nut', 'N', ['treenut'], None),
    ('12151', 'Pistachios', 'Raw', 'nut', 'N', ['treenut'], None),
    ('12155', 'Walnuts', 'Raw', 'nut', 'N', ['treenut'], None),
    ('12154', 'Black walnuts', 'Dried', 'nut', 'N', ['treenut'], None),
    ('12104', 'Coconut meat', 'Raw', 'nut', 'N', ['treenut'],
     'Many people with a tree-nut allergy can eat coconut, but some react to it. It is hidden when you avoid tree nuts, to be safe. Ask your allergist.'),
    ('16087', 'Peanuts', 'Raw', 'legume', 'N', ['peanut'], None),
    ('12006', 'Chia seeds', 'Dried', 'seed', 'N', [], None),
    ('12220', 'Flaxseeds', 'Whole', 'seed', 'N', [], 'Grind flaxseeds before eating. Whole seeds often pass through undigested.'),
    ('12012', 'Hemp seeds', 'Hulled', 'seed', 'N', [], None),
    ('12014', 'Pumpkin seeds', 'Dried kernels', 'seed', 'N', [], None),
    ('12023', 'Sesame seeds', 'Whole, dried', 'seed', 'N', ['sesame'], None),
    ('12036', 'Sunflower seeds', 'Dried kernels', 'seed', 'N', [], None),

    # ---------------- Legumes (boiled, no salt) ----------------
    ('16002', 'Adzuki beans', 'Boiled', 'legume', 'L', [], None),
    ('16015', 'Black beans', 'Boiled', 'legume', 'L', [], None),
    ('16063', 'Black-eyed peas', 'Boiled', 'legume', 'L', [], None),
    ('16057', 'Chickpeas', 'Boiled', 'legume', 'L', [], None),
    ('16053', 'Fava beans', 'Boiled', 'legume', 'L', [], None),
    ('16025', 'Great northern beans', 'Boiled', 'legume', 'L', [], None),
    ('16033', 'Red kidney beans', 'Boiled', 'legume', 'L', [], 'Never eat kidney beans raw or undercooked. Boil them for at least 10 minutes.'),
    ('16070', 'Lentils', 'Boiled', 'legume', 'L', [], None),
    ('16072', 'Lima beans', 'Boiled', 'legume', 'L', [], None),
    ('16077', 'Lupini beans', 'Boiled', 'legume', 'L', [], 'Lupin is a common allergen in Europe, especially for people allergic to peanuts.'),
    ('16081', 'Mung beans', 'Boiled', 'legume', 'L', [], None),
    ('16038', 'Navy beans', 'Boiled', 'legume', 'L', [], None),
    ('16102', 'Pigeon peas', 'Boiled', 'legume', 'L', [], None),
    ('16043', 'Pinto beans', 'Boiled', 'legume', 'L', [], None),
    ('16109', 'Soybeans', 'Boiled', 'legume', 'L', ['soy'], None),
    ('16086', 'Split peas', 'Boiled', 'legume', 'L', [], None),
    ('16084', 'Urad dal (black gram)', 'Boiled', 'legume', 'L', [], None),
    ('16427', 'Tofu, calcium-set', 'Raw', 'legume', 'TF', ['soy'], 'Tofu made with calcium sulfate is high in calcium. Check the label for calcium sulfate.'),
    ('16114', 'Tempeh', 'Plain', 'legume', 'TF', ['soy'], None),

    # ---------------- Grains ----------------
    ('20002', 'Amaranth', 'Cooked', 'grain', 'GC', [], None),
    ('20006', 'Barley, pearled', 'Cooked', 'grain', 'GC', ['gluten'], None),
    ('20010', 'Buckwheat groats', 'Cooked', 'grain', 'GC', [], None),
    ('20013', 'Bulgur wheat', 'Cooked', 'grain', 'GC', ['gluten'], None),
    ('20032', 'Millet', 'Cooked', 'grain', 'GC', [], None),
    ('20038', 'Oats', 'Dry', 'grain', 'OT', ['gluten'],
     'Oats are naturally gluten-free but are often contaminated with wheat. Choose oats labelled gluten-free if you need them.'),
    ('20137', 'Quinoa', 'Cooked', 'grain', 'GC', [], None),
    ('20037', 'Brown rice', 'Cooked', 'grain', 'GC', [], None),
    ('20445', 'White rice', 'Cooked, unenriched', 'grain', 'GC', [], None),
    ('20089', 'Wild rice', 'Cooked', 'grain', 'GC', [], None),
    ('20062', 'Rye berries', 'Dry', 'grain', 'GD', ['gluten'], None),
    ('20067', 'Sorghum', 'Dry', 'grain', 'GD', [], None),
    ('20141', 'Spelt', 'Cooked', 'grain', 'GC', ['gluten'], None),
    ('20143', 'Teff', 'Cooked', 'grain', 'GC', [], None),
    ('20139', 'Kamut (khorasan wheat)', 'Cooked', 'grain', 'GC', ['gluten'], None),
    ('20072', 'Wheat berries', 'Dry', 'grain', 'GD', ['gluten'], None),

    # ---------------- Dairy and eggs ----------------
    ('01077', 'Whole milk', 'Vitamin D added', 'dairy', 'M', ['dairy', 'lactose'],
     'Vitamin D in milk comes from fortification, which is standard in the US but varies by country.'),
    ('01085', 'Skim milk', 'Vitamins A and D added', 'dairy', 'M', ['dairy', 'lactose'], None),
    ('01106', "Goat's milk", 'Vitamin D added', 'dairy', 'M', ['dairy', 'lactose'], None),
    ('01116', 'Plain yogurt', 'Whole milk', 'dairy', 'Y', ['dairy', 'lactose'],
     'Live cultures break down some of the lactose, so many people with mild lactose intolerance manage small amounts.'),
    ('01256', 'Greek yogurt', 'Plain, nonfat', 'dairy', 'Y', ['dairy', 'lactose'], None),
    ('01009', 'Cheddar cheese', 'Aged', 'dairy', 'C', ['dairy'],
     'Aged hard cheeses have almost no lactose, so most lactose-intolerant people can eat them. Not safe with a milk allergy.'),
    ('01040', 'Swiss cheese', 'Aged', 'dairy', 'C', ['dairy'],
     'Aged hard cheeses have almost no lactose, so most lactose-intolerant people can eat them. Not safe with a milk allergy.'),
    ('01156', 'Goat cheese, hard', 'Aged', 'dairy', 'C', ['dairy'], None),
    ('01026', 'Mozzarella', 'Whole milk', 'dairy', 'C', ['dairy', 'lactose'], None),
    ('01019', 'Feta', 'Fresh', 'dairy', 'C', ['dairy', 'lactose'], None),
    ('01012', 'Cottage cheese', 'Creamed', 'dairy', 'CT', ['dairy', 'lactose'], None),
    ('01129', 'Eggs', 'Hard-boiled', 'egg', 'E', ['egg'], None),

    # ---------------- Plant milks (packaged; values vary by brand) ----------------
    ('16222', 'Soy milk', 'Unsweetened, fortified, varies by brand', 'plantmilk', 'M', ['soy'], PLANT_MILK_TIP),
    ('14091', 'Almond milk', 'Unsweetened, varies by brand', 'plantmilk', 'M', ['treenut'], PLANT_MILK_TIP),
    ('14171', 'Coconut milk (drink)', 'Sweetened, fortified, varies by brand', 'plantmilk', 'M', ['treenut'], PLANT_MILK_TIP),
    ('14639', 'Rice milk', 'Unsweetened, varies by brand', 'plantmilk', 'M', [], PLANT_MILK_TIP),

    # ---------------- Poultry and meat (cooked, lean where available) ----------------
    ('05064', 'Chicken breast', 'Roasted, meat only', 'poultry', 'MT', [], None),
    ('05098', 'Chicken thigh', 'Roasted, meat only', 'poultry', 'MT', [], None),
    ('05028', 'Chicken liver', 'Simmered', 'poultry', 'MT', [],
     'Very high in vitamin A. Eating liver often can go over the safe upper limit, and it is not advised in pregnancy.'),
    ('05186', 'Turkey breast', 'Roasted, light meat', 'poultry', 'MT', [], None),
    ('05142', 'Duck', 'Roasted, meat only', 'poultry', 'MT', [], None),
    ('23629', 'Beef sirloin steak', 'Broiled, lean', 'meat', 'MT', [], None),
    ('23568', 'Ground beef (85% lean)', 'Broiled', 'meat', 'MT', [], None),
    ('13326', 'Beef liver', 'Braised', 'meat', 'MT', [],
     'Very high in vitamin A. Eating liver often can go over the safe upper limit, and it is not advised in pregnancy.'),
    ('10042', 'Pork chop', 'Broiled, lean', 'meat', 'MT', [], None),
    ('10061', 'Pork tenderloin', 'Roasted, lean', 'meat', 'MT', [], None),
    ('17014', 'Lamb leg', 'Roasted, lean', 'meat', 'MT', [], None),
    ('17331', 'Bison, ground', 'Pan-broiled', 'meat', 'MT', [], None),
    ('17165', 'Venison', 'Roasted', 'meat', 'MT', [], None),
    ('17169', 'Goat meat', 'Roasted', 'meat', 'MT', [], None),

    # ---------------- Fish ----------------
    ('15237', 'Atlantic salmon, farmed', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15209', 'Atlantic salmon, wild', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15086', 'Sockeye salmon', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15260', 'Pink salmon', 'Canned, drained', 'fish', 'CN', ['fish'], None),
    ('15047', 'Atlantic mackerel', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15040', 'Atlantic herring', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15089', 'Sardines', 'Canned in tomato sauce, with bones', 'fish', 'CN', ['fish'], None),
    ('15002', 'Anchovies', 'Canned in oil, drained', 'fish', 'CN', ['fish'], None),
    ('15116', 'Rainbow trout, wild', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15121', 'Tuna, light', 'Canned in water', 'fish', 'CN', ['fish'], None),
    ('15221', 'Yellowfin tuna', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15016', 'Atlantic cod', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15034', 'Haddock', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15037', 'Halibut', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15067', 'Alaska pollock', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15029', 'Flounder and sole', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15262', 'Tilapia', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15235', 'Catfish, farmed', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15092', 'Sea bass', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15102', 'Snapper', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15194', 'Mahi-mahi', 'Cooked', 'fish', 'MT', ['fish'], None),
    ('15111', 'Swordfish', 'Cooked', 'fish', 'MT', ['fish'],
     'Swordfish is high in mercury. FDA advises pregnant people and young children to avoid it.'),

    # ---------------- Shellfish ----------------
    ('15151', 'Shrimp', 'Cooked', 'shellfish', 'MT', ['shellfish'], None),
    ('15140', 'Blue crab', 'Cooked', 'shellfish', 'MT', ['shellfish'], None),
    ('15148', 'Lobster', 'Cooked', 'shellfish', 'MT', ['shellfish'], None),
    ('15159', 'Clams', 'Cooked', 'shellfish', 'MT', ['shellfish'], None),
    ('15165', 'Mussels', 'Cooked', 'shellfish', 'MT', ['shellfish'], None),
    ('15244', 'Oysters, wild', 'Cooked', 'shellfish', 'MT', ['shellfish'], None),
    ('15230', 'Octopus', 'Cooked', 'shellfish', 'MT', ['shellfish'], None),
]

# Nutrients USDA SR28 does not report. Values from NIH Office of Dietary
# Supplements fact sheets, given per serving: (amount, grams in that serving).
#   Biotin: ODS Biotin fact sheet, Table 2 (Staggs et al. 2004), µg
#   Iodine: ODS Iodine fact sheet, Table 2 (USDA/FDA/ODS Iodine Database r4, 2024), µg
#   Omega-3 (ALA + EPA + DHA): ODS Omega-3 fact sheet, Table 2, g
ODS = {
    'b7': {
        '13326': (30.8, 85),   # beef liver, cooked, 3 oz
        '01129': (10.0, 50),   # egg, whole, cooked
        '15260': (5.0, 85),    # salmon, pink, canned, 3 oz
        '10042': (3.8, 85),    # pork chop, cooked, 3 oz
        '23568': (3.8, 85),    # hamburger patty, cooked, 3 oz
        '11508': (2.4, 100),   # sweet potato, cooked, 1/2 cup
        '15121': (0.6, 85),    # tuna, canned in water, 3 oz
        '11090': (0.4, 44),    # broccoli, fresh, 1/2 cup
        '01009': (0.4, 28),    # cheddar, 1 oz
        '01116': (0.2, 245),   # plain yogurt, 1 cup
        '09040': (0.2, 75),    # banana, 1/2 cup
        '09003': (0.0, 62),    # apple, 1/2 cup
    },
    'iodine': {
        '15016': (146, 85),    # cod, baked, 3 oz
        '15244': (93, 85),     # oysters, cooked, 3 oz
        '01256': (87, 170),    # Greek yogurt, plain, nonfat, 3/4 cup
        '01085': (84, 245),    # milk, nonfat, 1 cup
        '01129': (31, 50),     # egg, hard boiled, 1 large
        '01009': (14, 28),     # cheddar, 1 oz
        '13326': (14, 85),     # beef liver, cooked, 3 oz
        '15151': (13, 85),     # shrimp, cooked, 3 oz
        '15121': (7, 85),      # tuna, canned in water, 3 oz
        '05064': (1, 85),      # chicken breast, roasted, 3 oz
        '20037': (0, 146),     # brown rice, cooked, 3/4 cup
        '09040': (0, 136),     # banana, 1 large
    },
    'omega3': {
        '12006': (5.06, 28.35),  # chia seeds, 1 oz
        '12155': (2.57, 28.35),  # English walnuts, 1 oz
        '12220': (2.35, 10.3),   # flaxseed, whole, 1 tbsp
        '15237': (1.83, 85),     # salmon, Atlantic, farmed (DHA 1.24 + EPA 0.59)
        '15209': (1.57, 85),     # salmon, Atlantic, wild (1.22 + 0.35)
        '15040': (1.71, 85),     # herring, Atlantic (0.94 + 0.77)
        '15089': (1.19, 85),     # sardines, canned in tomato sauce (0.74 + 0.45)
        '15047': (1.02, 85),     # mackerel, Atlantic (0.59 + 0.43)
        '15260': (0.95, 85),     # salmon, pink, canned (0.04 + 0.63 + 0.28)
        '15116': (0.84, 85),     # trout, rainbow, wild (0.44 + 0.40)
        '12154': (0.76, 28.35),  # black walnuts, 1 oz
        '15244': (0.67, 85),     # oysters, eastern, wild (0.14 + 0.23 + 0.30)
        '15092': (0.65, 85),     # sea bass (0.47 + 0.18)
        '11212': (0.28, 77.5),   # edamame, 1/2 cup
        '15151': (0.24, 85),     # shrimp (0.12 + 0.12)
        '15148': (0.21, 85),     # lobster (0.04 + 0.07 + 0.10)
        '15121': (0.19, 85),     # tuna, light, canned in water (0.17 + 0.02)
        '15262': (0.15, 85),     # tilapia (0.04 + 0.11)
        '15221': (0.10, 85),     # tuna, yellowfin (0.09 + 0.01)
        '23568': (0.04, 85),     # ground beef 85% lean
        '01129': (0.03, 50),     # egg, cooked
        '05064': (0.03, 85),     # chicken breast, roasted (0.02 + 0.01)
    },
}
