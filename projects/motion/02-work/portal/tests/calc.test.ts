import { describe, expect, it } from 'vitest'
import { calcSvb, cartTotals, levelFor } from '../src/lib/calc'
import { buildPlan } from '../src/lib/goals'
import { parseProducts } from '../src/pages/Products'
import { childMap, descendants } from '../src/lib/tree'
import type { Profile } from '../src/lib/types'

const leg = (name: string, qpv: number) => ({ name, qpv, bv: qpv }) // BV equal to PV, as the plan's examples assume

describe('Sales Volume Bonus, checked against the NeoLife Compensation Plan', () => {
  it('chart levels (page 5)', () => {
    expect(levelFor(249)).toBeNull()
    expect([250, 500, 1000, 2000, 3000, 4000].map((q) => levelFor(q)!.pct)).toEqual([3, 5, 10, 15, 20, 25])
    expect(levelFor(1999)!.pct).toBe(10)
  })

  it('Senior Manager income example (page 7): total 85.00', () => {
    // You 250, Ben 250, Addie 250, Erick 500 (Erick 250 plus Jennifer 250).
    const r = calcSvb({ ownPv: 250, ownBv: 250, legs: [leg('Ben', 250), leg('Addie', 250), leg('Erick', 500)] })
    expect(r.qpv).toBe(1250)
    expect(r.pct).toBe(10)
    expect(r.legs.map((l) => l.diffPct)).toEqual([7, 7, 5])
    expect(r.legs.map((l) => l.earn)).toEqual([17.5, 17.5, 25])
    expect(r.ownEarn).toBe(25)
    expect(r.total).toBe(85)
  })

  it('alone at 250 PV earns 3% (page 7): 7.50', () => {
    expect(calcSvb({ ownPv: 250, ownBv: 250, legs: [] }).total).toBe(7.5)
  })

  it('Qualified Director example (page 9): 25, 22, 20, 15, 10', () => {
    const r = calcSvb({ ownPv: 100, ownBv: 100, legs: [100, 300, 500, 1000, 2000].map((q, i) => leg('L' + i, q)) })
    expect(r.qpv).toBe(4000)
    expect(r.pct).toBe(25)
    expect(r.legs.map((l) => l.legPct)).toEqual([0, 3, 5, 10, 15])
    expect(r.legs.map((l) => l.diffPct)).toEqual([25, 22, 20, 15, 10])
  })

  it('under 100 personal PV pays nothing', () => {
    const r = calcSvb({ ownPv: 99, ownBv: 99, legs: [leg('A', 2000)] })
    expect(r.eligible).toBe(false)
    expect(r.total).toBe(0)
  })

  it('a Director line leaves your QPV and is not paid as SVB', () => {
    const r = calcSvb({ ownPv: 250, ownBv: 250, legs: [leg('Dir', 4000), leg('A', 250)] })
    expect(r.qpv).toBe(500)
    expect(r.pct).toBe(5)
    expect(r.legs[0].directorLeg).toBe(true)
    expect(r.legs[0].earn).toBe(0)
    expect(r.total).toBe(250 * 0.05 + 250 * 0.02)
  })

  it('never pays a negative gap', () => {
    const r = calcSvb({ ownPv: 100, ownBv: 100, legs: [leg('Big', 3000)] })
    expect(r.pct).toBe(20)
    expect(r.legs[0].diffPct).toBe(0)
  })

  it('next level hint', () => {
    const r = calcSvb({ ownPv: 250, ownBv: 0, legs: [leg('A', 500)] })
    expect(r.next!.qpv).toBe(1000)
    expect(r.toNext).toBe(250)
  })

  it('cart totals', () => {
    const t = cartTotals([
      { pv: 25, bv: 22000, dp: 30000, srp: 36000, qty: 2 },
      { pv: 40, bv: 35000, dp: 47000, srp: 56500, qty: 1 },
      { pv: 10, bv: 1, dp: 1, srp: 1, qty: 0 },
    ])
    expect(t).toEqual({ pv: 90, bv: 79000, cost: 107000, retail: 128500, profit: 21500, items: 3 })
  })
})

describe('goal breakdown', () => {
  const e = (d: string, amount: number) => ({ earned_on: d, amount })

  it('splits November into days and weeks that add back up', () => {
    const p = buildPlan(300000, '2026-11', '2026-11-12', [])
    expect(p.days).toBe(30)
    expect(p.daily).toBe(10000)
    expect(p.weekly).toBe(70000)
    expect(p.weeks.map((w) => [w.startDay, w.endDay])).toEqual([[1, 7], [8, 14], [15, 21], [22, 28], [29, 30]])
    expect(p.weeks.reduce((s, w) => s + w.target, 0)).toBeCloseTo(300000)
    expect(p.weeks.find((w) => w.current)!.index).toBe(2)
  })

  it('catch up amount and state', () => {
    const p = buildPlan(300000, '2026-11', '2026-11-12', [e('2026-11-03', 50000), e('2026-11-09', 20000), e('2026-10-30', 999)])
    expect(p.earned).toBe(70000)
    expect(p.left).toBe(230000)
    expect(p.daysLeft).toBe(19)
    expect(p.catchUp).toBeCloseTo(230000 / 19)
    expect(p.state).toBe('behind') // 11 full days gone, should have 110,000
    expect(p.weeks[0].earned).toBe(50000)
    expect(p.weeks[1].earned).toBe(20000)
    expect(Math.round(p.pacePct)).toBe(40)
  })

  it('on track, hit, upcoming and past months', () => {
    expect(buildPlan(300000, '2026-11', '2026-11-12', [e('2026-11-02', 110000)]).state).toBe('on-track')
    expect(buildPlan(300000, '2026-11', '2026-11-12', [e('2026-11-02', 300000)]).state).toBe('hit')
    const next = buildPlan(310000, '2026-12', '2026-11-12', [])
    expect([next.state, next.daysLeft, next.pacePct]).toEqual(['upcoming', 31, 0])
    const past = buildPlan(100000, '2026-10', '2026-11-12', [e('2026-10-05', 40000)])
    expect([past.state, past.daysLeft, past.catchUp, past.pacePct]).toEqual(['behind', 0, 0, 100])
  })

  it('February in a leap year', () => {
    expect(buildPlan(29000, '2028-02', '2028-02-01', []).daily).toBe(1000)
  })
})

describe('team tree', () => {
  const p = (id: string, sponsor: string | null) => ({ id, sponsor_id: sponsor, full_name: id }) as Profile
  it('finds everyone under a person and survives a loop', () => {
    const list = [p('a', null), p('b', 'a'), p('c', 'b'), p('d', 'a'), p('x', 'y'), p('y', 'x')]
    const map = childMap(list)
    expect(descendants('a', map).map((q) => q.id).sort()).toEqual(['b', 'c', 'd'])
    expect(descendants('c', map)).toEqual([])
    expect(descendants('x', map).map((q) => q.id)).toEqual(['y'])
  })
})

describe('price list paste', () => {
  it('reads tab and comma rows, skips headings and blanks', () => {
    const rows = parseProducts('Name\tCode\tPV\tBV\tDP\tSRP\nAlpha\tA1\t25\t22,000\t₦30,000\t36000\n\nBeta, B2, 12.5, 9000, 12000, 15000\nbad line')
    expect(rows).toEqual([
      { name: 'Alpha', code: 'A1', pv: 25, bv: 22000, dp: 30000, srp: 36000 },
      { name: 'Beta', code: 'B2', pv: 12.5, bv: 9000, dp: 12000, srp: 15000 },
    ])
  })
})
