import { useState } from 'react'
import { dayLabel, monthLabel, naira } from '../lib/dates'
import type { GoalState } from '../lib/goals'
import { childMap, descendants } from '../lib/tree'
import { planOf, sum, useStore } from '../store'
import { Icon, MonthNav, PaceBar, PlanPill, Stat } from '../ui'
import { Leaderboard } from './Home'

type Filter = 'all' | GoalState | 'none'

export function Dashboard() {
  const { data, me, today, go } = useStore()
  const [month, setMonth] = useState(today.slice(0, 7))
  const [filter, setFilter] = useState<Filter>('all')

  const active = data.profiles.filter((p) => p.status !== 'pending')
  const team = active.filter((p) => p.id !== me.id)
  const map = childMap(active)
  const withDown = team.filter((p) => descendants(p.id, map).length > 0).length
  const pendingMembers = data.profiles.filter((p) => p.status === 'pending').length
  const pendingEarnings = data.earnings.filter((e) => e.status === 'pending').length
  const pendingBreakdowns = data.breakdowns.filter((b) => b.status === 'pending').length
  const inbox = pendingMembers + pendingEarnings + pendingBreakdowns

  const rows = active
    .filter((p) => p.status === 'active')
    .map((p) => ({ p, plan: planOf(data, p.id, month, today) }))
    .sort((a, b) => (b.plan?.pct ?? -1) - (a.plan?.pct ?? -1))
  const withGoal = rows.filter((r) => r.plan)
  const count = (s: GoalState) => withGoal.filter((r) => r.plan!.state === s).length
  const teamEarned = sum(data.earnings.filter((e) => e.status === 'approved' && e.earned_on.startsWith(month)))
  const teamTarget = withGoal.reduce((s, r) => s + r.plan!.target, 0)
  const shown = rows.filter((r) => (filter === 'all' ? true : filter === 'none' ? !r.plan : r.plan?.state === filter))

  return (
    <>
      <div className="page-head">
        <div className="stack" style={{ gap: 4 }}>
          <span className="label">{dayLabel(today)}</span>
          <h1>Team dashboard</h1>
        </div>
        <MonthNav month={month} onChange={setMonth} />
      </div>

      {inbox > 0 && (
        <button className="note warn item" onClick={() => go('inbox')}>
          <span className="grow">
            <b>{inbox} waiting for you.</b>{' '}
            {[
              pendingEarnings && `${pendingEarnings} earning${pendingEarnings === 1 ? '' : 's'} to review`,
              pendingBreakdowns && `${pendingBreakdowns} breakdown request${pendingBreakdowns === 1 ? '' : 's'}`,
              pendingMembers && `${pendingMembers} new member${pendingMembers === 1 ? '' : 's'}`,
            ]
              .filter(Boolean)
              .join(', ')}
            .
          </span>
          <span className="chev">
            <Icon name="right" />
          </span>
        </button>
      )}

      <div className="stats">
        <Stat label="Team members" value={team.length} sub="not counting you" onClick={() => go('team')} />
        <Stat label="Have a downline" value={withDown} onClick={() => go('team')} />
        <Stat label="No downline yet" value={team.length - withDown} onClick={() => go('team')} />
      </div>

      <div className="card hero">
        <span className="label">Team earnings approved in {monthLabel(month)}</span>
        <div className="big">{naira(teamEarned)}</div>
        <p className="small muted">
          {teamTarget > 0
            ? `That is ${Math.round((teamEarned / teamTarget) * 100)}% of the ${naira(teamTarget)} the team set as goals.`
            : 'No goals have been set for this month yet.'}
        </p>
      </div>

      <div className="card">
        <div className="card-head">
          <h2>Goals this month</h2>
          <span className="small muted">
            {count('hit')} of {withGoal.length} hit
          </span>
        </div>
        <div className="chips">
          {(
            [
              ['all', `Everyone (${rows.length})`],
              ['behind', `Behind (${count('behind')})`],
              ['on-track', `On track (${count('on-track')})`],
              ['hit', `Goal hit (${count('hit')})`],
              ['none', `No goal (${rows.length - withGoal.length})`],
            ] as [Filter, string][]
          ).map(([id, label]) => (
            <button key={id} className="chip" aria-pressed={filter === id} onClick={() => setFilter(id)}>
              {label}
            </button>
          ))}
        </div>
        {shown.length === 0 ? (
          <p className="muted small">Nobody in this group.</p>
        ) : (
          <div className="list">
            {shown.map(({ p, plan }) => (
              <button key={p.id} className="item" onClick={() => go('member-' + p.id)}>
                <span className="grow stack" style={{ gap: 6 }}>
                  <span className="row">
                    <span className="grow title">
                      {p.full_name}
                      {p.id === me.id ? ' (you)' : ''}
                    </span>
                    <PlanPill plan={plan} />
                  </span>
                  {plan ? (
                    <>
                      <PaceBar plan={plan} thin />
                      <span className="small muted num">
                        {naira(plan.earned)} of {naira(plan.target)}
                      </span>
                    </>
                  ) : (
                    <span className="small muted">Tap to set a goal for them.</span>
                  )}
                </span>
                <span className="chev">
                  <Icon name="right" />
                </span>
              </button>
            ))}
          </div>
        )}
      </div>

      <Leaderboard month={month} />

      <button className="btn" onClick={() => go('my-home')}>
        <Icon name="user" /> Open my own goal and to do list
      </button>
    </>
  )
}
