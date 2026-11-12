import { type FormEvent, useState } from 'react'
import { dayLabel, monthLabel, naira } from '../lib/dates'
import { shrinkImage } from '../lib/image'
import { EARNING_CATEGORIES, type Earning } from '../lib/types'
import { sum, useStore } from '../store'
import { Confirm, Empty, Field, FilePick, Icon, MoneyInput, MonthNav, PageHead, Proof, Sheet, Stat, StatusPill, useBusy } from '../ui'

export function EarningRow({ e, onDelete, who, hideProof }: { e: Earning; onDelete?: () => void; who?: string; hideProof?: boolean }) {
  return (
    <div className="stack" style={{ gap: 8 }}>
      <div className="item">
        {!hideProof && <Proof path={e.proof_path} label={`Proof for ${naira(e.amount)}`} />}
        <span className="grow">
          <span className="title num">{naira(e.amount)}</span>
          <br />
          <span className="small muted">
            {who ? who + ' · ' : ''}
            {e.category} · {dayLabel(e.earned_on)}
          </span>
        </span>
        <StatusPill status={e.status} />
        {onDelete && (
          <button className="iconbtn" aria-label="Delete this report" onClick={onDelete}>
            <Icon name="trash" />
          </button>
        )}
      </div>
      {e.note && <p className="small muted">Note: {e.note}</p>}
      {e.status === 'rejected' && <p className="note bad">Rejected: {e.reject_reason || 'No reason given.'} You can report it again with a clearer screenshot.</p>}
    </div>
  )
}

function ReportForm({ onClose }: { onClose: () => void }) {
  const { backend, me, run, today } = useStore()
  const [amount, setAmount] = useState(0)
  const [date, setDate] = useState(today)
  const [category, setCategory] = useState(EARNING_CATEGORIES[0])
  const [note, setNote] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [busy, wrap] = useBusy()

  const submit = (ev: FormEvent) => {
    ev.preventDefault()
    void wrap(async () => {
      const ok = await run(async () => {
        if (amount <= 0) throw new Error('Enter the amount you earned.')
        if (!file) throw new Error('Add a screenshot as proof.')
        if (date > today) throw new Error('The date cannot be in the future.')
        const small = backend.mode === 'demo' ? await shrinkImage(file, 900, 0.6) : await shrinkImage(file)
        const proof_path = await backend.upload(me.user_id!, small)
        await backend.insert<Earning>('earnings', {
          member_id: me.id,
          amount,
          earned_on: date,
          category,
          note: note.trim() || null,
          proof_path,
          status: 'pending',
        })
      }, 'Sent to your team leader for review')
      if (ok) onClose()
    })
  }

  return (
    <Sheet title="Report an earning" onClose={onClose}>
      <form className="stack" onSubmit={submit}>
        <Field label="Amount earned (₦)">
          <MoneyInput id="earn-amount" value={amount} onChange={setAmount} />
        </Field>
        <div className="grid2">
          <Field label="Date">
            <input id="earn-date" className="input" type="date" max={today} required value={date} onChange={(e) => setDate(e.target.value)} />
          </Field>
          <Field label="Type">
            <select id="earn-category" className="input" value={category} onChange={(e) => setCategory(e.target.value)}>
              {EARNING_CATEGORIES.map((c) => (
                <option key={c}>{c}</option>
              ))}
            </select>
          </Field>
        </div>
        <Field label="Proof (screenshot)" hint="A screenshot of the payment alert, receipt or back office. It is needed for approval.">
          <FilePick id="earn-proof" file={file} onPick={setFile} />
        </Field>
        <Field label="Note (optional)">
          <input id="earn-note" className="input" maxLength={200} value={note} onChange={(e) => setNote(e.target.value)} placeholder="Example: sold 2 products to a customer" />
        </Field>
        <button className="btn primary block" disabled={busy}>
          {busy ? 'Sending' : 'Send for review'}
        </button>
      </form>
    </Sheet>
  )
}

export function Earnings() {
  const { data, me, today, backend, run } = useStore()
  const [month, setMonth] = useState(today.slice(0, 7))
  const [adding, setAdding] = useState(false)
  const [deleting, setDeleting] = useState<Earning | null>(null)
  const list = data.earnings.filter((e) => e.member_id === me.id && e.earned_on.startsWith(month))
  const approved = list.filter((e) => e.status === 'approved')
  const waiting = list.filter((e) => e.status === 'pending')

  return (
    <>
      <PageHead title="Earnings" sub="Report what you earn with a screenshot. It counts toward your goal once approved.">
        <MonthNav month={month} onChange={setMonth} />
      </PageHead>

      <button className="btn primary" onClick={() => setAdding(true)}>
        <Icon name="plus" /> Report earning
      </button>

      <div className="stats">
        <Stat label="Approved" value={naira(sum(approved))} sub={`${approved.length} ${approved.length === 1 ? 'report' : 'reports'}`} />
        <Stat label="Waiting for review" value={naira(sum(waiting))} sub={`${waiting.length} ${waiting.length === 1 ? 'report' : 'reports'}`} />
      </div>

      {list.length === 0 ? (
        <Empty title={`No earnings reported for ${monthLabel(month)}`}>Tap “Report earning” after every sale or bonus, and add the screenshot.</Empty>
      ) : (
        <div className="card">
          <div className="list">
            {list.map((e) => (
              <EarningRow key={e.id} e={e} onDelete={e.status === 'pending' ? () => setDeleting(e) : undefined} />
            ))}
          </div>
        </div>
      )}

      {adding && <ReportForm onClose={() => setAdding(false)} />}
      {deleting && (
        <Confirm
          title="Delete this report?"
          body={`${naira(deleting.amount)} on ${dayLabel(deleting.earned_on)} will be removed. It has not been reviewed yet.`}
          action="Delete"
          danger
          onClose={() => setDeleting(null)}
          onYes={() => {
            const id = deleting.id
            setDeleting(null)
            void run(() => backend.remove('earnings', { id }), 'Report deleted')
          }}
        />
      )}
    </>
  )
}
