import { createClient } from '@supabase/supabase-js'
import type { LeaderRow, Table } from '../lib/types'
import { type Backend, type Match, newId } from './backend'

const BUCKET = 'proofs'

const TABLE_NAME: Record<Table, string> = {
  profiles: 'profiles',
  goals: 'goals',
  todos: 'todos',
  earnings: 'earnings',
  breakdowns: 'breakdown_requests',
  payments: 'payment_details',
  products: 'products',
  settings: 'team_settings',
  invites: 'invites',
}

function fail(error: { message: string } | null): void {
  if (!error) return
  const m = error.message || 'Something went wrong.'
  if (/row-level security|permission denied/i.test(m)) throw new Error('You are not allowed to do that.')
  if (/Failed to fetch|NetworkError/i.test(m)) throw new Error('No internet connection. Check your network and try again.')
  if (/Invalid login credentials/i.test(m)) throw new Error('Wrong email or password.')
  throw new Error(m)
}

export function makeLive(url: string, key: string): Backend {
  const sb = createClient(url, key)

  return {
    mode: 'live',

    async userId() {
      const { data } = await sb.auth.getSession()
      return data.session?.user.id ?? null
    },

    onAuth(cb) {
      const { data } = sb.auth.onAuthStateChange((event) => {
        if (event === 'PASSWORD_RECOVERY') cb('recovery')
        else if (event === 'SIGNED_IN' || event === 'SIGNED_OUT') cb('change')
      })
      return () => data.subscription.unsubscribe()
    },

    async signIn(email, password) {
      const { error } = await sb.auth.signInWithPassword({ email: email.trim(), password })
      fail(error)
    },

    async signUp({ email, password, fullName, inviteCode }) {
      const { data, error } = await sb.auth.signUp({
        email: email.trim(),
        password,
        options: {
          data: { full_name: fullName.trim(), invite_code: (inviteCode ?? '').trim().toUpperCase() },
          emailRedirectTo: window.location.origin + window.location.pathname,
        },
      })
      fail(error)
      return { confirmEmail: !data.session }
    },

    async signOut() {
      const { error } = await sb.auth.signOut()
      fail(error)
    },

    async resetPassword(email) {
      const { error } = await sb.auth.resetPasswordForEmail(email.trim(), {
        redirectTo: window.location.origin + window.location.pathname,
      })
      fail(error)
    },

    async setPassword(password) {
      const { error } = await sb.auth.updateUser({ password })
      fail(error)
    },

    async checkInvite(code) {
      const { data, error } = await sb.rpc('check_invite', { p_code: code.trim().toUpperCase() })
      fail(error)
      return (data as string | null) ?? null
    },

    async list<T>(table: Table) {
      // Supabase returns at most 1,000 rows per request, so read in pages.
      const size = 1000
      const out: T[] = []
      for (let from = 0; ; from += size) {
        const { data, error } = await sb
          .from(TABLE_NAME[table])
          .select('*')
          .range(from, from + size - 1)
        fail(error)
        out.push(...((data ?? []) as T[]))
        if (!data || data.length < size) break
      }
      return out
    },

    async insert<T>(table: Table, row: Partial<T>) {
      const { data, error } = await sb.from(TABLE_NAME[table]).insert(row as Record<string, unknown>).select().single()
      fail(error)
      return data as T
    },

    async update(table: Table, match: Match, patch) {
      const { data, error } = await sb.from(TABLE_NAME[table]).update(patch).match(match).select()
      fail(error)
      if (!data || data.length === 0) throw new Error('This could not be changed. It may be locked or already reviewed.')
    },

    async upsert(table, row, onConflict) {
      const { error } = await sb.from(TABLE_NAME[table]).upsert(row, { onConflict })
      fail(error)
    },

    async remove(table: Table, match: Match) {
      const { error } = await sb.from(TABLE_NAME[table]).delete().match(match)
      fail(error)
    },

    async leaderboard(month) {
      const { data, error } = await sb.rpc('leaderboard', { p_month: month })
      fail(error)
      return ((data ?? []) as LeaderRow[]).map((r) => ({ ...r, pct: r.pct === null ? null : Number(r.pct) }))
    },

    async upload(folderUserId, blob) {
      const path = `${folderUserId}/${newId()}.jpg`
      const { error } = await sb.storage.from(BUCKET).upload(path, blob, { contentType: 'image/jpeg' })
      fail(error)
      return path
    },

    async fileUrl(path) {
      const { data, error } = await sb.storage.from(BUCKET).createSignedUrl(path, 60 * 30)
      fail(error)
      return data!.signedUrl
    },
  }
}
