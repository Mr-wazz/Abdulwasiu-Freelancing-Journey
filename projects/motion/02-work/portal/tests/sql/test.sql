\set ON_ERROR_STOP on
\set QUIET on
\o /dev/null
set client_min_messages = warning;

-- helpers -------------------------------------------------------------
create or replace function pg_temp.noop() returns void language sql as $$ select $$;

create schema t;
grant usage on schema t to anon, authenticated;
create table t.ids (k text primary key, v uuid);
grant select on t.ids to anon, authenticated;
create function t.id(k text) returns uuid language sql stable as $$ select v from t.ids where ids.k = $1 $$;
-- Runs a statement and reports whether it was blocked (error, or zero rows changed).
create function t.blocked(q text) returns boolean language plpgsql as $$
declare n bigint;
begin
  execute q;
  get diagnostics n = row_count;
  return n = 0;
exception when others then
  return true;
end $$;
create function t.ok(cond boolean, label text) returns void language plpgsql as $$
begin
  if cond is not true then raise exception 'FAILED: %', label; end if;
  raise notice 'ok  %', label;
end $$;
set client_min_messages = notice;

-- 1. first sign up becomes admin ---------------------------------------
insert into auth.users (email, raw_user_meta_data) values ('Lead@Example.com', '{"full_name":"Lead"}') returning id as lead_uid \gset
insert into t.ids values ('lead_uid', :'lead_uid');
select t.ok((select role = 'admin' and status = 'active' and email = 'lead@example.com' from public.profiles where user_id = :'lead_uid'), 'first user becomes active admin');
insert into t.ids select 'lead', id from public.profiles where user_id = :'lead_uid';

-- 2. admin adds a member and an invite ----------------------------------
begin;
set local role authenticated;
select set_config('request.jwt.claim.sub', :'lead_uid', true) \gset x_
insert into public.profiles (full_name, sponsor_id, status) values ('Bola', t.id('lead'), 'active') returning id as bola \gset
insert into public.invites (profile_id, code) values (:'bola', 'ABCD2345');
commit;
insert into t.ids values ('bola', :'bola');

-- 3. invite check works for anonymous visitors, hides everything else ---
begin;
set local role anon;
select t.ok(public.check_invite('abcd2345') = 'Bola', 'anon can check a valid invite');
select t.ok(public.check_invite('ZZZZ9999') is null, 'wrong invite returns nothing');
select t.ok(t.blocked('select * from public.profiles'), 'anon cannot read profiles');
select t.ok(t.blocked('select * from public.earnings'), 'anon cannot read earnings');
select t.ok(t.blocked('select public.is_admin()'), 'anon cannot call helper functions');
select t.ok(t.blocked('select * from public.leaderboard(''2026-11'')'), 'anon cannot read leaderboard');
rollback;

-- 4. sign up with invite links to the prepared profile -------------------
insert into auth.users (email, raw_user_meta_data) values ('bola@example.com', '{"full_name":"Someone Else","invite_code":"abcd2345"}') returning id as bola_uid \gset
insert into t.ids values ('bola_uid', :'bola_uid');
select t.ok((select user_id = :'bola_uid' and full_name = 'Bola' and status = 'active' and role = 'member' from public.profiles where id = :'bola'), 'invite links login to the prepared profile');
select t.ok(not exists (select 1 from public.invites where profile_id = :'bola'), 'invite is used up');
select t.ok((select count(*) = 2 from public.profiles), 'no extra profile was made');

-- 5. reusing the code, or no code, gives a pending profile ---------------
insert into auth.users (email, raw_user_meta_data) values ('cee@example.com', '{"full_name":"Cee","invite_code":"ABCD2345"}') returning id as cee_uid \gset
insert into t.ids values ('cee_uid', :'cee_uid');
select t.ok((select status = 'pending' and role = 'member' and sponsor_id is null from public.profiles where user_id = :'cee_uid'), 'used or missing code gives a pending profile');
insert into t.ids select 'cee', id from public.profiles where user_id = :'cee_uid';

-- more people: Dayo under Bola, Efe under Lead ---------------------------
insert into auth.users (email) values ('dayo@example.com') returning id as dayo_uid \gset
insert into auth.users (email) values ('efe@example.com') returning id as efe_uid \gset
insert into t.ids values ('dayo_uid', :'dayo_uid'), ('efe_uid', :'efe_uid');
update public.profiles set status = 'active', sponsor_id = :'bola', full_name = 'Dayo' where user_id = :'dayo_uid';
update public.profiles set status = 'active', sponsor_id = t.id('lead'), full_name = 'Efe' where user_id = :'efe_uid';
insert into t.ids select 'dayo', id from public.profiles where user_id = :'dayo_uid';
insert into t.ids select 'efe', id from public.profiles where user_id = :'efe_uid';
insert into public.payment_details values (t.id('dayo'), 'Bank', '0123456789', 'Dayo');
insert into public.payment_details values (t.id('bola'), 'Bank', '1111111111', 'Bola');
insert into public.products (name, pv, bv) values ('Thing', 10, 9000);
insert into public.earnings (member_id, amount, earned_on, status) values
  (t.id('dayo'), 5000, '2026-11-03', 'approved'), (t.id('efe'), 9000, '2026-11-04', 'approved'), (t.id('lead'), 1000, '2026-11-04', 'pending');
insert into public.goals (member_id, month, target_amount) values (t.id('dayo'), '2026-11', 10000), (t.id('efe'), '2026-11', 20000);
insert into public.todos (member_id, due_on, title) values (t.id('dayo'), '2026-11-12', 'Call'), (t.id('bola'), '2026-11-12', 'Post');
insert into public.breakdown_requests (member_id, month) values (t.id('dayo'), '2026-11');

-- 6. pending user sees almost nothing ------------------------------------
begin;
set local role authenticated;
select set_config('request.jwt.claim.sub', :'cee_uid', true) \gset x_
select t.ok((select count(*) = 1 from public.profiles), 'pending user sees only their own profile');
select t.ok((select count(*) = 0 from public.products), 'pending user sees no products');
select t.ok((select count(*) = 0 from public.earnings), 'pending user sees no earnings');
select t.ok(t.blocked(format('insert into public.earnings (member_id, amount, earned_on) values (%L, 5, ''2026-11-01'')', t.id('cee'))), 'pending user cannot report earnings');
select t.ok(t.blocked(format('update public.profiles set status = ''active'' where id = %L', t.id('cee'))), 'pending user cannot approve themselves');
select t.ok(t.blocked(format('update public.profiles set role = ''admin'' where id = %L', t.id('cee'))), 'pending user cannot make themselves admin');
select t.ok((select count(*) = 0 from public.leaderboard('2026-11')), 'pending user gets an empty leaderboard');
rollback;

-- 7. member (Bola) with one downline (Dayo) -------------------------------
begin;
set local role authenticated;
select set_config('request.jwt.claim.sub', :'bola_uid', true) \gset x_
select t.ok((select array_agg(full_name order by full_name) = array['Bola','Dayo','Lead'] from public.profiles), 'member sees self, sponsor and downline only');
select t.ok((select count(*) = 1 and min(member_id::text) = t.id('dayo')::text from public.earnings), 'member sees downline earnings, not a sibling''s or the leader''s');
select t.ok((select count(*) = 1 from public.goals), 'member sees downline goals only');
select t.ok((select count(*) = 1 and min(member_id::text) = t.id('bola')::text from public.payment_details), 'member sees only their own bank details');
select t.ok((select count(*) = 1 and min(member_id::text) = t.id('bola')::text from public.todos), 'member sees only their own to do list');
select t.ok((select count(*) = 0 from public.breakdown_requests), 'member cannot see a downline''s breakdown request');
select t.ok((select count(*) = 0 from public.invites), 'member cannot read invite codes');
select t.ok((select count(*) = 1 from public.products), 'member can read products');
select t.ok(t.blocked('insert into public.products (name) values (''Hack'')'), 'member cannot add products');
select t.ok(t.blocked('update public.team_settings set team_name = ''Hack'''), 'member cannot change team setup');
select t.ok(not t.blocked(format('update public.profiles set phone = ''0801'' where id = %L', t.id('bola'))), 'member can edit own phone');
select t.ok(t.blocked(format('update public.profiles set role = ''admin'' where id = %L', t.id('bola'))), 'member cannot make themselves admin');
select t.ok(t.blocked(format('update public.profiles set rank = ''Director'' where id = %L', t.id('bola'))), 'member cannot change own rank');
select t.ok(t.blocked(format('update public.profiles set sponsor_id = null where id = %L', t.id('bola'))), 'member cannot change own sponsor');
select t.ok(t.blocked(format('update public.profiles set full_name = ''X'' where id = %L', t.id('dayo'))), 'member cannot edit a downline profile');
select t.ok(t.blocked(format('delete from public.profiles where id = %L', t.id('dayo'))), 'member cannot delete members');
select t.ok(not t.blocked(format('insert into public.profiles (full_name, sponsor_id, status) values (''Recruit'', %L, ''pending'')', t.id('bola'))), 'member can add a recruit that waits for approval');
select t.ok(t.blocked(format('insert into public.profiles (full_name, sponsor_id, status) values (''Sneak'', %L, ''active'')', t.id('bola'))), 'member cannot add an already approved recruit');
select t.ok(t.blocked(format('insert into public.profiles (full_name, sponsor_id, status) values (''Sneak'', %L, ''pending'')', t.id('efe'))), 'member cannot add a recruit under someone else');
select t.ok(t.blocked(format('insert into public.profiles (full_name, sponsor_id, status, role) values (''Sneak'', %L, ''pending'', ''admin'')', t.id('bola'))), 'member cannot add an admin');
select t.ok(not t.blocked(format('insert into public.earnings (member_id, amount, earned_on) values (%L, 7000, ''2026-11-05'')', t.id('bola'))), 'member can report an earning');
select t.ok(t.blocked(format('insert into public.earnings (member_id, amount, earned_on, status) values (%L, 7000, ''2026-11-05'', ''approved'')', t.id('bola'))), 'member cannot report an already approved earning');
select t.ok(t.blocked(format('insert into public.earnings (member_id, amount, earned_on) values (%L, 7000, ''2026-11-05'')', t.id('dayo'))), 'member cannot report for someone else');
select t.ok(t.blocked(format('update public.earnings set status = ''approved'' where member_id = %L', t.id('bola'))), 'member cannot approve their own earning');
select t.ok(t.blocked(format('update public.earnings set amount = 1 where member_id = %L', t.id('dayo'))), 'member cannot change a downline earning');
select t.ok(t.blocked(format('delete from public.earnings where member_id = %L', t.id('dayo'))), 'member cannot delete an approved earning of a downline');
select t.ok(not t.blocked(format('delete from public.earnings where member_id = %L and status = ''pending''', t.id('bola'))), 'member can delete own pending earning');
select t.ok(not t.blocked(format('insert into public.goals (member_id, month, target_amount) values (%L, ''2026-11'', 50000) on conflict (member_id, month) do update set target_amount = excluded.target_amount', t.id('bola'))), 'member can set own goal');
select t.ok(not t.blocked(format('insert into public.goals (member_id, month, target_amount) values (%L, ''2026-11'', 60000) on conflict (member_id, month) do update set target_amount = excluded.target_amount', t.id('bola'))), 'member can change own goal');
select t.ok(t.blocked(format('update public.goals set target_amount = 1 where member_id = %L', t.id('dayo'))), 'member cannot change a downline goal');
select t.ok(t.blocked(format('insert into public.goals (member_id, month, target_amount, locked) values (%L, ''2026-12'', 5, true)', t.id('bola'))), 'member cannot lock a goal');
select t.ok(not t.blocked(format('insert into public.breakdown_requests (member_id, month) values (%L, ''2026-11'')', t.id('bola'))), 'member can request a breakdown');
select t.ok(t.blocked(format('insert into public.breakdown_requests (member_id, month, status, amount_sent) values (%L, ''2026-11'', ''sent'', 99)', t.id('bola'))), 'member cannot mark a breakdown as sent');
select t.ok(t.blocked(format('update public.breakdown_requests set status = ''sent'' where member_id = %L', t.id('bola'))), 'member cannot answer own breakdown');
select t.ok(not t.blocked(format('update public.payment_details set bank_name = ''New'' where member_id = %L', t.id('bola'))), 'member can edit own bank details');
select t.ok(t.blocked(format('update public.payment_details set bank_name = ''New'' where member_id = %L', t.id('dayo'))), 'member cannot edit a downline''s bank details');
select t.ok(not t.blocked(format('insert into storage.objects (bucket_id, name) values (''proofs'', %L)', t.id('bola_uid') || '/a.jpg')), 'member can upload to own folder');
select t.ok(t.blocked(format('insert into storage.objects (bucket_id, name) values (''proofs'', %L)', t.id('dayo_uid') || '/a.jpg')), 'member cannot upload to another folder');
select t.ok((select array_agg(full_name order by pos) = array['Efe','Dayo'] and bool_and(pct is not null) from public.leaderboard('2026-11')), 'leaderboard lists approved earners in order');
commit;

-- storage objects from other people, to test reading
insert into storage.objects (bucket_id, name) values ('proofs', t.id('dayo_uid') || '/d.jpg'), ('other', t.id('bola_uid') || '/o.jpg');

begin;
set local role authenticated;
select set_config('request.jwt.claim.sub', :'bola_uid', true) \gset x_
select t.ok((select count(*) = 1 from storage.objects), 'member reads only own screenshots, not a downline''s');
select t.ok(t.blocked('delete from storage.objects'), 'member cannot delete screenshots');
rollback;

-- 8. downline (Dayo) cannot look up the tree -----------------------------
begin;
set local role authenticated;
select set_config('request.jwt.claim.sub', :'dayo_uid', true) \gset x_
select t.ok((select array_agg(full_name order by full_name) = array['Bola','Dayo'] from public.profiles), 'downline sees self and sponsor only');
select t.ok((select count(*) = 1 and min(member_id::text) = t.id('dayo')::text from public.earnings), 'downline cannot see sponsor earnings');
select t.ok((select count(*) = 1 from public.goals), 'downline cannot see sponsor goals');
rollback;

-- 9. admin lock stops the member changing a goal --------------------------
update public.goals set locked = true where member_id = t.id('bola');
begin;
set local role authenticated;
select set_config('request.jwt.claim.sub', :'bola_uid', true) \gset x_
select t.ok(t.blocked(format('update public.goals set target_amount = 1 where member_id = %L', t.id('bola'))), 'member cannot change a locked goal');
select t.ok(t.blocked(format('update public.goals set locked = false where member_id = %L', t.id('bola'))), 'member cannot unlock a goal');
rollback;

-- 10. admin powers and safety triggers ------------------------------------
begin;
set local role authenticated;
select set_config('request.jwt.claim.sub', :'lead_uid', true) \gset x_
select t.ok((select count(*) = 6 from public.profiles), 'admin sees every profile');
select t.ok((select count(*) = 2 from public.payment_details), 'admin sees all bank details');
select t.ok((select count(*) = 2 from storage.objects where bucket_id = 'proofs'), 'admin reads all screenshots');
select t.ok(not t.blocked(format('update public.earnings set status = ''approved'', reviewed_at = now() where member_id = %L', t.id('lead'))), 'admin can approve earnings');
select t.ok(not t.blocked(format('update public.breakdown_requests set status = ''sent'', amount_sent = 100, resolved_at = now() where member_id = %L', t.id('dayo'))), 'admin can answer a breakdown');
select t.ok(not t.blocked(format('insert into storage.objects (bucket_id, name) values (''proofs'', %L)', t.id('dayo_uid') || '/receipt.jpg')), 'admin can put a receipt in a member folder');
select t.ok(not t.blocked(format('update public.goals set target_amount = 70000, locked = true where member_id = %L', t.id('dayo'))), 'admin can set and lock a member goal');
select t.ok(not t.blocked('update public.team_settings set bv_per_pv = 900'), 'admin can change team setup');
select t.ok(not t.blocked(format('update public.profiles set status = ''active'', sponsor_id = %L where id = %L', t.id('efe'), t.id('cee'))), 'admin can approve a pending member');
select t.ok(t.blocked(format('update public.profiles set sponsor_id = %L where id = %L', t.id('dayo'), t.id('bola'))), 'nobody can be placed under their own downline');
select t.ok(t.blocked(format('update public.profiles set sponsor_id = %L where id = %L', t.id('bola'), t.id('bola'))), 'nobody can sponsor themselves');
select t.ok(t.blocked(format('update public.profiles set role = ''member'' where id = %L', t.id('lead'))), 'the last admin cannot be demoted');
select t.ok(t.blocked(format('update public.profiles set status = ''inactive'' where id = %L', t.id('lead'))), 'the last admin cannot be switched off');
select t.ok(t.blocked(format('delete from public.profiles where id = %L', t.id('bola'))), 'a member with a downline cannot be deleted');
select t.ok(not t.blocked(format('delete from public.profiles where id = %L', t.id('dayo'))), 'admin can delete a member with no downline');
select t.ok((select count(*) = 0 from public.earnings where member_id = t.id('dayo')), 'deleting a member removes their earnings');
rollback;

-- 11. switched off member loses access ------------------------------------
update public.profiles set status = 'inactive' where id = t.id('bola');
begin;
set local role authenticated;
select set_config('request.jwt.claim.sub', :'bola_uid', true) \gset x_
select t.ok((select count(*) = 1 from public.profiles), 'switched off member sees only own profile');
select t.ok((select count(*) = 0 from public.earnings), 'switched off member sees no earnings');
select t.ok(t.blocked(format('insert into public.earnings (member_id, amount, earned_on) values (%L, 5, ''2026-11-01'')', t.id('bola'))), 'switched off member cannot report');
rollback;

\echo ALL DATABASE CHECKS PASSED
