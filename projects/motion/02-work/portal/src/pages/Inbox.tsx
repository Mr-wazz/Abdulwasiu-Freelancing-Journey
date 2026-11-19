import { type FormEvent, useState } from 'react'
import { dayLabel, monthLabel, naira } from '../lib/dates'
import { shrinkImage } from '../lib/image'
import type { Breakdown, Earning, Profile } from '../lib/types'
import { approvedOf, nameOf, sum, useStore } from '../store'
import { Confirm, CopyButton, Empty, Field, FilePick, MoneyInput, PageHead, Pill, Sheet, useBusy } from '../ui'
import { EarningRow } from './Earnings'

function RejectForm({ earning, onClose }: { earning: Earning; onClose: () => void }) {
  const { backend, run, data } = useStore()
  const [reason, setReason] = useState('')
  const [busy, wrap] = useBusy()
  const submit = (e: FormEvent) => {
    e.preventDefault()
    void wrap(async () => {
      const ok = await run(
        () => backend.update('earnings', { id: earning.id }, { status: 'rejected', reject_reason: reason.trim(), reviewed_at: new Date().toISOString() }),
        'Rejected. The member can see your reason.',
      )
      if (ok) onClose()
    })
  }
  return (
    <Sheet title={`Reject ${naira(earning.amount)} from ${nameOf(data, earning.member_id)}?`} onClose={onClose}>
      <form className="stack" onSubmit={submit}>
        <Field label="Reason" hint="The member sees this, so they know what to fix.">
          <textarea id="reject-reason" className="input" required maxLength={300} value={reason} onChange={(e) => setReason(e.target.value)} />
        </Field>
        <div className="chips">
          {['The screenshot is not clear.', 'The amount does not match the screenshot.', 'This was already reported.'].map((r) => (
            <button type="button" key={r} className="chip" onClick={() => setReason(r)}>
              {r}
            </button>
          ))}
        </div>
        <button className="btn danger block" disabled={busy || !reason.trim()}>
          Reject this report
        </button>
      </form>
    </Sheet>
  )
}

function SendForm({ request, member, onClose }: { request: Breakdown; member: Profile | undefined; onClose: () => void }) {
  const { backend, run, data } = useStore()
  const total = sum(approvedOf(data, request.member_id, request.month))
  const [amount, setAmount] = useState(0)
  const [note, setNote] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [busy, wrap] = useBusy()

  const submit = (e: FormEvent) => {
    e.preventDefault()
    void wrap(async () => {
      const ok = await run(async () => {
        let proof_path: string | null = null
        if (file) {
          if (!member?.user_id) throw new Error('This member has no login yet, so a receipt cannot be attached.')
          proof_path = await backend.upload(member.user_id, await shrinkImage(file, backend.mode === 'demo' ? 900 : 1280, backend.mode === 'demo' ? 0.6 : 0.72))
        }
        await backend.update(
          'breakdowns',
          { id: request.id },
          { status: 'sent', amount_sent: amount > 0 ? amount : null, admin_note: note.trim() || null, proof_path, resolved_at: new Date().toISOString() },
        )
      }, 'Marked as sent. The member has been told.')
      if (ok) onClose()
    })
  }

  return (
    <Sheet title={`Breakdown for ${member?.full_name ?? 'member'}`} onClose={onClose}>
      <form className="stack" onSubmit={submit}>
        <p className="note">
          Their approved earnings in {monthLabel(request.month)}: <b className="num">{naira(total)}</b>
        </p>
        <Field label="Breakdown" hint="Write how the amount is made up. The member sees this.">
          <textarea id="send-note" className="input" maxLength={600} value={note} onChange={(e) => setNote(e.target.value)} placeholder="Example: Retail profit 40,000 plus bonus 12,500" />
        </Field>
        <Field label="Amount you sent (₦)" hint="Leave empty if you are only sending the breakdown and no money.">
          <MoneyInput id="send-amount" value={amount} onChange={setAmount} />
        </Field>
        <Field label="Transfer receipt (optional)">
          <FilePick id="send-proof" file={file} onPick={setFile} />
        </Field>
        <button className="btn primary block" disabled={busy || (!note.trim() && amount <= 0)}>
          {busy ? 'Saving' : 'Mark as sent'}
        </button>
      </form>
    </Sheet>
  )
}

export function Inbox() {
  const { data, backend, run, go } = useStore()
  const [rejecting, setRejecting] = useState<Earning | null>(null)
  const [sending, setSending] = useState<Breakdown | null>(null)
  const [removing, setRemoving] = useState<Profile | null>(null)

  const earnings = data.earnings.filter((e) => e.status === 'pending')
  const requests = data.breakdowns.filter((b) => b.status === 'pending')
  const members = data.profiles.filter((p) => p.status === 'pending')
  const byId = new Map(data.profiles.map((p) => [p.id, p]))
  const approve = (e: Earning) =>
    run(() => backend.update('earnings', { id: e.id }, { status: 'approved', reject_reason: null, reviewed_at: new Date().toISOString() }), 'Approved. It now counts toward their goal.')

  return (
    <>
      <PageHead title="Inbox" sub="Everything that needs your decision." />

      {earnings.length + requests.length + members.length === 0 && <Empty title="All clear">Nothing is waiting for you right now.</Empty>}

      {earnings.length > 0 && (
        <div className="card">
          <div className="card-head">
            <h2>Earnings to review</h2>
            <Pill tone="warn">{earnings.length}</Pill>
          </div>
          <p className="small muted">Tap the picture to open the screenshot, then approve or reject.</p>
          <div className="list">
            {earnings.map((e) => (
              <div key={e.id} className="stack">
                <EarningRow e={e} who={nameOf(data, e.member_id)} />
                <div className="row">
                  <button className="btn primary sm grow" onClick={() => approve(e)}>
                    Approve
                  </button>
                  <button className="btn danger sm grow" onClick={() => setRejecting(e)}>
                    Reject
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {requests.length > 0 && (
        <div className="card">
          <div className="card-head">
            <h2>Breakdown requests</h2>
            <Pill tone="warn">{requests.length}</Pill>
          </div>
          <div className="list">
            {requests.map((r) => {
              const bank = data.payments.find((p) => p.member_id === r.member_id)
              return (
                <div key={r.id} className="stack">
                  <div>
                    <span className="title" style={{ fontWeight: 600 }}>
                      {nameOf(data, r.member_id)}
                    </span>
                    <br />
                    <span className="small muted">
                      Wants the breakdown for {monthLabel(r.month)} · asked {dayLabel(r.created_at.slice(0, 10))}
                    </span>
                  </div>
                  {r.note && <p className="small">“{r.note}”</p>}
                  {bank ? (
                    <div className="note row">
                      <span className="grow">
                        {bank.bank_name}
                        <br />
                        <b className="num" style={{ userSelect: 'all' }}>
                          {bank.account_number}
                        </b>
                        <br />
                        {bank.account_name}
                      </span>
                      <CopyButton text={bank.account_number} label="Copy number" />
                    </div>
                  ) : (
                    <p className="note warn">This member has not added bank details yet.</p>
                  )}
                  <button className="btn primary sm" onClick={() => setSending(r)}>
                    Write breakdown and mark as sent
                  </button>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {members.length > 0 && (
        <div className="card">
          <div className="card-head">
            <h2>New members to approve</h2>
            <Pill tone="warn">{members.length}</Pill>
          </div>
          <div className="list">
            {members.map((p) => (
              <div key={p.id} className="stack">
                <div>
                  <span style={{ fontWeight: 600 }}>{p.full_name}</span>
                  <br />
                  <span className="small muted">
                    {p.sponsor_id ? `Added by ${nameOf(data, p.sponsor_id)}` : 'Signed up without an invite link. Choose a sponsor first.'}
                    {p.phone ? ' · ' + p.phone : ''}
                  </span>
                </div>
                <div className="row">
                  {p.sponsor_id ? (
                    <button className="btn primary sm grow" onClick={() => run(() => backend.update('profiles', { id: p.id }, { status: 'active' }), 'Member approved')}>
                      Approve
                    </button>
                  ) : (
                    <button className="btn primary sm grow" onClick={() => go('member-' + p.id)}>
                      Choose sponsor
                    </button>
                  )}
                  <button className="btn sm grow" onClick={() => go('member-' + p.id)}>
                    Open
                  </button>
                  <button className="btn danger sm grow" onClick={() => setRemoving(p)}>
                    Decline
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {rejecting && <RejectForm earning={rejecting} onClose={() => setRejecting(null)} />}
      {sending && <SendForm request={sending} member={byId.get(sending.member_id)} onClose={() => setSending(null)} />}
      {removing && (
        <Confirm
          title={`Decline ${removing.full_name}?`}
          body="They are removed from the waiting list and will not join the team."
          action="Decline"
          danger
          onClose={() => setRemoving(null)}
          onYes={() => {
            const id = removing.id
            setRemoving(null)
            void run(() => backend.remove('profiles', { id }), 'Declined')
          }}
        />
      )}
    </>
  )
}
