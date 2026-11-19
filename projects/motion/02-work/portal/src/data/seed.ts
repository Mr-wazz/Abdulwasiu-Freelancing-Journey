import { addDays, isoDate } from '../lib/dates'
import { DEFAULT_SETTINGS } from '../lib/types'
import type { Breakdown, Earning, Goal, Invite, Payment, Product, Profile, Settings, Todo } from '../lib/types'

export interface DemoDb {
  profiles: Profile[]
  goals: Goal[]
  todos: Todo[]
  earnings: Earning[]
  breakdowns: Breakdown[]
  payments: Payment[]
  products: Product[]
  settings: Settings[]
  invites: Invite[]
  files: Record<string, string>
}

/** A small drawn picture that stands in for a payment screenshot. */
export function samplePicture(label: string): string {
  const svg =
    `<svg xmlns="http://www.w3.org/2000/svg" width="360" height="520" viewBox="0 0 360 520">` +
    `<rect width="360" height="520" fill="#eef1f8"/>` +
    `<rect x="24" y="24" width="312" height="472" rx="14" fill="#ffffff" stroke="#c9d1e6"/>` +
    `<circle cx="180" cy="120" r="34" fill="#dcf3ea"/>` +
    `<path d="M164 121l11 11 22-24" fill="none" stroke="#12805c" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>` +
    `<text x="180" y="200" text-anchor="middle" font-family="sans-serif" font-size="18" font-weight="700" fill="#101a33">Sample screenshot</text>` +
    `<text x="180" y="232" text-anchor="middle" font-family="sans-serif" font-size="15" fill="#5b6785">${label}</text>` +
    `<text x="180" y="460" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#5b6785">Demo picture. Not a real payment.</text>` +
    `</svg>`
  return 'data:image/svg+xml;utf8,' + encodeURIComponent(svg)
}

/**
 * Sample team for the demo. Names, amounts, products and rates are made up
 * so the screens can be tried before the real team is added.
 */
export function seed(): DemoDb {
  const today = isoDate()
  const month = today.slice(0, 7)
  const day = Number(today.slice(8, 10))
  const now = new Date().toISOString()
  const date = (d: number) => `${month}-${String(Math.min(Math.max(d, 1), day)).padStart(2, '0')}`

  const people: [string, string, string | null, string, 'admin' | 'member', string][] = [
    // id, name, sponsor, rank, role, joined
    ['p-lead', 'Team Leader', null, 'Senior Manager', 'admin', '2025-03-10'],
    ['p-ada', 'Adaeze Okoro', 'p-lead', 'Manager', 'member', '2025-06-02'],
    ['p-tunde', 'Tunde Bakare', 'p-lead', 'Manager', 'member', '2025-09-15'],
    ['p-ngozi', 'Ngozi Eze', 'p-lead', 'Distributor', 'member', '2026-08-20'],
    ['p-kemi', 'Kemi Adebayo', 'p-ada', 'Distributor', 'member', '2026-08-11'],
    ['p-chidi', 'Chidi Nwosu', 'p-ada', 'Distributor', 'member', '2026-09-03'],
    ['p-bola', 'Bola Ojo', 'p-tunde', 'Distributor', 'member', '2026-09-22'],
    ['p-fatima', 'Fatima Bello', 'p-tunde', 'Distributor', 'member', '2026-10-05'],
    ['p-sola', 'Sola Akin', 'p-kemi', 'Distributor', 'member', '2026-10-18'],
    ['p-emeka', 'Emeka Obi', 'p-lead', 'Distributor', 'member', '2026-11-01'],
  ]

  const profiles: Profile[] = people.map(([id, full_name, sponsor_id, rank, role, joined_on]) => ({
    id,
    user_id: 'u-' + id.slice(2),
    full_name,
    email: id.slice(2) + '@example.com',
    phone: '0800 000 00' + String(people.findIndex((p) => p[0] === id)).padStart(2, '0'),
    sponsor_id,
    rank,
    role,
    status: 'active',
    joined_on,
    created_at: now,
  }))
  // One recruit waiting for the leader to approve, added by a member.
  profiles.push({
    id: 'p-new',
    user_id: null,
    full_name: 'Yusuf Lawal',
    email: null,
    phone: '0800 000 0099',
    sponsor_id: 'p-ngozi',
    rank: 'Distributor',
    role: 'member',
    status: 'pending',
    joined_on: today,
    created_at: now,
  })

  const targets: Record<string, number> = {
    'p-lead': 400000,
    'p-ada': 200000,
    'p-tunde': 150000,
    'p-ngozi': 60000,
    'p-kemi': 80000,
    'p-chidi': 50000,
    'p-bola': 50000,
    'p-fatima': 40000,
  }
  const goals: Goal[] = Object.entries(targets).map(([member_id, target_amount]) => ({
    id: 'g-' + member_id,
    member_id,
    month,
    target_amount,
    locked: member_id === 'p-chidi',
    updated_at: now,
  }))

  const files: Record<string, string> = {}
  const earnings: Earning[] = []
  let n = 0
  const earn = (
    member: string,
    amount: number,
    d: number,
    category: string,
    status: Earning['status'] = 'approved',
    reject_reason: string | null = null,
  ) => {
    n++
    const path = `u-${member.slice(2)}/sample-${n}.svg`
    files[path] = samplePicture('₦' + amount.toLocaleString('en-NG'))
    earnings.push({
      id: 'e-' + n,
      member_id: member,
      amount,
      earned_on: date(d),
      category,
      note: null,
      proof_path: path,
      status,
      reject_reason,
      reviewed_at: status === 'pending' ? null : now,
      created_at: now,
    })
  }
  // Share of the monthly goal already earned, so the demo shows every state.
  const pace = day / 30
  earn('p-lead', Math.round(400000 * pace * 1.05), day - 2, 'Sales Volume Bonus')
  earn('p-ada', Math.round(200000 * pace * 0.7), day - 6, 'Retail profit')
  earn('p-ada', Math.round(200000 * pace * 0.45), day - 1, 'Sales Volume Bonus')
  earn('p-tunde', Math.round(150000 * pace * 0.5), day - 4, 'Retail profit')
  earn('p-tunde', 18000, day, 'Retail profit', 'pending')
  earn('p-ngozi', 62000, day - 3, 'Retail profit')
  earn('p-kemi', Math.round(80000 * pace * 0.9), day - 2, 'Retail profit')
  earn('p-kemi', 9500, day, 'Retail profit', 'pending')
  earn('p-chidi', Math.round(50000 * pace * 0.3), day - 5, 'Retail profit')
  earn('p-chidi', 12000, day - 1, 'Retail profit', 'rejected', 'The screenshot is cut off. Please send the full receipt.')
  earn('p-bola', Math.round(50000 * pace), day - 1, 'Retail profit')

  const todos: Todo[] = [
    ['p-ada', 'Follow up with 3 customers', true],
    ['p-ada', 'Post a product on my WhatsApp status', false],
    ['p-ada', 'Check in with my downline', false],
    ['p-lead', 'Review earnings in the inbox', false],
  ].map(([member_id, title, done], i) => ({
    id: 't-' + i,
    member_id: member_id as string,
    due_on: today,
    title: title as string,
    done: done as boolean,
    created_at: now,
  }))

  const payments: Payment[] = [
    { member_id: 'p-ada', bank_name: 'Sample Bank', account_number: '0000000001', account_name: 'Adaeze Okoro', updated_at: now },
    { member_id: 'p-kemi', bank_name: 'Sample Bank', account_number: '0000000002', account_name: 'Kemi Adebayo', updated_at: now },
  ]

  files['u-ada/sample-receipt.svg'] = samplePicture('Transfer sent')
  const breakdowns: Breakdown[] = [
    {
      id: 'b-1',
      member_id: 'p-kemi',
      month,
      note: 'Please send my breakdown for this month so far.',
      status: 'pending',
      admin_note: null,
      amount_sent: null,
      proof_path: null,
      created_at: now,
      resolved_at: null,
    },
    {
      id: 'b-2',
      member_id: 'p-ada',
      month: isoDate(new Date(new Date().getFullYear(), new Date().getMonth() - 1, 1)).slice(0, 7),
      note: null,
      status: 'sent',
      admin_note: 'Retail profit 96,000 plus bonus 44,000.',
      amount_sent: 140000,
      proof_path: 'u-ada/sample-receipt.svg',
      created_at: addDays(today, -9) + 'T09:00:00.000Z',
      resolved_at: addDays(today, -8) + 'T09:00:00.000Z',
    },
  ]

  const products: Product[] = [
    ['Sample Product A', 'S-001', 25, 22000, 30000, 36000],
    ['Sample Product B', 'S-002', 40, 35000, 47000, 56500],
    ['Sample Product C', 'S-003', 12, 10500, 14500, 17500],
    ['Sample Product D', 'S-004', 60, 52000, 70000, 84000],
  ].map(([name, code, pv, bv, dp, srp], i) => ({
    id: 'pr-' + i,
    name: name as string,
    code: code as string,
    pv: pv as number,
    bv: bv as number,
    dp: dp as number,
    srp: srp as number,
    active: true,
    created_at: now,
  }))

  return {
    profiles,
    goals,
    todos,
    earnings,
    breakdowns,
    payments,
    products,
    settings: [{ ...DEFAULT_SETTINGS, bv_per_pv: 880 }],
    invites: [],
    files,
  }
}
