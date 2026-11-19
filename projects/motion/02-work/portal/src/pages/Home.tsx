import { useEffect, useState } from 'react'
import { addDays, dayLabel, firstName, monthLabel, naira } from '../lib/dates'
import { childMap, descendants } from '../lib/tree'
import type { LeaderRow } from '../lib/types'
import { planOf, sum, useStore } from '../store'
import { Icon, Stat } from '../ui'
import { GoalHero, TodoList } from './Goals'

export function Leaderboard({ month }: { month: string }) {
  const { backend, me, data } = useStore()
  const [rows, setRows] = useState<LeaderRow[] | null>(null)
  useEffect(() => {
    let live = true
    backend
      .leaderboard(month)
      .then((r) => live && setRows(r))
      .catch(() => live && setRows([]))
    return () => {
      live = false
    }
    // Refresh when earnings change.
  }, [backend, month, data.earnings])

  return (
    <div className="card">
      <div className="card-head">
        <h2>Top earners in {monthLabel(month).split(' ')[0]}</h2>
        <Icon name="star" />
      </div>
      {rows === null ? (
        <p className="muted small">Loading</p>
      ) : rows.length === 0 ? (
        <p className="muted small">No approved earnings yet this month. Be the first on the board.</p>
      ) : (
        <div className="list">
          {rows.map((r) => (
            <div key={r.member_id} className="item">
              <span className="avatar num">{r.pos}</span>
              <span className="grow title">
                {r.full_name}
                {r.member_id === me.id && ' (you)'}
              </span>
              <span className="muted small num">{r.pct === null ? 'No goal set' : r.pct + '% of goal'}</span>
            </div>
          ))}
        </div>
      )}
      <p className="small muted">The board shows names and progress only. Nobody sees your Naira amounts except you and the team leader.</p>
    </div>
  )
}

export function Home() {
  const { data, me, today, go } = useStore()
  const month = today.slice(0, 7)
  const plan = planOf(data, me.id, month, today)
  const mine = data.earnings.filter((e) => e.member_id === me.id && e.earned_on.startsWith(month))
  const approved = sum(mine.filter((e) => e.status === 'approved'))
  const waiting = mine.filter((e) => e.status === 'pending')
  const rejected = mine.filter((e) => e.status === 'rejected')
  const down = descendants(me.id, childMap(data.profiles)).filter((p) => p.status !== 'pending').length
  const hasBank = data.payments.some((p) => p.member_id === me.id)
  const weekAgo = addDays(today, -7)
  const answered = data.breakdowns.filter((b) => b.member_id === me.id && b.status === 'sent' && (b.resolved_at ?? '').slice(0, 10) >= weekAgo)
  const hour = new Date().getHours()
  const hello = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening'

  return (
    <>
      <div className="page-head">
        <div className="stack" style={{ gap: 4 }}>
          <span className="label">{dayLabel(today)}</span>
          <h1>
            {hello}, {firstName(me.full_name)}
          </h1>
        </div>
      </div>

      {plan ? (
        <GoalHero plan={plan} title={`${monthLabel(month)} goal`} />
      ) : (
        <div className="card">
          <h2>Set your goal for {monthLabel(month)}</h2>
          <p className="muted">Pick a monthly target. You will see what to earn each week and each day.</p>
          <button className="btn primary" onClick={() => go('goals')}>
            <Icon name="target" /> Set my goal
          </button>
        </div>
      )}

      {rejected.length > 0 && (
        <button className="note bad item" onClick={() => go('earnings')}>
          <span className="grow">
            {rejected.length === 1 ? '1 earning was rejected.' : `${rejected.length} earnings were rejected.`} Tap to see why and send it again.
          </span>
          <span className="chev">
            <Icon name="right" />
          </span>
        </button>
      )}

      {answered.length > 0 && (
        <button className="note ok item" onClick={() => go('breakdown')}>
          <span className="grow">Your team leader answered your breakdown request. Tap to see it.</span>
          <span className="chev">
            <Icon name="right" />
          </span>
        </button>
      )}

      <div className="stats">
        <Stat label="Approved this month" value={naira(approved)} onClick={() => go('earnings')} />
        <Stat label="Waiting for review" value={naira(sum(waiting))} sub={waiting.length ? `${waiting.length} to review` : 'Nothing waiting'} onClick={() => go('earnings')} />
        <Stat label="My downline" value={down} sub={down ? 'people under you' : 'No downline yet'} onClick={() => go('team')} />
      </div>

      <div className="card">
        <div className="card-head">
          <h2>Today&apos;s to do list</h2>
          <button className="btn ghost sm" onClick={() => go('goals')}>
            Plan my day
          </button>
        </div>
        <TodoList date={today} />
      </div>

      <div className="row">
        <button className="btn primary grow" onClick={() => go('earnings')}>
          <Icon name="plus" /> Report earning
        </button>
        <button className="btn grow" onClick={() => go('calculator')}>
          <Icon name="calc" /> Bonus calculator
        </button>
      </div>

      {!hasBank && (
        <button className="note item" onClick={() => go('payment')}>
          <span className="grow">Add your bank details so your breakdown can be sent to you directly.</span>
          <span className="chev">
            <Icon name="right" />
          </span>
        </button>
      )}

      <Leaderboard month={month} />
    </>
  )
}
