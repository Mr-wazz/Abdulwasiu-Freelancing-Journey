import { type FormEvent, useState } from 'react'
import { useStore } from '../store'
import { Confirm, Field, Icon, NumInput, PageHead, Pill, useBusy } from '../ui'

export function More() {
  const { isAdmin, go, data } = useStore()
  const links: [string, string, string, string][] = isAdmin
    ? [
        ['my-home', 'user', 'My own space', 'Your own goal, to do list and progress'],
        ['goals', 'target', 'My goals', 'Set your own monthly goal'],
        ['earnings', 'wallet', 'My earnings', 'Report your own earnings'],
        ['products', 'box', 'Products', `${data.products.length} in the price list. PV, BV and prices`],
        ['incentives', 'star', 'Incentives', 'Who is close to qualifying for NeoLife events'],
        ['team-setup', 'gear', 'Team setup', 'Team name, point value and task ideas'],
        ['profile', 'user', 'My profile', 'Name, phone, password, sign out'],
      ]
    : [
        ['team', 'team', 'My team', 'You and the people under you'],
        ['breakdown', 'receipt', 'Breakdown', 'Ask for the breakdown of a month'],
        ['payment', 'bank', 'Bank details', 'Where your breakdown is sent'],
        ['products', 'box', 'Products', 'PV, BV and prices'],
        ['incentives', 'star', 'Incentives', 'What you need for NeoLife events'],
        ['profile', 'user', 'My profile', 'Name, phone, password, sign out'],
      ]
  return (
    <>
      <PageHead title="More" />
      <div className="card">
        <div className="list">
          {links.map(([route, icon, title, sub]) => (
            <button key={route} className="item" onClick={() => go(route)}>
              <span className="avatar">
                <span style={{ width: 20, height: 20, display: 'grid' }}>
                  <Icon name={icon} />
                </span>
              </span>
              <span className="grow">
                <span className="title">{title}</span>
                <br />
                <span className="small muted">{sub}</span>
              </span>
              <span className="chev">
                <Icon name="right" />
              </span>
            </button>
          ))}
        </div>
      </div>
    </>
  )
}

export function PaymentDetails() {
  const { data, me, backend, run } = useStore()
  const saved = data.payments.find((p) => p.member_id === me.id)
  const [bank, setBank] = useState(saved?.bank_name ?? '')
  const [number, setNumber] = useState(saved?.account_number ?? '')
  const [name, setName] = useState(saved?.account_name ?? me.full_name)
  const [busy, wrap] = useBusy()

  const save = (e: FormEvent) => {
    e.preventDefault()
    void wrap(() =>
      run(async () => {
        if (!/^\d{10}$/.test(number)) throw new Error('A Nigerian account number has 10 digits. Please check it.')
        await backend.upsert('payments', { member_id: me.id, bank_name: bank.trim(), account_number: number, account_name: name.trim() }, 'member_id')
      }, 'Bank details saved'),
    )
  }

  return (
    <>
      <PageHead title="Bank details" sub="Your team leader uses this to send your breakdown. Only you and the team leader can see it." back="more" />
      <form className="card" onSubmit={save}>
        <Field label="Bank name">
          <input id="pay-bank" className="input" required maxLength={80} value={bank} onChange={(e) => setBank(e.target.value)} placeholder="Example: GTBank, Opay, Access" />
        </Field>
        <Field label="Account number" hint="10 digits.">
          <input id="pay-number" className="input num" required inputMode="numeric" maxLength={10} value={number} onChange={(e) => setNumber(e.target.value.replace(/\D/g, ''))} />
        </Field>
        <Field label="Account name" hint="Exactly as the bank shows it.">
          <input id="pay-name" className="input" required maxLength={120} value={name} onChange={(e) => setName(e.target.value)} />
        </Field>
        <button className="btn primary block" disabled={busy}>
          Save bank details
        </button>
      </form>
    </>
  )
}

export function ProfilePage() {
  const { me, backend, run, toast, data } = useStore()
  const [name, setName] = useState(me.full_name)
  const [phone, setPhone] = useState(me.phone ?? '')
  const [password, setPassword] = useState('')
  const [busy, wrap] = useBusy()

  const save = (e: FormEvent) => {
    e.preventDefault()
    void wrap(() => run(() => backend.update('profiles', { id: me.id }, { full_name: name.trim(), phone: phone.trim() || null }), 'Profile saved'))
  }
  const changePassword = (e: FormEvent) => {
    e.preventDefault()
    void wrap(async () => {
      if (password.length < 8) return toast('Use a password with at least 8 characters.', 'bad')
      try {
        await backend.setPassword(password)
        setPassword('')
        toast('Password changed')
      } catch (err) {
        toast(err instanceof Error ? err.message : 'Could not change the password.', 'bad')
      }
    })
  }

  return (
    <>
      <PageHead title="My profile" back="more" />
      <div className="row">
        <Pill tone="brand">{me.rank}</Pill>
        <Pill>{me.role === 'admin' ? 'Team leader' : 'Team member'}</Pill>
        <Pill>{data.settings.team_name}</Pill>
      </div>
      <form className="card" onSubmit={save}>
        <Field label="Full name">
          <input id="prof-name" className="input" required maxLength={120} value={name} onChange={(e) => setName(e.target.value)} />
        </Field>
        <Field label="Phone or WhatsApp">
          <input id="prof-phone" className="input" inputMode="tel" value={phone} onChange={(e) => setPhone(e.target.value)} />
        </Field>
        <Field label="Email">
          <input id="prof-email" className="input" value={me.email ?? ''} disabled />
        </Field>
        <button className="btn primary block" disabled={busy}>
          Save profile
        </button>
      </form>
      {backend.mode === 'live' && (
        <form className="card" onSubmit={changePassword}>
          <h2>Change password</h2>
          <Field label="New password" hint="At least 8 characters.">
            <input id="prof-password" className="input" type="password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </Field>
          <button className="btn block" disabled={busy || !password}>
            Change password
          </button>
        </form>
      )}
      <button className="btn danger" onClick={() => void backend.signOut()}>
        <Icon name="out" /> {backend.demo ? 'Switch account' : 'Sign out'}
      </button>
    </>
  )
}

export function TeamSettings() {
  const { data, backend, run, reload, toast } = useStore()
  const s = data.settings
  const [teamName, setTeamName] = useState(s.team_name)
  const [rate, setRate] = useState(s.bv_per_pv)
  const [ideas, setIdeas] = useState(s.todo_suggestions.join('\n'))
  const [busy, wrap] = useBusy()
  const [resetting, setResetting] = useState(false)

  const save = (e: FormEvent) => {
    e.preventDefault()
    void wrap(() =>
      run(
        () =>
          backend.update(
            'settings',
            { id: 1 },
            {
              team_name: teamName.trim() || 'Motion',
              bv_per_pv: rate,
              todo_suggestions: ideas
                .split('\n')
                .map((x) => x.trim())
                .filter(Boolean)
                .slice(0, 12),
            },
          ),
        'Team setup saved',
      ),
    )
  }

  return (
    <>
      <PageHead title="Team setup" back="more" />
      <form className="card" onSubmit={save}>
        <Field label="Team name">
          <input id="set-name" className="input" required maxLength={40} value={teamName} onChange={(e) => setTeamName(e.target.value)} />
        </Field>
        <Field
          label="Bonus Volume (BV) per 1 PV, in Naira"
          hint="Used by the bonus calculator to turn points into Naira. Take a product from the NeoLife price list and divide its BV by its PV. Use the average of a few products."
        >
          <NumInput id="set-rate" value={rate} onChange={setRate} />
        </Field>
        <Field label="Task ideas for the daily to do list" hint="One per line. Members tap these to add them to their day.">
          <textarea id="set-ideas" className="input" rows={7} value={ideas} onChange={(e) => setIdeas(e.target.value)} />
        </Field>
        <button className="btn primary block" disabled={busy}>
          Save team setup
        </button>
      </form>
      {backend.demo && (
        <div className="card">
          <h2>Demo data</h2>
          <p className="muted small">Put the sample team back the way it started. Only this browser is changed.</p>
          <button className="btn" onClick={() => setResetting(true)}>
            Reset the demo
          </button>
        </div>
      )}
      {resetting && (
        <Confirm
          title="Reset the demo?"
          body="Everything you changed in this demo goes back to the sample data."
          action="Reset"
          onClose={() => setResetting(false)}
          onYes={() => {
            setResetting(false)
            backend.demo!.reset()
            void reload().then(() => toast('Demo reset'))
          }}
        />
      )}
    </>
  )
}
