// NeoLife Sales Volume Bonus (SVB) maths.
// Source: NeoLife Compensation Plan, Africa, March 2026, pages 5, 7 and 9.

export interface SvbLevel {
  qpv: number
  pct: number
  rank: string
}

/** Sales Volume Bonus chart, highest level first. */
export const SVB_CHART: SvbLevel[] = [
  { qpv: 4000, pct: 25, rank: 'Director' },
  { qpv: 3000, pct: 20, rank: 'Executive Manager' },
  { qpv: 2000, pct: 15, rank: 'Executive Manager' },
  { qpv: 1000, pct: 10, rank: 'Senior Manager' },
  { qpv: 500, pct: 5, rank: 'Manager' },
  { qpv: 250, pct: 3, rank: 'Distributor' },
]

export const MIN_PERSONAL_PV = 100
export const DIRECTOR_QPV = 4000

export function levelFor(qpv: number): SvbLevel | null {
  return SVB_CHART.find((l) => qpv >= l.qpv) ?? null
}

export function nextLevel(qpv: number): SvbLevel | null {
  const above = SVB_CHART.filter((l) => l.qpv > qpv)
  return above.length ? above[above.length - 1] : null
}

export interface LegInput {
  name: string
  /** Total PV of this downline and everyone under them. */
  qpv: number
  /** Bonus Volume of the same orders, in Naira. */
  bv: number
}

export interface LegResult extends LegInput {
  /** SVB % this leg earns for itself. */
  legPct: number
  /** Your % minus their %. */
  diffPct: number
  earn: number
  /** 4,000 QPV or more: paid as Leadership Development Bonus, not SVB. */
  directorLeg: boolean
}

export interface SvbResult {
  ownPv: number
  qpv: number
  pct: number
  rank: string | null
  /** False when personal PV is under 100, so no bonus is paid. */
  eligible: boolean
  ownEarn: number
  teamEarn: number
  total: number
  legs: LegResult[]
  next: SvbLevel | null
  toNext: number
}

/**
 * Your SVB = your % on your own Bonus Volume, plus on each directly sponsored
 * leg the difference between your % and the % that leg earns for itself.
 * A leg at 4,000 QPV or more is a Director leg: its volume leaves your QPV and
 * is paid through the Leadership Development Bonus instead.
 */
export function calcSvb(input: { ownPv: number; ownBv: number; legs: LegInput[] }): SvbResult {
  const ownPv = Math.max(0, input.ownPv || 0)
  const ownBv = Math.max(0, input.ownBv || 0)
  const legs = input.legs.map((l) => ({
    ...l,
    qpv: Math.max(0, l.qpv || 0),
    bv: Math.max(0, l.bv || 0),
  }))

  const qpv = ownPv + legs.filter((l) => l.qpv < DIRECTOR_QPV).reduce((s, l) => s + l.qpv, 0)
  const eligible = ownPv >= MIN_PERSONAL_PV
  const level = levelFor(qpv)
  const pct = eligible && level ? level.pct : 0

  const legResults: LegResult[] = legs.map((l) => {
    const directorLeg = l.qpv >= DIRECTOR_QPV
    const legPct = levelFor(l.qpv)?.pct ?? 0
    const diffPct = directorLeg ? 0 : Math.max(0, pct - legPct)
    return { ...l, legPct, diffPct, directorLeg, earn: (diffPct / 100) * l.bv }
  })

  const ownEarn = (pct / 100) * ownBv
  const teamEarn = legResults.reduce((s, l) => s + l.earn, 0)
  const next = nextLevel(qpv)

  return {
    ownPv,
    qpv,
    pct,
    rank: level?.rank ?? null,
    eligible,
    ownEarn,
    teamEarn,
    total: ownEarn + teamEarn,
    legs: legResults,
    next,
    toNext: next ? next.qpv - qpv : 0,
  }
}

export interface CartLine {
  pv: number
  bv: number
  dp: number
  srp: number
  qty: number
}

export function cartTotals(lines: CartLine[]) {
  const t = { pv: 0, bv: 0, cost: 0, retail: 0, profit: 0, items: 0 }
  for (const l of lines) {
    const q = Math.max(0, l.qty || 0)
    t.items += q
    t.pv += l.pv * q
    t.bv += l.bv * q
    t.cost += l.dp * q
    t.retail += l.srp * q
  }
  t.profit = Math.max(0, t.retail - t.cost)
  return t
}
