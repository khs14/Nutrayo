// NOT USED YET. Template for when you add login.
//
// 1. npm install @supabase/supabase-js
// 2. Create a free Supabase project, run docs/supabase-schema.sql in its SQL editor.
// 3. Put the project URL and anon key in .env:
//      VITE_SUPABASE_URL=...
//      VITE_SUPABASE_ANON_KEY=...
//    (The anon key is safe in the browser; row-level security protects each user's rows.)
// 4. Rename this file to supabase.js, then after sign-in:
//      import { createSupabaseBackend } from './lib/backends/supabase.js';
//      await store.useBackend(createSupabaseBackend(supabase, user.id));
//
// import { createClient } from '@supabase/supabase-js';
// export const supabase = createClient(
//   import.meta.env.VITE_SUPABASE_URL,
//   import.meta.env.VITE_SUPABASE_ANON_KEY
// );

export function createSupabaseBackend(supabase, userId) {
  return {
    name: 'account',

    async load() {
      const [{ data: prefsRow }, { data: reactions }] = await Promise.all([
        supabase.from('preferences').select('diet, avoid').eq('user_id', userId).maybeSingle(),
        supabase.from('food_reactions').select('food_id, reaction').eq('user_id', userId),
      ]);
      return {
        prefs: prefsRow ? { diet: prefsRow.diet, avoid: prefsRow.avoid } : undefined,
        liked: (reactions || []).filter((r) => r.reaction === 'like').map((r) => r.food_id),
        hidden: (reactions || []).filter((r) => r.reaction === 'hide').map((r) => r.food_id),
      };
    },

    async savePrefs(prefs) {
      await supabase.from('preferences').upsert({ user_id: userId, diet: prefs.diet, avoid: prefs.avoid });
    },

    async clearReactions(kind) {
      await supabase.from('food_reactions').delete().eq('user_id', userId).eq('reaction', kind);
    },

    async setReaction(foodId, reaction) {
      if (reaction === null) {
        await supabase.from('food_reactions').delete().eq('user_id', userId).eq('food_id', foodId);
      } else {
        await supabase.from('food_reactions').upsert({ user_id: userId, food_id: foodId, reaction });
      }
    },
  };
}
