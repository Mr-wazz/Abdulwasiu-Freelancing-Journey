import { type FormEvent, useEffect, useState } from 'react'
import type { Backend } from '../data/backend'
import { Field, Mark } from '../ui'

function codeFromLink(): string {
  try {
    return (new URLSearchParams(window.location.search).get('code') ?? '').toUpperCase()
  } catch {
    return ''
  }
}

export function Auth({ backend }: { backend: Backend }) {
  const linkCode = codeFromLink()
  const [mode, setMode] = useState<'in' | 'join' | 'forgot'>(linkCode ? 'join' : 'in')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [code, setCode] = useState(linkCode)
  const [invited, setInvited] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [info, setInfo] = useState('')

  useEffect(() => {
    let live = true
    setInvited(null)
    if (code.trim().length === 8)
      backend
        .checkInvite(code)
        .then((name) => {
          if (!live) return
          setInvited(name)
          if (name) setFullName((n) => n || name)
        })
        .catch(() => {})
    return () => {
      live = false
    }
  }, [code, backend])

  if (backend.demo) {
    const accounts = backend.demo.accounts()
    return (
      <div className="auth">
        <div className="auth-box">
          <div className="center stack" style={{ alignItems: 'center' }}>
            <Mark />
            <h1>Motion Team Portal</h1>
            <p className="muted">Choose who to look as. The leader sees the whole team. A member sees only their own space.</p>
          </div>
          <div className="card">
            <div className="list">
              {accounts.map((a) => (
                <button key={a.id} className="item" onClick={() => backend.demo!.signInAs(a.id)}>
                  <span className="grow">
                    <span className="title">{a.name}</span>
                    <br />
                    <span className="small muted">{a.note}</span>
                  </span>
                  <span className={'pill ' + (a.role === 'Admin view' ? 'brand' : '')}>{a.role}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    setInfo('')
    setBusy(true)
    try {
      if (mode === 'in') {
        await backend.signIn(email, password)
      } else if (mode === 'join') {
        if (password.length < 8) throw new Error('Use a password with at least 8 characters.')
        if (code.trim() && code.trim().length !== 8) throw new Error('The invite code has 8 characters. Check the link you were sent.')
        const { confirmEmail } = await backend.signUp({ email, password, fullName, inviteCode: code })
        if (confirmEmail) {
          setInfo('Almost done. Open the email we just sent you and tap the link to confirm. Then come back and sign in.')
          setMode('in')
        }
      } else {
        await backend.resetPassword(email)
        setInfo('If that email has an account, a reset link is on its way. Check your inbox.')
        setMode('in')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth">
      <form className="auth-box" onSubmit={submit}>
        <div className="center stack" style={{ alignItems: 'center' }}>
          <Mark />
          <h1>{mode === 'in' ? 'Sign in to Motion' : mode === 'join' ? 'Join the Motion team' : 'Reset your password'}</h1>
          {mode === 'join' && invited && <p className="note ok">Welcome, {invited}. Create your password to get in.</p>}
        </div>
        {error && (
          <p className="note bad" role="alert">
            {error}
          </p>
        )}
        {info && <p className="note ok">{info}</p>}
        <div className="card">
          {mode === 'join' && (
            <Field label="Full name">
              <input id="auth-name" className="input" required autoComplete="name" value={fullName} onChange={(e) => setFullName(e.target.value)} />
            </Field>
          )}
          <Field label="Email">
            <input id="auth-email" className="input" type="email" required autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          </Field>
          {mode !== 'forgot' && (
            <Field label="Password" hint={mode === 'join' ? 'At least 8 characters.' : undefined}>
              <input
                id="auth-password"
                className="input"
                type="password"
                required
                autoComplete={mode === 'join' ? 'new-password' : 'current-password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </Field>
          )}
          {mode === 'join' && (
            <Field label="Invite code" hint="It is in the link your team leader sent you. No code? You can still join, and the leader will approve you.">
              <input id="auth-code" className="input" maxLength={8} autoCapitalize="characters" value={code} onChange={(e) => setCode(e.target.value.toUpperCase())} />
            </Field>
          )}
          <button className="btn primary block" disabled={busy}>
            {busy ? 'Please wait' : mode === 'in' ? 'Sign in' : mode === 'join' ? 'Create my account' : 'Send reset link'}
          </button>
        </div>
        <div className="row" style={{ justifyContent: 'center' }}>
          {mode !== 'in' && (
            <button type="button" className="btn ghost" onClick={() => setMode('in')}>
              I have an account
            </button>
          )}
          {mode !== 'join' && (
            <button type="button" className="btn ghost" onClick={() => setMode('join')}>
              Join the team
            </button>
          )}
          {mode === 'in' && (
            <button type="button" className="btn ghost" onClick={() => setMode('forgot')}>
              Forgot password
            </button>
          )}
        </div>
      </form>
    </div>
  )
}

export function NewPassword({ backend, onDone }: { backend: Backend; onDone: () => void }) {
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    if (password.length < 8) return setError('Use a password with at least 8 characters.')
    setBusy(true)
    try {
      await backend.setPassword(password)
      onDone()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setBusy(false)
    }
  }
  return (
    <div className="auth">
      <form className="auth-box" onSubmit={submit}>
        <h1 className="center">Choose a new password</h1>
        {error && (
          <p className="note bad" role="alert">
            {error}
          </p>
        )}
        <div className="card">
          <Field label="New password" hint="At least 8 characters.">
            <input id="new-password" className="input" type="password" autoComplete="new-password" required value={password} onChange={(e) => setPassword(e.target.value)} />
          </Field>
          <button className="btn primary block" disabled={busy}>
            Save password
          </button>
        </div>
      </form>
    </div>
  )
}
