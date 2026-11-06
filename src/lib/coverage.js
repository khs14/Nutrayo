// Which nutrients a set of foods covers, and which are still missing.
// Used today by the Examples page. Later the same function powers
// "what's covered / what's left" for a signed-in user's liked foods.
import { nutrients, foodById } from './data.js';

/**
 * @param {string[]} foodIds
 * @returns {{ covered: Map<string,'high'|'good'>, missing: string[] }}
 */
export function coverage(foodIds) {
  const covered = new Map();
  for (const id of foodIds) {
    const food = foodById[id];
    if (!food) continue;
    for (const n of food.good) if (!covered.has(n)) covered.set(n, 'good');
    for (const n of food.high) covered.set(n, 'high');
  }
  const missing = nutrients.filter((n) => !covered.has(n.id)).map((n) => n.id);
  return { covered, missing };
}
