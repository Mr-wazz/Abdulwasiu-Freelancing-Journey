import type { LeaderRow, Table } from '../lib/types'

export type AuthEvent = 'change' | 'recovery'
export type Match = Record<string, string | number>

export interface DemoAccount {
  id: string
  name: string
  role: string
  note: string
}

/**
 * Everything the screens need from a database. Two versions exist:
 * "live" talks to Supabase, "demo" keeps sample data in this browser only.
 */
export interface Backend {
  mode: 'demo' | 'live'
  userId(): Promise<string | null>
  onAuth(cb: (e: AuthEvent) => void): () => void
  signIn(email: string, password: string): Promise<void>
  signUp(p: { email: string; password: string; fullName: string; inviteCode?: string }): Promise<{ confirmEmail: boolean }>
  signOut(): Promise<void>
  resetPassword(email: string): Promise<void>
  setPassword(password: string): Promise<void>
  /** Returns the invited member's name, or null when the code is not valid. */
  checkInvite(code: string): Promise<string | null>
  list<T>(table: Table): Promise<T[]>
  insert<T>(table: Table, row: Partial<T>): Promise<T>
  update(table: Table, match: Match, patch: Record<string, unknown>): Promise<void>
  upsert(table: Table, row: Record<string, unknown>, onConflict: string): Promise<void>
  remove(table: Table, match: Match): Promise<void>
  leaderboard(month: string): Promise<LeaderRow[]>
  /** Saves a picture in the given member's private folder and returns its path. */
  upload(folderUserId: string, blob: Blob): Promise<string>
  fileUrl(path: string): Promise<string>
  demo?: {
    accounts(): DemoAccount[]
    signInAs(profileId: string): void
    reset(): void
  }
}

export function inviteCode(): string {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  const bytes = new Uint8Array(8)
  crypto.getRandomValues(bytes)
  return Array.from(bytes, (b) => alphabet[b % alphabet.length]).join('')
}

export function newId(): string {
  if (typeof crypto.randomUUID === 'function') return crypto.randomUUID()
  const b = new Uint8Array(16)
  crypto.getRandomValues(b)
  return Array.from(b, (x) => x.toString(16).padStart(2, '0')).join('')
}
