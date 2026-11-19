import { createContext, useContext } from 'react'
import type { Backend } from './data/backend'
import { buildPlan, type Plan } from './lib/goals'
import { DEFAULT_SETTINGS } from './lib/types'
import type { Breakdown, Data, Earning, Goal, Invite, Payment, Product, Profile, Settings, Todo } from './lib/types'

export interface Store {
  backend: Backend
  me: Profile
  isAdmin: boolean
  data: Data
  today: string
  route: string
  go(route: string): void
  reload(): Promise<void>
  /** Runs a change, refreshes the data and shows a message. Returns true when it worked. */
  run(fn: () => Promise<unknown>, done?: string): Promise<boolean>
  toast(message: string, tone?: 'ok' | 'bad'): void
}

export const StoreContext = createContext<Store | null>(null)

export function useStore(): Store {
  const s = useContext(StoreContext)
  if (!s) throw new Error('Store is not ready')
  return s
}

export async function loadAll(b: Backend): Promise<Data> {
  const [profiles, goals, todos, earnings, breakdowns, payments, products, settings, invites] = await Promise.all([
    b.list<Profile>('profiles'),
    b.list<Goal>('goals'),
    b.list<Todo>('todos'),
    b.list<Earning>('earnings'),
    b.list<Breakdown>('breakdowns'),
    b.list<Payment>('payments'),
    b.list<Product>('products'),
    b.list<Settings>('settings'),
    b.list<Invite>('invites'),
  ])
  const s = settings[0]
  return {
    profiles,
    goals: goals.map((g) => ({ ...g, target_amount: Number(g.target_amount) })),
    todos,
    earnings: earnings
      .map((e) => ({ ...e, amount: Number(e.amount) }))
      .sort((a, b2) => (a.earned_on === b2.earned_on ? b2.created_at.localeCompare(a.created_at) : b2.earned_on.localeCompare(a.earned_on))),
    breakdowns: breakdowns.sort((a, b2) => b2.created_at.localeCompare(a.created_at)),
    payments,
    products: products
      .map((p) => ({ ...p, pv: Number(p.pv), bv: Number(p.bv), dp: Number(p.dp), srp: Number(p.srp) }))
      .sort((a, b2) => a.name.localeCompare(b2.name)),
    settings: s
      ? {
          ...s,
          bv_per_pv: Number(s.bv_per_pv) || 0,
          todo_suggestions: Array.isArray(s.todo_suggestions) ? s.todo_suggestions : DEFAULT_SETTINGS.todo_suggestions,
        }
      : DEFAULT_SETTINGS,
    invites,
  }
}

// ---------- small look ups used by many screens ----------

export function approvedOf(data: Data, memberId: string, month: string): Earning[] {
  return data.earnings.filter((e) => e.member_id === memberId && e.status === 'approved' && e.earned_on.startsWith(month))
}

export function goalOf(data: Data, memberId: string, month: string): Goal | undefined {
  return data.goals.find((g) => g.member_id === memberId && g.month === month)
}

export function planOf(data: Data, memberId: string, month: string, today: string): Plan | null {
  const goal = goalOf(data, memberId, month)
  if (!goal) return null
  return buildPlan(goal.target_amount, month, today, approvedOf(data, memberId, month))
}

export function sum(list: { amount: number }[]): number {
  return list.reduce((s, e) => s + e.amount, 0)
}

export function nameOf(data: Data, id: string | null): string {
  return data.profiles.find((p) => p.id === id)?.full_name ?? 'Unknown'
}

export function initials(name: string): string {
  const parts = name.trim().split(/\s+/)
  return ((parts[0]?.[0] ?? '') + (parts[1]?.[0] ?? '')).toUpperCase() || '?'
}
