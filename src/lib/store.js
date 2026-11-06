// App state for user choices: diet/allergy filters, liked foods, hidden foods.
//
// The UI only talks to this store. Where the data is saved is decided by a
// "backend" object with four methods. Today that's the browser (guest mode).
// When you add login, write a Supabase backend with the same methods and call
// store.useBackend(supabaseBackend) after sign-in. No page code changes.
//
// Backend interface (all async):
//   load()                         -> { prefs, liked: string[], hidden: string[] }
//   savePrefs(prefs)               -> void
//   setReaction(foodId, reaction)  -> void   reaction: 'like' | 'hide' | null
//   clearReactions(kind)           -> void   optional; 'like' | 'hide' (falls back to setReaction per food)
//   name                           -> 'guest' | 'account'
import { localBackend } from './backends/local.js';

const DEFAULT_PREFS = { diet: 'all', avoid: [] };

const state = {
  prefs: { ...DEFAULT_PREFS },
  liked: new Set(),
  hidden: new Set(),
  backend: localBackend,
};
const listeners = new Set();
const emit = () => listeners.forEach((fn) => fn(state));

async function loadFrom(backend) {
  const data = await backend.load();
  state.backend = backend;
  state.prefs = { ...DEFAULT_PREFS, ...(data.prefs || {}) };
  state.liked = new Set(data.liked || []);
  state.hidden = new Set(data.hidden || []);
  emit();
}

function persistReaction(foodId) {
  const r = state.liked.has(foodId) ? 'like' : state.hidden.has(foodId) ? 'hide' : null;
  state.backend.setReaction(foodId, r).catch((e) => console.error('Save failed', e));
}

export const store = {
  get prefs() { return state.prefs; },
  get liked() { return state.liked; },
  get hidden() { return state.hidden; },
  get mode() { return state.backend.name; },

  init: () => loadFrom(localBackend),
  /** Swap storage, e.g. after login. Loads that backend's saved data. */
  useBackend: (backend) => loadFrom(backend),

  subscribe(fn) { listeners.add(fn); return () => listeners.delete(fn); },

  setDiet(diet) {
    state.prefs = { ...state.prefs, diet };
    state.backend.savePrefs(state.prefs);
    emit();
  },
  toggleAvoid(id) {
    const avoid = state.prefs.avoid.includes(id)
      ? state.prefs.avoid.filter((a) => a !== id)
      : [...state.prefs.avoid, id];
    state.prefs = { ...state.prefs, avoid };
    state.backend.savePrefs(state.prefs);
    emit();
  },
  clearFilters() {
    state.prefs = { ...DEFAULT_PREFS };
    state.backend.savePrefs(state.prefs);
    emit();
  },

  /** Like/unlike. Liking a hidden food un-hides it. */
  toggleLike(foodId) {
    if (state.liked.has(foodId)) state.liked.delete(foodId);
    else { state.liked.add(foodId); state.hidden.delete(foodId); }
    persistReaction(foodId);
    emit();
  },
  /** Hide/unhide ("I don't like this"). Hiding a liked food un-likes it. */
  toggleHidden(foodId) {
    if (state.hidden.has(foodId)) state.hidden.delete(foodId);
    else { state.hidden.add(foodId); state.liked.delete(foodId); }
    persistReaction(foodId);
    emit();
  },

  /**
   * Remove every liked ('like') or hidden ('hide') food. Returns the ids that
   * were removed, so the caller can offer Undo with restoreReactions().
   */
  clearReactions(kind) {
    const set = kind === 'like' ? state.liked : state.hidden;
    const removed = [...set];
    if (!removed.length) return removed;
    set.clear();
    const save = state.backend.clearReactions
      ? state.backend.clearReactions(kind)
      : Promise.all(removed.map((id) => state.backend.setReaction(id, null)));
    save.catch((e) => console.error('Save failed', e));
    emit();
    return removed;
  },
  /** Put back foods removed by clearReactions(). */
  restoreReactions(kind, ids) {
    for (const id of ids) {
      if (kind === 'like') { state.liked.add(id); state.hidden.delete(id); }
      else { state.hidden.add(id); state.liked.delete(id); }
      persistReaction(id);
    }
    emit();
  },
};
