// Guest-mode backend: saves to this browser only.
const KEY = 'nutrayo:v1';
const OLD_KEY = 'nutrient-table:v1'; // name before the rename; migrated once

try {
  if (!localStorage.getItem(KEY) && localStorage.getItem(OLD_KEY)) {
    localStorage.setItem(KEY, localStorage.getItem(OLD_KEY));
    localStorage.removeItem(OLD_KEY);
  }
} catch {
  /* storage blocked: nothing to migrate */
}

function read() {
  try {
    return JSON.parse(localStorage.getItem(KEY)) || {};
  } catch {
    return {};
  }
}
function write(data) {
  try {
    localStorage.setItem(KEY, JSON.stringify(data));
  } catch {
    /* private mode or storage blocked: keep working in memory */
  }
}

export const localBackend = {
  name: 'guest',
  async load() {
    const d = read();
    return { prefs: d.prefs, liked: d.liked || [], hidden: d.hidden || [] };
  },
  async savePrefs(prefs) {
    write({ ...read(), prefs });
  },
  async setReaction(foodId, reaction) {
    const d = read();
    const liked = new Set(d.liked || []);
    const hidden = new Set(d.hidden || []);
    liked.delete(foodId);
    hidden.delete(foodId);
    if (reaction === 'like') liked.add(foodId);
    if (reaction === 'hide') hidden.add(foodId);
    write({ ...d, liked: [...liked], hidden: [...hidden] });
  },
  async clearReactions(kind) {
    const d = read();
    write({ ...d, [kind === 'like' ? 'liked' : 'hidden']: [] });
  },
  /** Used later to copy guest choices into a new account on first login. */
  exportAll() {
    return read();
  },
};
