import { type FormEvent, useState } from 'react'
import { inviteCode } from '../data/backend'
import { dayLabel, monthLabel, naira } from '../lib/dates'
import { childMap, descendants } from '../lib/tree'
import { type Profile, RANKS } from '../lib/types'
import { goalOf, initials, nameOf, planOf, useStore } from '../store'
import { Confirm, CopyButton, Empty, Field, Icon, MonthNav, PaceBar, PageHead, Pill, PlanPill, Sheet, StatusPill, useBusy } from '../ui'
import { EarningRow } from './Earnings'
import { GoalForm } from './Goals'

/** Add a new member, or edit one. Members can add their own recruits, who then wait for approval. */
export function MemberForm({ member, onClose }: { member?: Profile; onClose: () => void }) {
  const { data, me, isAdmin, backend, run, today } = useStore()
  const [fullName, setFullName] = useState(member?.full_name ?? '')
  const [phone, setPhone] = useState(member?.phone ?? '')
  const [email, setEmail] = useState(member?.email ?? '')
  const [sponsor, setSponsor] = useState(member ? (member.sponsor_id ?? '') : me.id)
  const [rank, setRank] = useState(member?.rank ?? RANKS[0])
  const [joined, setJoined] = useState(member?.joined_on ?? today)
  const [busy, wrap] = useBusy()

  // A person cannot be placed under themselves or under their own downline.
  const blocked = new Set<string>(member ? [member.id, ...descendants(member.id, childMap(data.profiles)).map((p) => p.id)] : [])
  const sponsors = data.profiles.filter((p) => p.status !== 'pending' && !blocked.has(p.id)).sort((a, b) => a.full_name.localeCompare(b.full_name))
  const isTop = member?.role === 'admin'

  const save = (e: FormEvent) => {
    e.preventDefault()
    void wrap(async () => {
      const base = {
        full_name: fullName.trim(),
        phone: phone.trim() || null,
        email: email.trim().toLowerCase() || null,
      }
      const ok = member
        ? await run(
            () =>
              backend.update(
                'profiles',
                { id: member.id },
                isAdmin ? { ...base, sponsor_id: sponsor || null, rank, joined_on: joined || null } : base,
              ),
            'Saved',
          )
        : await run(
            () =>
              backend.insert<Profile>('profiles', {
                ...base,
                sponsor_id: isAdmin ? sponsor || null : me.id,
                rank: isAdmin ? rank : RANKS[0],
                role: 'member',
                status: isAdmin ? 'active' : 'pending',
                joined_on: joined || today,
              }),
            isAdmin ? 'Member added' : 'Sent to your team leader for approval',
          )
      if (ok) onClose()
    })
  }

  return (
    <Sheet title={member ? 'Edit member' : 'Add a team member'} onClose={onClose}>
      <form className="stack" onSubmit={save}>
        {!member && !isAdmin && <p className="note">You are adding someone you sponsored. They join your downline once the team leader approves.</p>}
        <Field label="Full name">
          <input id="member-name" className="input" required maxLength={120} value={fullName} onChange={(e) => setFullName(e.target.value)} />
        </Field>
        <div className="grid2">
          <Field label="Phone or WhatsApp">
            <input id="member-phone" className="input" inputMode="tel" value={phone} onChange={(e) => setPhone(e.target.value)} />
          </Field>
          <Field label="Email (optional)">
            <input id="member-email" className="input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          </Field>
        </div>
        {isAdmin && (
          <>
            {!isTop && (
              <Field label="Sponsor" hint="The person who brought them in. This decides whose downline they are in.">
                <select id="member-sponsor" className="input" value={sponsor} onChange={(e) => setSponsor(e.target.value)} required>
                  <option value="">Choose a sponsor</option>
                  {sponsors.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.full_name}
                      {p.id === me.id ? ' (you)' : ''}
                    </option>
                  ))}
                </select>
              </Field>
            )}
            <div className="grid2">
              <Field label="Rank">
                <select id="member-rank" className="input" value={rank} onChange={(e) => setRank(e.target.value)}>
                  {RANKS.map((r) => (
                    <option key={r}>{r}</option>
                  ))}
                </select>
              </Field>
              <Field label="Date joined">
                <input id="member-joined" className="input" type="date" max={today} value={joined} onChange={(e) => setJoined(e.target.value)} />
              </Field>
            </div>
          </>
        )}
        <button className="btn primary block" disabled={busy}>
          {member ? 'Save changes' : isAdmin ? 'Add member' : 'Send for approval'}
        </button>
      </form>
    </Sheet>
  )
}

function InviteCard({ member }: { member: Profile }) {
  const { data, backend, run } = useStore()
  const [busy, wrap] = useBusy()
  const invite = data.invites.find((i) => i.profile_id === member.id)
  const link = invite ? `${window.location.origin}${window.location.pathname}?code=${invite.code}` : ''
  const message = `Hi ${member.full_name.split(' ')[0]}, welcome to ${data.settings.team_name}. Use this link to create your login for our team portal: ${link}`

  return (
    <div className="card">
      <div className="card-head">
        <h2>Login</h2>
        <Pill tone="warn">Not joined yet</Pill>
      </div>
      {invite ? (
        <>
          <p className="small muted">Send this private link to {member.full_name}. It works once, for them only.</p>
          <p className="note num" style={{ overflowWrap: 'anywhere', userSelect: 'all' }}>
            {link}
          </p>
          <div className="row">
            <CopyButton text={link} label="Copy link" />
            <CopyButton text={message} label="Copy WhatsApp message" />
          </div>
        </>
      ) : (
        <>
          <p className="small muted">This member has no login yet. Create an invite link and send it to them on WhatsApp.</p>
          <button
            className="btn primary"
            disabled={busy}
            onClick={() => wrap(() => run(() => backend.upsert('invites', { profile_id: member.id, code: inviteCode() }, 'profile_id'), 'Invite link created'))}
          >
            Create invite link
          </button>
        </>
      )}
    </div>
  )
}

export function Member({ id }: { id: string }) {
  const { data, me, isAdmin, today, go, backend, run } = useStore()
  const [month, setMonth] = useState(today.slice(0, 7))
  const [sheet, setSheet] = useState<'edit' | 'goal' | 'delete' | null>(null)
  const member = data.profiles.find((p) => p.id === id)

  if (!member)
    return (
      <>
        <PageHead title="Member not found" back="team" />
        <Empty title="This member is not in your team view">They may have been removed, or they are not in your downline.</Empty>
      </>
    )

  const map = childMap(data.profiles.filter((p) => p.status !== 'pending'))
  const direct = map.get(member.id) ?? []
  const downline = descendants(member.id, map).length
  const plan = planOf(data, member.id, month, today)
  const goal = goalOf(data, member.id, month)
  const earnings = data.earnings.filter((e) => e.member_id === member.id && e.earned_on.startsWith(month))
  const bank = data.payments.find((p) => p.member_id === member.id)
  const isMe = member.id === me.id
  const canSeeMoney = isAdmin || isMe || earnings.length > 0 || !!plan
  const setStatus = (status: Profile['status'], done: string) => run(() => backend.update('profiles', { id: member.id }, { status }), done)

  return (
    <>
      <PageHead title={member.full_name + (isMe ? ' (you)' : '')} back="team">
        <span className="avatar">{initials(member.full_name)}</span>
      </PageHead>

      <div className="row">
        <Pill tone="brand">{member.rank}</Pill>
        <StatusPill status={member.status} />
        <Pill>{downline > 0 ? `${downline} in downline` : 'No downline'}</Pill>
      </div>

      {member.status === 'pending' && isAdmin && (
        <div className="card">
          <h2>Waiting for your approval</h2>
          <p className="muted small">
            {member.sponsor_id ? `Added under ${nameOf(data, member.sponsor_id)}.` : 'They signed up without an invite link, so they have no sponsor yet. Tap Edit to choose one first.'}
          </p>
          <div className="row">
            <button className="btn primary grow" disabled={!member.sponsor_id} onClick={() => setStatus('active', 'Member approved')}>
              Approve
            </button>
            <button className="btn grow" onClick={() => setSheet('edit')}>
              Edit
            </button>
          </div>
        </div>
      )}

      <div className="card">
        <div className="list">
          <div className="item">
            <span className="grow">
              <span className="label">Sponsor</span>
              <br />
              {member.sponsor_id ? nameOf(data, member.sponsor_id) : 'None (top of the team)'}
            </span>
          </div>
          <div className="item">
            <span className="grow">
              <span className="label">Phone</span>
              <br />
              <span style={{ userSelect: 'all' }}>{member.phone || 'Not added'}</span>
            </span>
            {member.phone && <CopyButton text={member.phone} />}
          </div>
          <div className="item">
            <span className="grow">
              <span className="label">Email</span>
              <br />
              <span style={{ overflowWrap: 'anywhere' }}>{member.email || 'Not added'}</span>
            </span>
          </div>
          <div className="item">
            <span className="grow">
              <span className="label">Joined</span>
              <br />
              {member.joined_on ? dayLabel(member.joined_on) + ' ' + member.joined_on.slice(0, 4) : 'Not set'}
            </span>
          </div>
        </div>
      </div>

      {isAdmin && !member.user_id && member.status !== 'pending' && <InviteCard member={member} />}

      {canSeeMoney && member.status !== 'pending' && (
        <>
          <div className="card">
            <div className="card-head">
              <h2>Goal</h2>
              <MonthNav month={month} onChange={setMonth} />
            </div>
            {plan ? (
              <>
                <div className="row">
                  <span className="grow">
                    <b className="num">{naira(plan.earned)}</b> <span className="muted">of {naira(plan.target)}</span>
                  </span>
                  <PlanPill plan={plan} />
                </div>
                <PaceBar plan={plan} />
                <p className="small muted">
                  {naira(plan.weekly)} a week, {naira(plan.daily)} a day.
                  {plan.state !== 'hit' && plan.daysLeft > 0 && ` Needs ${naira(plan.catchUp)} a day from now.`}
                  {goal?.locked && ' Locked by the team leader.'}
                </p>
              </>
            ) : (
              <p className="muted small">No goal set for {monthLabel(month)}.</p>
            )}
            {isAdmin && (
              <button className="btn" onClick={() => setSheet('goal')}>
                <Icon name="target" /> {plan ? 'Change their goal' : 'Set a goal for them'}
              </button>
            )}
          </div>

          <div className="card">
            <h2>Earnings in {monthLabel(month)}</h2>
            {earnings.length === 0 ? (
              <p className="muted small">Nothing reported this month.</p>
            ) : (
              <div className="list">
                {earnings.map((e) => (
                  <EarningRow key={e.id} e={e} hideProof={!isAdmin && !isMe} />
                ))}
              </div>
            )}
          </div>
        </>
      )}

      {isAdmin && (
        <div className="card">
          <div className="card-head">
            <h2>Bank details</h2>
            <Icon name="bank" />
          </div>
          {bank ? (
            <>
              <p>
                {bank.bank_name}
                <br />
                <b className="num" style={{ userSelect: 'all' }}>
                  {bank.account_number}
                </b>
                <br />
                {bank.account_name}
              </p>
              <CopyButton text={bank.account_number} label="Copy account number" />
            </>
          ) : (
            <p className="muted small">Not added yet. The member adds this from their own account.</p>
          )}
        </div>
      )}

      {direct.length > 0 && (
        <div className="card">
          <h2>People they sponsored</h2>
          <div className="list">
            {direct.map((p) => (
              <button key={p.id} className="item" onClick={() => go('member-' + p.id)}>
                <span className="avatar">{initials(p.full_name)}</span>
                <span className="grow title">{p.full_name}</span>
                <span className="chev">
                  <Icon name="right" />
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      {isAdmin && (
        <div className="row">
          <button className="btn grow" onClick={() => setSheet('edit')}>
            Edit
          </button>
          {!isMe && member.status === 'active' && (
            <button className="btn grow" onClick={() => setStatus('inactive', 'Member switched off')}>
              Switch off
            </button>
          )}
          {!isMe && member.status === 'inactive' && (
            <button className="btn grow" onClick={() => setStatus('active', 'Member switched on')}>
              Switch on
            </button>
          )}
          {!isMe && (
            <button className="btn danger grow" onClick={() => setSheet('delete')}>
              Remove
            </button>
          )}
        </div>
      )}

      {sheet === 'edit' && <MemberForm member={member} onClose={() => setSheet(null)} />}
      {sheet === 'goal' && <GoalForm memberId={member.id} month={month} onClose={() => setSheet(null)} />}
      {sheet === 'delete' &&
        (downline > 0 ? (
          <Sheet title="This member has a downline" onClose={() => setSheet(null)}>
            <p>
              {member.full_name} has {downline} {downline === 1 ? 'person' : 'people'} under them. Move those people to another sponsor first, or use “Switch off” to keep the
              records.
            </p>
            <button className="btn primary" onClick={() => setSheet(null)}>
              OK
            </button>
          </Sheet>
        ) : (
          <Confirm
            title={`Remove ${member.full_name}?`}
            body="Their goals, earnings and requests are deleted for good. To keep the records, use “Switch off” instead."
            action="Remove for good"
            danger
            onClose={() => setSheet(null)}
            onYes={() => {
              setSheet(null)
              void run(() => backend.remove('profiles', { id: member.id }), 'Member removed').then((ok) => ok && go('team'))
            }}
          />
        ))}
    </>
  )
}
