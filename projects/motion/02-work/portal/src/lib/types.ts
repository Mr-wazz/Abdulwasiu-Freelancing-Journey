export type Role = 'admin' | 'member'
export type MemberStatus = 'pending' | 'active' | 'inactive'

export interface Profile {
  id: string
  user_id: string | null
  full_name: string
  email: string | null
  phone: string | null
  sponsor_id: string | null
  rank: string
  role: Role
  status: MemberStatus
  joined_on: string | null
  created_at: string
}

export interface Goal {
  id: string
  member_id: string
  month: string // YYYY-MM
  target_amount: number
  locked: boolean
  updated_at: string
}

export interface Todo {
  id: string
  member_id: string
  due_on: string // YYYY-MM-DD
  title: string
  done: boolean
  created_at: string
}

export type ReviewStatus = 'pending' | 'approved' | 'rejected'

export interface Earning {
  id: string
  member_id: string
  amount: number
  earned_on: string
  category: string
  note: string | null
  proof_path: string | null
  status: ReviewStatus
  reject_reason: string | null
  reviewed_at: string | null
  created_at: string
}

export interface Breakdown {
  id: string
  member_id: string
  month: string
  note: string | null
  status: 'pending' | 'sent'
  admin_note: string | null
  amount_sent: number | null
  proof_path: string | null
  created_at: string
  resolved_at: string | null
}

export interface Payment {
  member_id: string
  bank_name: string
  account_number: string
  account_name: string
  updated_at: string
}

export interface Product {
  id: string
  name: string
  code: string | null
  pv: number
  bv: number
  dp: number
  srp: number
  active: boolean
  created_at: string
}

export interface Settings {
  id: number
  team_name: string
  bv_per_pv: number
  todo_suggestions: string[]
}

export interface Invite {
  profile_id: string
  code: string
}

export interface LeaderRow {
  member_id: string
  full_name: string
  pct: number | null
  pos: number
}

export interface Data {
  profiles: Profile[]
  goals: Goal[]
  todos: Todo[]
  earnings: Earning[]
  breakdowns: Breakdown[]
  payments: Payment[]
  products: Product[]
  settings: Settings
  invites: Invite[]
}

export type Table =
  | 'profiles'
  | 'goals'
  | 'todos'
  | 'earnings'
  | 'breakdowns'
  | 'payments'
  | 'products'
  | 'settings'
  | 'invites'

export const RANKS = [
  'Distributor',
  'Manager',
  'Senior Manager',
  'Executive Manager',
  'Director',
  'Emerald Director',
  'World Team',
  "President's Team",
]

export const EARNING_CATEGORIES = [
  'Retail profit',
  'Sales Volume Bonus',
  'Leadership bonus',
  'Incentive',
  'Other',
]

export const DEFAULT_SETTINGS: Settings = {
  id: 1,
  team_name: 'Motion',
  bv_per_pv: 0,
  todo_suggestions: [
    'Talk to 5 new people about the products',
    'Follow up with 3 customers',
    'Post a product on my WhatsApp status',
    'Invite 2 people to see the business',
    'Check in with my downline',
    'Report my earnings with a screenshot',
  ],
}
