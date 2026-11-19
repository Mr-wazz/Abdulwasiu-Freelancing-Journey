import { daysInMonth } from './dates'

export interface WeekPlan {
  index: number
  startDay: number
  endDay: number
  target: number
  earned: number
  current: boolean
}

export type GoalState = 'hit' | 'on-track' | 'behind' | 'upcoming'

export interface Plan {
  month: string
  target: number
  days: number
  /** Even split of the month. */
  daily: number
  weekly: number
  earned: number
  left: number
  pct: number
  /** Where the bar should be by the end of today, 0 to 100. */
  pacePct: number
  daysLeft: number
  /** What to earn each remaining day to still hit the goal. */
  catchUp: number
  weeks: WeekPlan[]
  state: GoalState
}

/**
 * Breaks a monthly goal into weeks and days.
 * Weeks run 1 to 7, 8 to 14, 15 to 21, 22 to 28, then the last few days.
 */
export function buildPlan(
  target: number,
  month: string,
  todayIso: string,
  approved: { earned_on: string; amount: number }[],
): Plan {
  const days = daysInMonth(month)
  const todayMonth = todayIso.slice(0, 7)
  const dayNow = month < todayMonth ? days : month > todayMonth ? 0 : Number(todayIso.slice(8, 10))
  const inMonth = approved.filter((e) => e.earned_on.slice(0, 7) === month)
  const earned = inMonth.reduce((s, e) => s + Number(e.amount), 0)
  const left = Math.max(0, target - earned)
  const daily = target / days
  const daysLeft = month < todayMonth ? 0 : month > todayMonth ? days : days - dayNow + 1

  const weeks: WeekPlan[] = []
  for (let start = 1, i = 1; start <= days; start += 7, i++) {
    const end = Math.min(days, start + 6)
    const earnedInWeek = inMonth
      .filter((e) => {
        const d = Number(e.earned_on.slice(8, 10))
        return d >= start && d <= end
      })
      .reduce((s, e) => s + Number(e.amount), 0)
    weeks.push({
      index: i,
      startDay: start,
      endDay: end,
      target: daily * (end - start + 1),
      earned: earnedInWeek,
      current: month === todayMonth && dayNow >= start && dayNow <= end,
    })
  }

  let state: GoalState
  if (target > 0 && earned >= target) state = 'hit'
  else if (dayNow === 0) state = 'upcoming'
  else state = earned >= daily * (dayNow - 1) ? 'on-track' : 'behind'

  return {
    month,
    target,
    days,
    daily,
    weekly: daily * 7,
    earned,
    left,
    pct: target > 0 ? Math.min(100, (earned / target) * 100) : 0,
    pacePct: (dayNow / days) * 100,
    daysLeft,
    catchUp: daysLeft > 0 ? left / daysLeft : 0,
    weeks,
    state,
  }
}

export const STATE_LABEL: Record<GoalState, string> = {
  hit: 'Goal hit',
  'on-track': 'On track',
  behind: 'Behind',
  upcoming: 'Not started',
}
