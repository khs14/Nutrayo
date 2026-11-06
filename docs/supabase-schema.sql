-- Run in the Supabase SQL editor when you add login.
-- Food and nutrient data stay as static JSON in the site; only per-user choices live here.

create table preferences (
  user_id uuid primary key references auth.users on delete cascade,
  diet text not null default 'all',
  avoid text[] not null default '{}',
  updated_at timestamptz not null default now()
);

create table food_reactions (
  user_id uuid references auth.users on delete cascade,
  food_id text not null,                       -- matches "id" in src/data/foods.json
  reaction text not null check (reaction in ('like', 'hide')),
  created_at timestamptz not null default now(),
  primary key (user_id, food_id)
);

-- Each user can only see and change their own rows.
alter table preferences enable row level security;
alter table food_reactions enable row level security;

create policy "own prefs" on preferences
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "own reactions" on food_reactions
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
