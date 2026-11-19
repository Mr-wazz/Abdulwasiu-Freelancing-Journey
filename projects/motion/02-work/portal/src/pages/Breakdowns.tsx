import { type FormEvent, useState } from 'react'
import { addMonths, dayLabel, monthLabel, naira } from '../lib/dates'
import type { Breakdown } from '../lib/types'
import { approvedOf, sum, useStore } from '../store'
import { Confirm, Empty, Field, Icon, PageHead, Proof, Sheet, StatusPill, useBusy } from '../ui'

function RequestForm({ onClose }: { onClose: () => void }) {
  const { backend, me, run, today, data } = useStore()
  const thisM = today.slice(0, 7)
  const months = [thisM, addMonths(thisM, -1), addMonths(thisM, -2)]
  const [month, setMonth] = useState(thisM)
  const [note, setNote] = useState('')
  const [busy, wrap] = useBusy()
  const total = sum(approvedOf(data, me.id, month))
  const already = data.breakdowns.some((b) => b.member_id === me.id && b.month === month && b.status === 'pending')

  const submit = (e: FormEvent) => {
    e.preventDefault()
    void wrap(async () => {
      const ok = await run(
        () => backend.insert<Breakdown>('breakdowns', { member_id: me.id, month, note: note.trim() || null, status: 'pending' }),
        'Request sent to your team leader',
      )
      if (ok) onClose()
    })
  }

  return (
    <Sheet title="Request a breakdown" onClose={onClose}>
      <form className="stack" onSubmit={submit}>
        <Field label="Which month">
          <select id="bd-month" className="input" value={month} onChange={(e) => setMonth(e.target.value)}>
            {months.map((m) => (
              <option key={m} value={m}>
                {monthLabel(m)}
              </option>
            ))}
          </select>
        </Field>
        <p className="note">
          Your approved earnings in {monthLabel(month)}: <b className="num">{naira(total)}</b>
        </p>
        {already && <p className="note warn">You already have a request waiting for this month.</p>}
        <Field label="Message (optional)">
          <textarea id="bd-note" className="input" maxLength={300} value={note} onChange={(e) => setNote(e.target.value)} />
        </Field>
        <button className="btn primary block" disabled={busy || already}>
          Send request
        </button>
      </form>
    </Sheet>
  )
}

export function Breakdowns() {
  const { data, me, go, backend, run } = useStore()
  const [asking, setAsking] = useState(false)
  const [cancel, setCancel] = useState<Breakdown | null>(null)
  const list = data.breakdowns.filter((b) => b.member_id === me.id)
  const bank = data.payments.find((p) => p.member_id === me.id)

  return (
    <>
      <PageHead title="Breakdown" sub="Ask your team leader for the breakdown of a month. They get a notification and reply here." back="more" />

      {bank ? (
        <button className="note item" onClick={() => go('payment')}>
          <span className="grow">
            It will be sent to {bank.bank_name}, account ending {bank.account_number.slice(-4)}. Tap to change.
          </span>
          <span className="chev">
            <Icon name="right" />
          </span>
        </button>
      ) : (
        <button className="note warn item" onClick={() => go('payment')}>
          <span className="grow">Add your bank details first, so your team leader knows where to send it.</span>
          <span className="chev">
            <Icon name="right" />
          </span>
        </button>
      )}

      <button className="btn primary" onClick={() => setAsking(true)}>
        <Icon name="receipt" /> Request a breakdown
      </button>

      {list.length === 0 ? (
        <Empty title="No requests yet">Your requests and the replies will show here.</Empty>
      ) : (
        <div className="card">
          <div className="list">
            {list.map((b) => (
              <div key={b.id} className="stack">
                <div className="item">
                  {b.proof_path && <Proof path={b.proof_path} label="Transfer receipt" />}
                  <span className="grow">
                    <span className="title">{monthLabel(b.month)}</span>
                    <br />
                    <span className="small muted">Asked {dayLabel(b.created_at.slice(0, 10))}</span>
                  </span>
                  <StatusPill status={b.status} />
                  {b.status === 'pending' && (
                    <button className="iconbtn" aria-label="Cancel this request" onClick={() => setCancel(b)}>
                      <Icon name="trash" />
                    </button>
                  )}
                </div>
                {b.status === 'sent' && (
                  <p className="note ok">
                    {b.amount_sent ? (
                      <>
                        <b className="num">{naira(b.amount_sent)}</b> sent
                        {b.resolved_at ? ' on ' + dayLabel(b.resolved_at.slice(0, 10)) : ''}.{' '}
                      </>
                    ) : null}
                    {b.admin_note}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {asking && <RequestForm onClose={() => setAsking(false)} />}
      {cancel && (
        <Confirm
          title="Cancel this request?"
          body={`Your request for ${monthLabel(cancel.month)} will be removed.`}
          action="Cancel request"
          danger
          onClose={() => setCancel(null)}
          onYes={() => {
            const id = cancel.id
            setCancel(null)
            void run(() => backend.remove('breakdowns', { id }), 'Request cancelled')
          }}
        />
      )}
    </>
  )
}
