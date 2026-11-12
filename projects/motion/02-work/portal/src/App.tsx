import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import type { Backend } from './data/backend'
import { isoDate } from './lib/dates'
import type { Data } from './lib/types'
import { Auth, NewPassword } from './pages/Auth'
import { Breakdowns } from './pages/Breakdowns'
import { Calculator } from './pages/Calculator'
import { Dashboard } from './pages/Dashboard'
import { Earnings } from './pages/Earnings'
import { Goals } from './pages/Goals'
import { Home } from './pages/Home'
import { Inbox } from './pages/Inbox'
import { Incentives } from './pages/Incentives'
import { Member } from './pages/Member'
import { More, PaymentDetails, ProfilePage, TeamSettings } from './pages/More'
import { Products } from './pages/Products'
import { Team } from './pages/Team'
import { initials, loadAll, type Store, StoreContext } from './store'
import { Icon, Mark } from './ui'

type Phase = 'loading' | 'auth' | 'ready' | 'error'

function readHash(): string {
  try {
    return window.location.hash.replace(/^#/, '') || 'home'
  } catch {
    return 'home'
  }
}

const MEMBER_TABS = [
  ['home', 'Home', 'home'],
  ['goals', 'Goals', 'target'],
  ['earnings', 'Earnings', 'wallet'],
  ['calculator', 'Calculator', 'calc'],
  ['more', 'More', 'more'],
] as const

const ADMIN_TABS = [
  ['home', 'Dashboard', 'chart'],
  ['team', 'Team', 'team'],
  ['inbox', 'Inbox', 'inbox'],
  ['calculator', 'Calculator', 'calc'],
  ['more', 'More', 'more'],
] as const

export function App({ backend }: { backend: Backend }) {
  const [phase, setPhase] = useState<Phase>('loading')
  const [recovering, setRecovering] = useState(false)
  const [data, setData] = useState<Data | null>(null)
  const [uid, setUid] = useState<string | null>(null)
  const [error, setError] = useState('')
  const [route, setRoute] = useState(readHash)
  const [toastState, setToastState] = useState<{ message: string; tone: 'ok' | 'bad' } | null>(null)
  const uidRef = useRef<string | null>(null)
  const toastTimer = useRef<number>()

  const boot = useCallback(async () => {
    try {
      const id = await backend.userId()
      const switched = id !== uidRef.current
      uidRef.current = id
      setUid(id)
      if (!id) {
        setData(null)
        setPhase('auth')
        return
      }
      if (switched) setPhase('loading')
      setData(await loadAll(backend))
      setPhase('ready')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Something went wrong.')
      setPhase('error')
    }
  }, [backend])

  useEffect(() => {
    void boot()
    return backend.onAuth((e) => {
      // Wait a tick: the sign in library must finish its own work first.
      window.setTimeout(async () => {
        if (e === 'recovery') return setRecovering(true)
        const id = await backend.userId()
        if (id && id === uidRef.current && backend.mode === 'live') return
        if (id !== uidRef.current) go('home')
        void boot()
      }, 0)
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [backend, boot])

  useEffect(() => {
    const onHash = () => setRoute(readHash())
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  }, [])

  const go = useCallback((r: string) => {
    setRoute(r)
    try {
      if (window.location.hash !== '#' + r) window.location.hash = r
    } catch {
      /* the screen still changes without the address bar */
    }
    window.scrollTo(0, 0)
  }, [])

  const toast = useCallback((message: string, tone: 'ok' | 'bad' = 'ok') => {
    setToastState({ message, tone })
    window.clearTimeout(toastTimer.current)
    toastTimer.current = window.setTimeout(() => setToastState(null), tone === 'bad' ? 6000 : 3000)
  }, [])

  const reload = useCallback(async () => setData(await loadAll(backend)), [backend])

  const run = useCallback(
    async (fn: () => Promise<unknown>, done?: string) => {
      try {
        await fn()
        await reload()
        if (done) toast(done)
        return true
      } catch (e) {
        toast(e instanceof Error ? e.message : 'Something went wrong.', 'bad')
        return false
      }
    },
    [reload, toast],
  )

  const me = useMemo(() => data?.profiles.find((p) => p.user_id === uid) ?? null, [data, uid])

  const toastEl = toastState && (
    <div className={'toast ' + (toastState.tone === 'bad' ? 'bad' : '')} role="status">
      {toastState.message}
    </div>
  )
  const demoBar = backend.mode === 'demo' && <div className="demo-bar">Demo with sample names and numbers. Nothing here is real.</div>

  if (recovering)
    return (
      <>
        <NewPassword backend={backend} onDone={() => setRecovering(false)} />
        {toastEl}
      </>
    )
  if (phase === 'loading') return <div className="spin" role="status" aria-label="Loading" />
  if (phase === 'error')
    return (
      <div className="auth">
        <div className="auth-box center">
          <h1>The portal could not load</h1>
          <p className="muted">{error}</p>
          <button className="btn primary" onClick={() => void boot()}>
            Try again
          </button>
        </div>
      </div>
    )
  if (phase === 'auth' || !data)
    return (
      <>
        {demoBar}
        <Auth backend={backend} />
      </>
    )

  if (!me || me.status !== 'active') {
    const pending = me?.status === 'pending'
    return (
      <div className="auth">
        <div className="auth-box center">
          <Mark />
          <h1>{pending ? 'Waiting for approval' : !me ? 'No team profile yet' : 'Account switched off'}</h1>
          <p className="muted">
            {pending
              ? 'Your account is created. The team leader needs to approve you before you can come in. Check back soon.'
              : !me
                ? 'Your login works, but it is not linked to a team profile. Ask the team leader for an invite link.'
                : 'The team leader has switched off this account. Contact them if this is a mistake.'}
          </p>
          <button className="btn primary" onClick={() => void boot()}>
            Check again
          </button>
          <button className="btn" onClick={() => void backend.signOut()}>
            Sign out
          </button>
        </div>
      </div>
    )
  }

  const isAdmin = me.role === 'admin'
  const store: Store = { backend, me, isAdmin, data, today: isoDate(), route, go, reload, run, toast }

  const inboxCount = isAdmin
    ? data.earnings.filter((e) => e.status === 'pending').length +
      data.breakdowns.filter((b) => b.status === 'pending').length +
      data.profiles.filter((p) => p.status === 'pending').length
    : 0

  const tabs = isAdmin ? ADMIN_TABS : MEMBER_TABS
  const tabIds: string[] = tabs.map((t) => t[0])
  const activeTab = tabIds.includes(route) ? route : route.startsWith('member-') ? (isAdmin ? 'team' : 'more') : 'more'

  let page
  if (route.startsWith('member-')) page = <Member id={route.slice(7)} />
  else
    switch (route) {
      case 'goals':
        page = <Goals />
        break
      case 'earnings':
        page = <Earnings />
        break
      case 'calculator':
        page = <Calculator />
        break
      case 'team':
        page = <Team />
        break
      case 'inbox':
        page = isAdmin ? <Inbox /> : <Home />
        break
      case 'breakdown':
        page = <Breakdowns />
        break
      case 'payment':
        page = <PaymentDetails />
        break
      case 'products':
        page = <Products />
        break
      case 'team-setup':
        page = isAdmin ? <TeamSettings /> : <Home />
        break
      case 'incentives':
        page = <Incentives />
        break
      case 'profile':
        page = <ProfilePage />
        break
      case 'my-home':
        page = <Home />
        break
      case 'more':
        page = <More />
        break
      default:
        page = isAdmin ? <Dashboard /> : <Home />
    }

  return (
    <StoreContext.Provider value={store}>
      <div className="shell">
        {demoBar}
        <header className="topbar">
          <div className="topbar-in">
            <div className="brand">
              <Mark />
              <span>{data.settings.team_name}</span>
            </div>
            <div className="spacer" />
            {backend.demo && (
              <button className="btn sm" onClick={() => void backend.signOut()}>
                Switch account
              </button>
            )}
            <button className="avatar" style={{ border: 0, cursor: 'pointer' }} aria-label="My profile" onClick={() => go('profile')}>
              {initials(me.full_name)}
            </button>
          </div>
        </header>
        <main className="page" key={route}>
          {page}
        </main>
        <nav className="tabbar" aria-label="Main">
          <div className="tabbar-in">
            {tabs.map(([id, label, icon]) => (
              <button key={id} className="tab" aria-current={activeTab === id ? 'page' : undefined} onClick={() => go(id)}>
                <Icon name={icon} />
                <span>{label}</span>
                {id === 'inbox' && inboxCount > 0 && <span className="badge">{inboxCount}</span>}
              </button>
            ))}
          </div>
        </nav>
        {toastEl}
      </div>
    </StoreContext.Provider>
  )
}
