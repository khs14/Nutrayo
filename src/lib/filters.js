// Diet + allergy rules. Pure functions: no DOM, no storage, easy to test.

export const DIETS = [
  { id: 'all', label: 'Everything', hint: 'All foods' },
  { id: 'pescatarian', label: 'Pescatarian', hint: 'No meat or poultry. Fish, shellfish, eggs and dairy are included.' },
  { id: 'vegetarian', label: 'Vegetarian', hint: 'No meat, poultry, fish or shellfish. Eggs and dairy are included.' },
  { id: 'vegan', label: 'Vegan', hint: 'Plants only: no meat, fish, eggs or dairy.' },
];

export const AVOIDS = [
  { id: 'lactose', label: 'Lactose' },
  { id: 'dairy', label: 'Milk allergy' },
  { id: 'gluten', label: 'Gluten' },
  { id: 'egg', label: 'Eggs' },
  { id: 'peanut', label: 'Peanuts' },
  { id: 'treenut', label: 'Tree nuts' },
  { id: 'soy', label: 'Soy' },
  { id: 'fish', label: 'Fish' },
  { id: 'shellfish', label: 'Shellfish' },
  { id: 'sesame', label: 'Sesame' },
];

const NOT_ALLOWED = {
  all: [],
  pescatarian: ['meat', 'poultry'],
  vegetarian: ['meat', 'poultry', 'fish', 'shellfish'],
  vegan: ['meat', 'poultry', 'fish', 'shellfish', 'dairy', 'egg'],
};

const ALLERGEN_WORD = {
  lactose: 'lactose', dairy: 'milk', gluten: 'gluten', egg: 'egg', peanut: 'peanuts',
  treenut: 'tree nuts', soy: 'soy', fish: 'fish', shellfish: 'shellfish', sesame: 'sesame',
};
export const allergenWord = (id) => ALLERGEN_WORD[id] ?? id;

/**
 * Why a food is excluded by the user's choices, or null if it's allowed.
 * prefs: { diet, avoid: string[] }, hidden: Set of food ids the user hid.
 */
export function excludedReason(food, prefs, hidden = new Set()) {
  if (hidden.has(food.id)) return 'You hid this';
  if (NOT_ALLOWED[prefs.diet]?.includes(food.category)) {
    return `Not ${DIETS.find((d) => d.id === prefs.diet).label.toLowerCase()}`;
  }
  const hit = food.allergens.find((a) => prefs.avoid.includes(a));
  if (hit) return `Contains ${allergenWord(hit)}`;
  return null;
}

export const isAllowed = (food, prefs, hidden) => excludedReason(food, prefs, hidden) === null;
