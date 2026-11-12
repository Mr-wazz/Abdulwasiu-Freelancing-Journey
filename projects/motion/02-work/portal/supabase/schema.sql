-- Motion Team Portal: database setup for Supabase.
-- Paste this whole file into Supabase > SQL Editor and press Run. It is safe to run again.
--
-- Who can see what:
--   Admin (the team leader): everything.
--   Member: their own records, plus the names, goals and earnings of the people under them.
--   Bank details, to do lists, breakdown requests and screenshots: only the member and the admin.

create extension if not exists pgcrypto;

-- ---------------------------------------------------------------- tables

create table if not exists public.profiles (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid unique references auth.users (id) on delete set null,
  full_name   text not null check (length(trim(full_name)) between 1 and 120),
  email       text,
  phone       text,
  sponsor_id  uuid references public.profiles (id) on delete restrict,
  rank        text not null default 'Distributor',
  role        text not null default 'member' check (role in ('admin', 'member')),
  status      text not null default 'active' check (status in ('pending', 'active', 'inactive')),
  joined_on   date,
  created_at  timestamptz not null default now(),
  check (sponsor_id is null or sponsor_id <> id)
);
create index if not exists profiles_sponsor_idx on public.profiles (sponsor_id);

create table if not exists public.invites (
  profile_id  uuid primary key references public.profiles (id) on delete cascade,
  code        text not null unique check (code ~ '^[A-Z0-9]{8}$'),
  created_at  timestamptz not null default now()
);

create table if not exists public.goals (
  id             uuid primary key default gen_random_uuid(),
  member_id      uuid not null references public.profiles (id) on delete cascade,
  month          text not null check (month ~ '^\d{4}-(0[1-9]|1[0-2])$'),
  target_amount  numeric(14, 2) not null check (target_amount > 0),
  locked         boolean not null default false,
  updated_at     timestamptz not null default now(),
  unique (member_id, month)
);

create table if not exists public.todos (
  id          uuid primary key default gen_random_uuid(),
  member_id   uuid not null references public.profiles (id) on delete cascade,
  due_on      date not null,
  title       text not null check (length(trim(title)) between 1 and 200),
  done        boolean not null default false,
  created_at  timestamptz not null default now()
);
create index if not exists todos_member_day_idx on public.todos (member_id, due_on);

create table if not exists public.earnings (
  id             uuid primary key default gen_random_uuid(),
  member_id      uuid not null references public.profiles (id) on delete cascade,
  amount         numeric(14, 2) not null check (amount > 0),
  earned_on      date not null,
  category       text not null default 'Other',
  note           text,
  proof_path     text,
  status         text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  reject_reason  text,
  reviewed_at    timestamptz,
  created_at     timestamptz not null default now()
);
create index if not exists earnings_member_day_idx on public.earnings (member_id, earned_on);

create table if not exists public.breakdown_requests (
  id           uuid primary key default gen_random_uuid(),
  member_id    uuid not null references public.profiles (id) on delete cascade,
  month        text not null check (month ~ '^\d{4}-(0[1-9]|1[0-2])$'),
  note         text,
  status       text not null default 'pending' check (status in ('pending', 'sent')),
  admin_note   text,
  amount_sent  numeric(14, 2),
  proof_path   text,
  created_at   timestamptz not null default now(),
  resolved_at  timestamptz
);

create table if not exists public.payment_details (
  member_id       uuid primary key references public.profiles (id) on delete cascade,
  bank_name       text not null,
  account_number  text not null,
  account_name    text not null,
  updated_at      timestamptz not null default now()
);

create table if not exists public.products (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  code        text,
  pv          numeric(10, 2) not null default 0 check (pv >= 0),
  bv          numeric(14, 2) not null default 0 check (bv >= 0),
  dp          numeric(14, 2) not null default 0 check (dp >= 0),
  srp         numeric(14, 2) not null default 0 check (srp >= 0),
  active      boolean not null default true,
  created_at  timestamptz not null default now()
);

create table if not exists public.team_settings (
  id                int primary key default 1 check (id = 1),
  team_name         text not null default 'Motion',
  bv_per_pv         numeric(14, 2) not null default 0,
  todo_suggestions  jsonb not null default '[]'::jsonb
);
insert into public.team_settings (id, todo_suggestions)
values (1, '["Talk to 5 new people about the products","Follow up with 3 customers","Post a product on my WhatsApp status","Invite 2 people to see the business","Check in with my downline","Report my earnings with a screenshot"]'::jsonb)
on conflict (id) do nothing;

-- ---------------------------------------------------------------- helper functions
-- These run with owner rights so the privacy rules below can look at the team tree.

create or replace function public.my_profile_id() returns uuid
language sql stable security definer set search_path = public as $$
  select id from public.profiles where user_id = auth.uid() and status = 'active'
$$;

create or replace function public.is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.profiles
    where user_id = auth.uid() and role = 'admin' and status = 'active'
  )
$$;

-- True when "target" sits anywhere under "root" in the sponsor tree.
create or replace function public.is_under(root uuid, target uuid) returns boolean
language sql stable security definer set search_path = public as $$
  with recursive up as (
    select p.id, p.sponsor_id, 1 as depth from public.profiles p where p.id = target
    union all
    select p.id, p.sponsor_id, up.depth + 1
    from public.profiles p join up on p.id = up.sponsor_id
    where up.depth < 100
  )
  select root is not null and exists (select 1 from up where sponsor_id = root)
$$;

-- Admin, the person themselves, or someone above them.
create or replace function public.can_see_member(target uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select public.is_admin()
      or target = public.my_profile_id()
      or public.is_under(public.my_profile_id(), target)
$$;

-- Only the member or the admin.
create or replace function public.is_me_or_admin(target uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select public.is_admin() or target = public.my_profile_id()
$$;

create or replace function public.my_sponsor_id() returns uuid
language sql stable security definer set search_path = public as $$
  select sponsor_id from public.profiles where user_id = auth.uid() and status = 'active'
$$;

-- ---------------------------------------------------------------- sign up
-- The first person to sign up becomes the admin.
-- Everyone after that joins with an invite link, or waits for the admin to approve them.

create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
declare
  v_code text := upper(nullif(trim(new.raw_user_meta_data ->> 'invite_code'), ''));
  v_name text := left(coalesce(nullif(trim(new.raw_user_meta_data ->> 'full_name'), ''), split_part(new.email, '@', 1)), 120);
  v_pid  uuid;
begin
  -- Take a lock so two sign ups at the same moment cannot both become admin.
  perform pg_advisory_xact_lock(hashtext('motion_first_admin'));

  if not exists (select 1 from public.profiles where role = 'admin') then
    insert into public.profiles (user_id, full_name, email, role, status, joined_on)
    values (new.id, v_name, lower(new.email), 'admin', 'active', current_date);
    return new;
  end if;

  if v_code is not null then
    select i.profile_id into v_pid
    from public.invites i join public.profiles p on p.id = i.profile_id
    where i.code = v_code and p.user_id is null
    for update of p;

    if v_pid is not null then
      update public.profiles set user_id = new.id, email = lower(new.email) where id = v_pid;
      delete from public.invites where profile_id = v_pid;
      return new;
    end if;
  end if;

  insert into public.profiles (user_id, full_name, email, role, status)
  values (new.id, v_name, lower(new.email), 'member', 'pending');
  return new;
end
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- Lets the join page greet an invited person by name. Returns nothing for a wrong code.
create or replace function public.check_invite(p_code text) returns text
language sql stable security definer set search_path = public as $$
  select p.full_name
  from public.invites i join public.profiles p on p.id = i.profile_id
  where i.code = upper(trim(p_code)) and p.user_id is null
$$;

-- ---------------------------------------------------------------- safety triggers

-- Members may edit their own name and phone, never their role, rank, sponsor or status.
create or replace function public.protect_profile() returns trigger
language plpgsql set search_path = public as $$
begin
  if auth.uid() is null or public.is_admin() then
    return new;
  end if;
  if new.role is distinct from old.role
     or new.status is distinct from old.status
     or new.sponsor_id is distinct from old.sponsor_id
     or new.rank is distinct from old.rank
     or new.user_id is distinct from old.user_id
     or new.joined_on is distinct from old.joined_on
     or new.id is distinct from old.id then
    raise exception 'Only the team leader can change this.';
  end if;
  return new;
end
$$;

drop trigger if exists protect_profile on public.profiles;
create trigger protect_profile
  before update on public.profiles
  for each row execute function public.protect_profile();

-- Nobody can end up under their own downline.
create or replace function public.prevent_sponsor_loop() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if new.sponsor_id is not null and (new.sponsor_id = new.id or public.is_under(new.id, new.sponsor_id)) then
    raise exception 'A member cannot be placed under their own downline.';
  end if;
  return new;
end
$$;

drop trigger if exists prevent_sponsor_loop on public.profiles;
create trigger prevent_sponsor_loop
  before insert or update of sponsor_id on public.profiles
  for each row execute function public.prevent_sponsor_loop();

-- There must always be at least one admin.
create or replace function public.keep_one_admin() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if old.role = 'admin' and old.status = 'active'
     and (tg_op = 'DELETE' or new.role <> 'admin' or new.status <> 'active')
     and not exists (
       select 1 from public.profiles
       where role = 'admin' and status = 'active' and id <> old.id
     ) then
    raise exception 'The team must keep at least one admin.';
  end if;
  if tg_op = 'DELETE' then return old; end if;
  return new;
end
$$;

drop trigger if exists keep_one_admin on public.profiles;
create trigger keep_one_admin
  before update or delete on public.profiles
  for each row execute function public.keep_one_admin();

create or replace function public.touch_updated_at() returns trigger
language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end
$$;

drop trigger if exists goals_touch on public.goals;
create trigger goals_touch before update on public.goals
  for each row execute function public.touch_updated_at();

drop trigger if exists payment_touch on public.payment_details;
create trigger payment_touch before update on public.payment_details
  for each row execute function public.touch_updated_at();

-- ---------------------------------------------------------------- leaderboard
-- Top 5 for a month. Shows names and % of goal only, never the Naira amounts.

create or replace function public.leaderboard(p_month text)
returns table (member_id uuid, full_name text, pct numeric, pos int)
language sql stable security definer set search_path = public as $$
  select p.id,
         p.full_name,
         case when g.target_amount > 0 then round(100 * e.total / g.target_amount) end,
         (row_number() over (order by e.total desc, p.full_name))::int
  from public.profiles p
  join (
    select x.member_id, sum(x.amount) as total
    from public.earnings x
    where x.status = 'approved' and to_char(x.earned_on, 'YYYY-MM') = p_month
    group by x.member_id
  ) e on e.member_id = p.id
  left join public.goals g on g.member_id = p.id and g.month = p_month
  where p.status = 'active' and public.my_profile_id() is not null
  order by e.total desc, p.full_name
  limit 5
$$;

-- ---------------------------------------------------------------- privacy rules (row level security)

alter table public.profiles           enable row level security;
alter table public.invites            enable row level security;
alter table public.goals              enable row level security;
alter table public.todos              enable row level security;
alter table public.earnings           enable row level security;
alter table public.breakdown_requests enable row level security;
alter table public.payment_details    enable row level security;
alter table public.products           enable row level security;
alter table public.team_settings      enable row level security;

-- profiles
drop policy if exists profiles_select on public.profiles;
create policy profiles_select on public.profiles for select to authenticated
  using (user_id = auth.uid() or public.can_see_member(id) or id = public.my_sponsor_id());

drop policy if exists profiles_insert on public.profiles;
create policy profiles_insert on public.profiles for insert to authenticated
  with check (
    public.is_admin()
    or (status = 'pending' and role = 'member' and user_id is null and sponsor_id = public.my_profile_id())
  );

drop policy if exists profiles_update on public.profiles;
create policy profiles_update on public.profiles for update to authenticated
  using (public.is_admin() or user_id = auth.uid())
  with check (public.is_admin() or user_id = auth.uid());

drop policy if exists profiles_delete on public.profiles;
create policy profiles_delete on public.profiles for delete to authenticated
  using (public.is_admin());

-- invites: admin only
drop policy if exists invites_admin on public.invites;
create policy invites_admin on public.invites for all to authenticated
  using (public.is_admin()) with check (public.is_admin());

-- goals: members set their own unless the admin locked it
drop policy if exists goals_select on public.goals;
create policy goals_select on public.goals for select to authenticated
  using (public.can_see_member(member_id));

drop policy if exists goals_insert on public.goals;
create policy goals_insert on public.goals for insert to authenticated
  with check (public.is_admin() or (member_id = public.my_profile_id() and locked = false));

drop policy if exists goals_update on public.goals;
create policy goals_update on public.goals for update to authenticated
  using (public.is_admin() or (member_id = public.my_profile_id() and locked = false))
  with check (public.is_admin() or (member_id = public.my_profile_id() and locked = false));

drop policy if exists goals_delete on public.goals;
create policy goals_delete on public.goals for delete to authenticated
  using (public.is_admin());

-- todos: private to the member, admin can read
drop policy if exists todos_select on public.todos;
create policy todos_select on public.todos for select to authenticated
  using (public.is_me_or_admin(member_id));

drop policy if exists todos_insert on public.todos;
create policy todos_insert on public.todos for insert to authenticated
  with check (member_id = public.my_profile_id());

drop policy if exists todos_update on public.todos;
create policy todos_update on public.todos for update to authenticated
  using (member_id = public.my_profile_id())
  with check (member_id = public.my_profile_id());

drop policy if exists todos_delete on public.todos;
create policy todos_delete on public.todos for delete to authenticated
  using (member_id = public.my_profile_id());

-- earnings: members report, only the admin approves or rejects
drop policy if exists earnings_select on public.earnings;
create policy earnings_select on public.earnings for select to authenticated
  using (public.can_see_member(member_id));

drop policy if exists earnings_insert on public.earnings;
create policy earnings_insert on public.earnings for insert to authenticated
  with check (
    public.is_admin()
    or (member_id = public.my_profile_id() and status = 'pending' and reviewed_at is null and reject_reason is null)
  );

drop policy if exists earnings_update on public.earnings;
create policy earnings_update on public.earnings for update to authenticated
  using (public.is_admin())
  with check (public.is_admin());

drop policy if exists earnings_delete on public.earnings;
create policy earnings_delete on public.earnings for delete to authenticated
  using (public.is_admin() or (member_id = public.my_profile_id() and status = 'pending'));

-- breakdown requests: members ask, only the admin answers
drop policy if exists breakdown_select on public.breakdown_requests;
create policy breakdown_select on public.breakdown_requests for select to authenticated
  using (public.is_me_or_admin(member_id));

drop policy if exists breakdown_insert on public.breakdown_requests;
create policy breakdown_insert on public.breakdown_requests for insert to authenticated
  with check (
    member_id = public.my_profile_id() and status = 'pending'
    and admin_note is null and amount_sent is null and proof_path is null and resolved_at is null
  );

drop policy if exists breakdown_update on public.breakdown_requests;
create policy breakdown_update on public.breakdown_requests for update to authenticated
  using (public.is_admin()) with check (public.is_admin());

drop policy if exists breakdown_delete on public.breakdown_requests;
create policy breakdown_delete on public.breakdown_requests for delete to authenticated
  using (public.is_admin() or (member_id = public.my_profile_id() and status = 'pending'));

-- bank details: only the member and the admin
drop policy if exists payment_select on public.payment_details;
create policy payment_select on public.payment_details for select to authenticated
  using (public.is_me_or_admin(member_id));

drop policy if exists payment_insert on public.payment_details;
create policy payment_insert on public.payment_details for insert to authenticated
  with check (member_id = public.my_profile_id());

drop policy if exists payment_update on public.payment_details;
create policy payment_update on public.payment_details for update to authenticated
  using (member_id = public.my_profile_id())
  with check (member_id = public.my_profile_id());

drop policy if exists payment_delete on public.payment_details;
create policy payment_delete on public.payment_details for delete to authenticated
  using (public.is_me_or_admin(member_id));

-- products and settings: every active member reads, the admin edits
drop policy if exists products_select on public.products;
create policy products_select on public.products for select to authenticated
  using (public.my_profile_id() is not null);

drop policy if exists products_write on public.products;
create policy products_write on public.products for all to authenticated
  using (public.is_admin()) with check (public.is_admin());

drop policy if exists settings_select on public.team_settings;
create policy settings_select on public.team_settings for select to authenticated
  using (true);

drop policy if exists settings_write on public.team_settings;
create policy settings_write on public.team_settings for update to authenticated
  using (public.is_admin()) with check (public.is_admin());

-- ---------------------------------------------------------------- access grants

revoke all on all tables in schema public from anon;
grant select, insert, update, delete on
  public.profiles, public.invites, public.goals, public.todos, public.earnings,
  public.breakdown_requests, public.payment_details, public.products
  to authenticated;
grant select, update on public.team_settings to authenticated;

revoke execute on all functions in schema public from public, anon;
grant execute on function
  public.my_profile_id(), public.is_admin(), public.is_under(uuid, uuid),
  public.can_see_member(uuid), public.is_me_or_admin(uuid), public.my_sponsor_id(),
  public.leaderboard(text)
  to authenticated;
grant execute on function public.check_invite(text) to anon, authenticated;

-- ---------------------------------------------------------------- screenshots (storage)
-- One private bucket. Each member has a folder named after their login id.
-- A member reads and writes only their own folder. The admin reads and writes all.

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('proofs', 'proofs', false, 5242880, array['image/jpeg', 'image/png', 'image/webp'])
on conflict (id) do update
  set public = false, file_size_limit = excluded.file_size_limit, allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists proofs_select on storage.objects;
create policy proofs_select on storage.objects for select to authenticated
  using (bucket_id = 'proofs' and ((storage.foldername(name))[1] = auth.uid()::text or public.is_admin()));

drop policy if exists proofs_insert on storage.objects;
create policy proofs_insert on storage.objects for insert to authenticated
  with check (
    bucket_id = 'proofs'
    and (
      public.is_admin()
      or ((storage.foldername(name))[1] = auth.uid()::text and public.my_profile_id() is not null)
    )
  );

drop policy if exists proofs_delete on storage.objects;
create policy proofs_delete on storage.objects for delete to authenticated
  using (bucket_id = 'proofs' and public.is_admin());
