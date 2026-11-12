import { type FormEvent, useState } from 'react'
import { addDays, dayLabel, monthLabel, naira } from '../lib/dates'
import type { Plan } from '../lib/goals'
import { goalOf, planOf, useStore } from '../store'
import { Field, Icon, MoneyInput, MonthNav, PaceBar, PageHead, Pill, PlanPill, Sheet, useBusy } from '../ui'

/** The big goal card: money earned against the goal, with the pace tick. */
export function GoalHero({ plan, title }: { plan: Plan; title: string }) {
  return (
    <div className="card hero">
      <div className="card-head">
        <span className="label">{title}</span>
        <span className="pill" style={{ background: 'var(--brand-ink)', color: 'var(--brand)' }}>
          {plan.state === 'hit' ? 'Goal hit' : Math.floor(plan.pct) + '%'}
        </span>
      </div>
      <div>
        <div className="big">{naira(plan.earned)}</div>
        <div className="muted">of {naira(plan.target)}</div>
      </div>
      <PaceBar plan={plan} />
      <p className="small muted">
        {plan.state === 'hit'
          ? 'You have reached this goal. Well done.'
          : plan.daysLeft > 0
            ? `${naira(plan.left)} to go. That is ${naira(plan.catchUp)} a day for the ${plan.daysLeft} ${plan.daysLeft === 1 ? 'day' : 'days'} left.`
            : `This month ended ${naira(plan.left)} short.`}
      </p>
    </div>
  )
}

/** To do list for one day, with suggestions the member can tap to add. */
export function TodoList({ date, suggest }: { date: string; suggest?: boolean }) {
  const { data, me, backend, run, today } = useStore()
  const [text, setText] = useState('')
  const [busy, wrap] = useBusy()
  const todos = data.todos.filter((t) => t.member_id === me.id && t.due_on === date).sort((a, b) => a.created_at.localeCompare(b.created_at))
  const plan = planOf(data, me.id, date.slice(0, 7), today)

  const ideas: string[] = []
  if (plan && plan.catchUp > 0 && plan.state !== 'hit') ideas.push(`Earn ${naira(plan.catchUp)} today`)
  ideas.push(...data.settings.todo_suggestions)
  const have = new Set(todos.map((t) => t.title.toLowerCase()))
  const open = ideas.filter((i) => !have.has(i.toLowerCase()))

  const add = (title: string) =>
    wrap(() => run(() => backend.insert('todos', { member_id: me.id, due_on: date, title: title.trim(), done: false })))

  const submit = (e: FormEvent) => {
    e.preventDefault()
    if (!text.trim()) return
    void add(text).then(() => setText(''))
  }

  return (
    <div className="stack">
      {todos.length > 0 ? (
        <div className="list">
          {todos.map((t) => (
            <div key={t.id} className="item">
              <button
                className="check"
                role="checkbox"
                aria-checked={t.done}
                aria-label={t.title}
                onClick={() => run(() => backend.update('todos', { id: t.id }, { done: !t.done }))}
              >
                {t.done && <Icon name="check" />}
              </button>
              <span className={'grow ' + (t.done ? 'done' : '')}>{t.title}</span>
              {suggest && (
                <button className="iconbtn" aria-label={'Remove ' + t.title} onClick={() => run(() => backend.remove('todos', { id: t.id }))}>
                  <Icon name="x" />
                </button>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p className="muted small">Nothing planned for this day yet.</p>
      )}
      {suggest && (
        <>
          {open.length > 0 && (
            <div className="stack" style={{ gap: 6 }}>
              <span className="label">Suggested from your goal. Tap to add</span>
              <div className="chips">
                {open.map((i) => (
                  <button key={i} className="chip add" disabled={busy} onClick={() => void add(i)}>
                    + {i}
                  </button>
                ))}
              </div>
            </div>
          )}
          <form className="row" onSubmit={submit}>
            <input id="todo-new" className="input grow" placeholder="Add your own task" maxLength={200} value={text} onChange={(e) => setText(e.target.value)} />
            <button className="btn primary" disabled={busy || !text.trim()}>
              Add
            </button>
          </form>
        </>
      )}
    </div>
  )
}

export function GoalForm({ memberId, month, onClose }: { memberId: string; month: string; onClose: () => void }) {
  const { data, backend, run, isAdmin, me } = useStore()
  const goal = goalOf(data, memberId, month)
  const [amount, setAmount] = useState(goal?.target_amount ?? 0)
  const [locked, setLocked] = useState(goal?.locked ?? false)
  const [busy, wrap] = useBusy()
  const forOther = memberId !== me.id

  const save = (e: FormEvent) => {
    e.preventDefault()
    void wrap(async () => {
      const row: Record<string, unknown> = { member_id: memberId, month, target_amount: amount }
      if (isAdmin) row.locked = forOther ? locked : false
      if (await run(() => backend.upsert('goals', row, 'member_id,month'), 'Goal saved')) onClose()
    })
  }

  return (
    <Sheet title={`Goal for ${monthLabel(month)}`} onClose={onClose}>
      <form className="stack" onSubmit={save}>
        <Field label="How much to earn this month (₦)" hint={amount > 0 ? `About ${naira((amount / 30) * 7)} a week, or ${naira(amount / 30)} a day.` : 'The portal breaks it into weeks and days.'}>
          <MoneyInput id="goal-amount" value={amount} onChange={setAmount} placeholder="100,000" />
        </Field>
        <div className="chips">
          {[50000, 100000, 200000, 500000].map((n) => (
            <button type="button" key={n} className="chip" aria-pressed={amount === n} onClick={() => setAmount(n)}>
              {naira(n)}
            </button>
          ))}
        </div>
        {isAdmin && forOther && (
          <label className="row">
            <input id="goal-locked" type="checkbox" checked={locked} onChange={(e) => setLocked(e.target.checked)} style={{ width: 20, height: 20 }} />
            <span className="grow">Lock this goal, so the member cannot change it</span>
          </label>
        )}
        <button className="btn primary block" disabled={busy || amount <= 0}>
          Save goal
        </button>
      </form>
    </Sheet>
  )
}

export function WeekTable({ plan }: { plan: Plan }) {
  const mon = monthLabel(plan.month).split(' ')[0].slice(0, 3)
  return (
    <div className="tablewrap">
      <table>
        <thead>
          <tr>
            <th>Week</th>
            <th className="r">Target</th>
            <th className="r">Earned</th>
          </tr>
        </thead>
        <tbody>
          {plan.weeks.map((w) => (
            <tr key={w.index} className={w.current ? 'now' : ''}>
              <td>
                Week {w.index}{' '}
                <span className="muted small">
                  {w.startDay} to {w.endDay} {mon}
                </span>{' '}
                {w.current && <Pill tone="brand">Now</Pill>}
              </td>
              <td className="r">{naira(w.target)}</td>
              <td className="r">{naira(w.earned)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export function Goals() {
  const { data, me, today, isAdmin } = useStore()
  const [month, setMonth] = useState(today.slice(0, 7))
  const [editing, setEditing] = useState(false)
  const [day, setDay] = useState(today)
  const goal = goalOf(data, me.id, month)
  const plan = planOf(data, me.id, month, today)
  const canEdit = isAdmin || !goal?.locked
  const tomorrow = addDays(today, 1)

  return (
    <>
      <PageHead title="Goals" sub="Set your monthly goal. The portal turns it into weeks, days and a to do list.">
        <MonthNav month={month} onChange={setMonth} />
      </PageHead>

      {plan ? (
        <>
          <GoalHero plan={plan} title={`${monthLabel(month)} goal`} />
          <div className="card">
            <div className="card-head">
              <h2>Your goal, broken down</h2>
              <PlanPill plan={plan} />
            </div>
            <div className="stats">
              <div className="stat">
                <span className="label">Each week</span>
                <b>{naira(plan.weekly)}</b>
              </div>
              <div className="stat">
                <span className="label">Each day</span>
                <b>{naira(plan.daily)}</b>
              </div>
            </div>
            <WeekTable plan={plan} />
            <p className="small muted">Only earnings your team leader has approved are counted. The dark tick on the bar shows where you should be today.</p>
            {canEdit ? (
              <button className="btn" onClick={() => setEditing(true)}>
                Change goal
              </button>
            ) : (
              <p className="note">Your team leader set this goal, so it cannot be changed here.</p>
            )}
          </div>
        </>
      ) : (
        <div className="card">
          <h2>No goal for {monthLabel(month)} yet</h2>
          <p className="muted">Choose how much you want to earn. You will get a weekly target, a daily target and task ideas for each day.</p>
          <button className="btn primary" onClick={() => setEditing(true)}>
            <Icon name="target" /> Set my goal
          </button>
        </div>
      )}

      <div className="card">
        <div className="card-head">
          <h2>To do list</h2>
          <div className="chips">
            <button className="chip" aria-pressed={day === today} onClick={() => setDay(today)}>
              Today
            </button>
            <button className="chip" aria-pressed={day === tomorrow} onClick={() => setDay(tomorrow)}>
              Tomorrow
            </button>
          </div>
        </div>
        <p className="small muted">{dayLabel(day)}</p>
        <TodoList date={day} suggest />
      </div>

      {editing && <GoalForm memberId={me.id} month={month} onClose={() => setEditing(false)} />}
    </>
  )
}
