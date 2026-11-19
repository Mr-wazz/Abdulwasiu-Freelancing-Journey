import { buildPlan } from '../lib/goals'
import { isoDate } from '../lib/dates'
import { blobToDataUrl } from '../lib/image'
import { childMap, descendants } from '../lib/tree'
import type { LeaderRow, Profile, Table } from '../lib/types'
import { type AuthEvent, type Backend, type Match, newId } from './backend'
import { type DemoDb, seed } from './seed'

const DB_KEY = 'motion-demo-db-v1'
const USER_KEY = 'motion-demo-user-v1'

// Browser storage can be missing or blocked. Fall back to memory so the demo still runs.
function readStore(key: string): string | null {
  try {
    return localStorage.getItem(key)
  } catch {
    return null
  }
}
function writeStore(key: string, value: string | null): void {
  try {
    if (value === null) localStorage.removeItem(key)
    else localStorage.setItem(key, value)
  } catch {
    /* keep going in memory */
  }
}

const KEY_COL: Partial<Record<Table, string>> = { payments: 'member_id', invites: 'profile_id' }

export function makeDemo(): Backend {
  let db: DemoDb
  try {
    const raw = readStore(DB_KEY)
    db = raw ? (JSON.parse(raw) as DemoDb) : seed()
  } catch {
    db = seed()
  }
  let userId: string | null = readStore(USER_KEY)
  const listeners = new Set<(e: AuthEvent) => void>()
  const save = () => writeStore(DB_KEY, JSON.stringify(db))
  const emit = () => listeners.forEach((l) => l('change'))

  const me = (): Profile | null => db.profiles.find((p) => p.user_id === userId) ?? null
  const rows = (t: Table) => db[t] as unknown as Record<string, unknown>[]

  /** Mirrors the privacy rules of the real database, so the demo shows what each person would see. */
  function visible(table: Table): Record<string, unknown>[] {
    const m = me()
    if (!m) return []
    const all = rows(table)
    if (m.role === 'admin' || table === 'products' || table === 'settings') return all
    if (m.status !== 'active') return table === 'profiles' ? all.filter((r) => r.id === m.id) : []
    const down = new Set(descendants(m.id, childMap(db.profiles)).map((p) => p.id))
    switch (table) {
      case 'profiles':
        return all.filter((r) => r.id === m.id || r.id === m.sponsor_id || down.has(r.id as string))
      case 'goals':
      case 'earnings':
        return all.filter((r) => r.member_id === m.id || down.has(r.member_id as string))
      case 'todos':
      case 'breakdowns':
      case 'payments':
        return all.filter((r) => r.member_id === m.id)
      default:
        return []
    }
  }

  const matches = (r: Record<string, unknown>, match: Match) => Object.entries(match).every(([k, v]) => r[k] === v)

  return {
    mode: 'demo',

    async userId() {
      return userId
    },
    onAuth(cb) {
      listeners.add(cb)
      return () => listeners.delete(cb)
    },
    async signIn() {
      throw new Error('This is the demo. Choose a sample account below.')
    },
    async signUp() {
      throw new Error('This is the demo. Choose a sample account below.')
    },
    async signOut() {
      userId = null
      writeStore(USER_KEY, null)
      emit()
    },
    async resetPassword() {},
    async setPassword() {},
    async checkInvite(code) {
      const inv = db.invites.find((i) => i.code === code.trim().toUpperCase())
      return db.profiles.find((p) => p.id === inv?.profile_id)?.full_name ?? null
    },

    async list<T>(table: Table) {
      return JSON.parse(JSON.stringify(visible(table))) as T[]
    },

    async insert<T>(table: Table, row: Partial<T>) {
      const now = new Date().toISOString()
      const full: Record<string, unknown> = { created_at: now, updated_at: now, ...(row as Record<string, unknown>) }
      if (!KEY_COL[table] && !full.id) full.id = newId()
      rows(table).push(full)
      save()
      return full as T
    },

    async update(table, match, patch) {
      const hit = rows(table).filter((r) => matches(r, match))
      if (hit.length === 0) throw new Error('This could not be changed.')
      hit.forEach((r) => Object.assign(r, patch))
      save()
    },

    async upsert(table, row, onConflict) {
      const cols = onConflict.split(',')
      const existing = rows(table).find((r) => cols.every((c) => r[c] === row[c]))
      const now = new Date().toISOString()
      if (existing) Object.assign(existing, row, { updated_at: now })
      else rows(table).push({ created_at: now, updated_at: now, ...(cols.includes('id') || KEY_COL[table] ? {} : { id: newId() }), ...row })
      save()
    },

    async remove(table, match) {
      const list = rows(table)
      for (let i = list.length - 1; i >= 0; i--) if (matches(list[i], match)) list.splice(i, 1)
      if (table === 'profiles') {
        // Like the real database: removing a member removes their records too.
        const ids = new Set(db.profiles.map((p) => p.id))
        db.goals = db.goals.filter((r) => ids.has(r.member_id))
        db.todos = db.todos.filter((r) => ids.has(r.member_id))
        db.earnings = db.earnings.filter((r) => ids.has(r.member_id))
        db.breakdowns = db.breakdowns.filter((r) => ids.has(r.member_id))
        db.payments = db.payments.filter((r) => ids.has(r.member_id))
        db.invites = db.invites.filter((r) => ids.has(r.profile_id))
      }
      save()
    },

    async leaderboard(month) {
      const today = isoDate()
      const out: (LeaderRow & { total: number })[] = []
      for (const p of db.profiles.filter((x) => x.status === 'active')) {
        const mine = db.earnings.filter((e) => e.member_id === p.id && e.status === 'approved' && e.earned_on.startsWith(month))
        const total = mine.reduce((s, e) => s + e.amount, 0)
        if (total <= 0) continue
        const goal = db.goals.find((g) => g.member_id === p.id && g.month === month)
        const pct = goal && goal.target_amount > 0 ? Math.round((buildPlan(goal.target_amount, month, today, mine).earned / goal.target_amount) * 100) : null
        out.push({ member_id: p.id, full_name: p.full_name, pct, pos: 0, total })
      }
      out.sort((a, b) => b.total - a.total)
      return out.slice(0, 5).map(({ total: _t, ...r }, i) => ({ ...r, pos: i + 1 }))
    },

    async upload(folderUserId, blob) {
      const path = `${folderUserId}/${newId()}.jpg`
      db.files[path] = await blobToDataUrl(blob)
      save()
      return path
    },

    async fileUrl(path) {
      const url = db.files[path]
      if (!url) throw new Error('Picture not found.')
      return url
    },

    demo: {
      accounts() {
        const map = childMap(db.profiles)
        return db.profiles
          .filter((p) => p.user_id && p.status === 'active')
          .map((p) => {
            const down = descendants(p.id, map).length
            return {
              id: p.id,
              name: p.full_name,
              role: p.role === 'admin' ? 'Admin view' : 'Member view',
              note: p.role === 'admin' ? 'Sees the whole team' : down ? `${down} in downline` : 'No downline yet',
            }
          })
      },
      signInAs(profileId) {
        userId = db.profiles.find((p) => p.id === profileId)?.user_id ?? null
        writeStore(USER_KEY, userId)
        emit()
      },
      reset() {
        db = seed()
        save()
        emit()
      },
    },
  }
}
