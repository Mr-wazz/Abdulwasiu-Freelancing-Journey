import { type ReactNode, useEffect, useId, useRef, useState } from 'react'
import { addMonths, monthLabel } from './lib/dates'
import { type Plan, STATE_LABEL } from './lib/goals'
import { useStore } from './store'

// ---------- icons (simple line drawings) ----------
const PATHS: Record<string, string> = {
  home: 'M3 11l9-8 9 8M5 10v10h5v-6h4v6h5V10',
  target: 'M12 21a9 9 0 100-18 9 9 0 000 18zM12 16a4 4 0 100-8 4 4 0 000 8zM12 12h.01',
  wallet: 'M3 7a2 2 0 012-2h13v4M3 7v10a2 2 0 002 2h15V9H5a2 2 0 01-2-2zM16 14h.01',
  calc: 'M6 3h12a1 1 0 011 1v16a1 1 0 01-1 1H6a1 1 0 01-1-1V4a1 1 0 011-1zM8 7h8M8 12h.01M12 12h.01M16 12h.01M8 16h.01M12 16h.01M16 16h.01',
  team: 'M9 11a3.5 3.5 0 100-7 3.5 3.5 0 000 7zM2.5 20a6.5 6.5 0 0113 0M16 4.2a3.5 3.5 0 010 6.6M18 14.5a6.5 6.5 0 013.5 5.5',
  inbox: 'M3 13l3-8h12l3 8M3 13v6h18v-6M3 13h5l1 3h6l1-3h5',
  more: 'M5 12h.01M12 12h.01M19 12h.01',
  chart: 'M4 20V10M10 20V4M16 20v-8M21 20H3',
  plus: 'M12 5v14M5 12h14',
  check: 'M5 12.5l4.5 4.5L19 7.5',
  x: 'M6 6l12 12M18 6L6 18',
  left: 'M15 5l-7 7 7 7',
  right: 'M9 5l7 7-7 7',
  copy: 'M9 9h10v11H9zM5 15V4h10',
  trash: 'M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13',
  bank: 'M3 10l9-6 9 6M5 10v8M9 10v8M15 10v8M19 10v8M3 20h18',
  box: 'M3 8l9-5 9 5v8l-9 5-9-5zM3 8l9 5 9-5M12 13v8',
  gear: 'M12 15a3 3 0 100-6 3 3 0 000 6zM19 12a7 7 0 00-.1-1.3l2-1.5-2-3.4-2.3.9a7 7 0 00-2.3-1.3L14 3h-4l-.3 2.4a7 7 0 00-2.3 1.3l-2.3-.9-2 3.4 2 1.5a7 7 0 000 2.6l-2 1.5 2 3.4 2.3-.9a7 7 0 002.3 1.3L10 21h4l.3-2.4a7 7 0 002.3-1.3l2.3.9 2-3.4-2-1.5c.1-.4.1-.9.1-1.3z',
  star: 'M12 3l2.7 5.6 6.1.8-4.5 4.3 1.1 6.1L12 16.9 6.6 19.8l1.1-6.1L3.2 9.4l6.1-.8z',
  user: 'M12 12a4 4 0 100-8 4 4 0 000 8zM4 21a8 8 0 0116 0',
  receipt: 'M6 3h12v18l-3-2-3 2-3-2-3 2zM9 8h6M9 12h6',
  out: 'M15 4h4v16h-4M10 8l-4 4 4 4M6 12h9',
}

export function Icon({ name }: { name: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d={PATHS[name] ?? ''} />
    </svg>
  )
}

/** Team mark: three bars stepping up, like a rising pace. */
export function Mark() {
  return (
    <svg className="mark" viewBox="0 0 28 28" aria-hidden="true">
      <rect width="28" height="28" rx="8" fill="var(--brand)" />
      <path d="M7 19.5h3.6M12.2 14h3.6M17.4 8.5H21" stroke="var(--brand-ink)" strokeWidth="3" strokeLinecap="round" fill="none" />
    </svg>
  )
}

// ---------- layout pieces ----------
export function PageHead({ title, sub, back, children }: { title: string; sub?: ReactNode; back?: string; children?: ReactNode }) {
  const { go } = useStore()
  return (
    <div className="page-head">
      <div className="stack" style={{ gap: 4 }}>
        {back && (
          <button className="btn ghost sm" style={{ alignSelf: 'flex-start', paddingLeft: 0 }} onClick={() => go(back)}>
            <Icon name="left" /> Back
          </button>
        )}
        <h1>{title}</h1>
        {sub && <p className="muted">{sub}</p>}
      </div>
      {children}
    </div>
  )
}

export function Pill({ tone, children }: { tone?: 'ok' | 'warn' | 'bad' | 'brand'; children: ReactNode }) {
  return <span className={'pill ' + (tone ?? '')}>{children}</span>
}

export function StatusPill({ status }: { status: string }) {
  const map: Record<string, ['ok' | 'warn' | 'bad' | 'brand' | undefined, string]> = {
    approved: ['ok', 'Approved'],
    pending: ['warn', 'Waiting for review'],
    rejected: ['bad', 'Rejected'],
    sent: ['ok', 'Sent'],
    active: ['ok', 'Active'],
    inactive: [undefined, 'Inactive'],
  }
  const [tone, label] = map[status] ?? [undefined, status]
  return <Pill tone={tone}>{label}</Pill>
}

export function PlanPill({ plan }: { plan: Plan | null }) {
  if (!plan) return <Pill>No goal</Pill>
  const tone = plan.state === 'hit' ? 'ok' : plan.state === 'behind' ? 'warn' : 'brand'
  return <Pill tone={tone}>{STATE_LABEL[plan.state]}</Pill>
}

/** Goal bar. The fill is approved money, the tick shows where today's pace should be. */
export function PaceBar({ plan, thin }: { plan: Plan; thin?: boolean }) {
  const showTick = plan.pacePct > 0 && plan.pacePct < 100 && plan.state !== 'hit'
  return (
    <div
      className={`track ${plan.state === 'hit' ? 'hit' : plan.state === 'behind' ? 'behind' : ''} ${thin ? 'thin' : ''}`}
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={Math.round(plan.pct)}
      aria-label="Progress to goal"
    >
      <i style={{ width: plan.pct + '%' }} />
      {showTick && <em style={{ left: plan.pacePct + '%' }} title="Where you should be today" />}
    </div>
  )
}

export function Stat({ label, value, sub, onClick }: { label: string; value: ReactNode; sub?: ReactNode; onClick?: () => void }) {
  const body = (
    <>
      <span className="label">{label}</span>
      <b>{value}</b>
      {sub && <span className="small muted">{sub}</span>}
    </>
  )
  return onClick ? (
    <button className="stat" onClick={onClick}>
      {body}
    </button>
  ) : (
    <div className="stat">{body}</div>
  )
}

export function Empty({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div className="card flat center">
      <h3>{title}</h3>
      {children && <p className="muted small">{children}</p>}
    </div>
  )
}

export function MonthNav({ month, onChange }: { month: string; onChange: (m: string) => void }) {
  return (
    <div className="monthnav">
      <button className="iconbtn" aria-label="Previous month" onClick={() => onChange(addMonths(month, -1))}>
        <Icon name="left" />
      </button>
      <span>{monthLabel(month)}</span>
      <button className="iconbtn" aria-label="Next month" onClick={() => onChange(addMonths(month, 1))}>
        <Icon name="right" />
      </button>
    </div>
  )
}

// ---------- forms ----------
export function Field({ label, hint, children }: { label: string; hint?: ReactNode; children: ReactNode }) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
      {hint && <small>{hint}</small>}
    </label>
  )
}

/** Number box that accepts "50,000" and keeps only digits. */
export function MoneyInput({ value, onChange, id, placeholder }: { value: number; onChange: (n: number) => void; id: string; placeholder?: string }) {
  return (
    <input
      id={id}
      className="input num"
      inputMode="numeric"
      placeholder={placeholder ?? '0'}
      value={value ? value.toLocaleString('en-NG') : ''}
      onChange={(e) => onChange(Number(e.target.value.replace(/[^\d]/g, '')) || 0)}
    />
  )
}

export function NumInput({ value, onChange, id, step }: { value: number; onChange: (n: number) => void; id: string; step?: string }) {
  return (
    <input
      id={id}
      className="input num"
      type="number"
      inputMode="decimal"
      min="0"
      step={step ?? 'any'}
      value={Number.isFinite(value) && value !== 0 ? value : ''}
      placeholder="0"
      onChange={(e) => onChange(Math.max(0, Number(e.target.value) || 0))}
    />
  )
}

export function Sheet({ title, onClose, children }: { title: string; onClose: () => void; children: ReactNode }) {
  const id = useId()
  const ref = useRef<HTMLDivElement>(null)
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose()
    document.addEventListener('keydown', onKey)
    ref.current?.focus()
    return () => document.removeEventListener('keydown', onKey)
  }, [onClose])
  return (
    <div className="overlay" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className="sheet" role="dialog" aria-modal="true" aria-labelledby={id} tabIndex={-1} ref={ref}>
        <div className="row">
          <h2 className="grow" id={id}>
            {title}
          </h2>
          <button className="iconbtn" aria-label="Close" onClick={onClose}>
            <Icon name="x" />
          </button>
        </div>
        {children}
      </div>
    </div>
  )
}

export function Confirm({ title, body, action, danger, onYes, onClose }: { title: string; body: ReactNode; action: string; danger?: boolean; onYes: () => void; onClose: () => void }) {
  return (
    <Sheet title={title} onClose={onClose}>
      <p>{body}</p>
      <div className="row">
        <button className="btn grow" onClick={onClose}>
          Cancel
        </button>
        <button className={'btn grow ' + (danger ? 'danger' : 'primary')} onClick={onYes}>
          {action}
        </button>
      </div>
    </Sheet>
  )
}

/** Small picture that opens big when tapped. Used for payment screenshots. */
export function Proof({ path, label }: { path: string | null; label?: string }) {
  const { backend } = useStore()
  const [url, setUrl] = useState<string | null>(null)
  const [failed, setFailed] = useState(false)
  const [open, setOpen] = useState(false)
  useEffect(() => {
    let live = true
    setUrl(null)
    setFailed(false)
    if (path)
      backend
        .fileUrl(path)
        .then((u) => live && setUrl(u))
        .catch(() => live && setFailed(true))
    return () => {
      live = false
    }
  }, [path, backend])
  if (!path) return <div className="thumb">No proof</div>
  return (
    <>
      <button className="thumb" onClick={() => url && setOpen(true)} aria-label={label ?? 'Open screenshot'}>
        {url ? <img src={url} alt="" /> : failed ? 'Error' : '...'}
      </button>
      {open && url && (
        <Sheet title={label ?? 'Screenshot'} onClose={() => setOpen(false)}>
          <img className="fullimg" src={url} alt={label ?? 'Screenshot'} />
        </Sheet>
      )}
    </>
  )
}

export function FilePick({ id, file, onPick }: { id: string; file: File | null; onPick: (f: File | null) => void }) {
  const [preview, setPreview] = useState<string | null>(null)
  useEffect(() => {
    if (!file) return setPreview(null)
    const u = URL.createObjectURL(file)
    setPreview(u)
    return () => URL.revokeObjectURL(u)
  }, [file])
  return (
    <div className="row">
      {preview && (
        <div className="thumb">
          <img src={preview} alt="Chosen screenshot" />
        </div>
      )}
      <input id={id} className="input grow" type="file" accept="image/*" onChange={(e) => onPick(e.target.files?.[0] ?? null)} />
    </div>
  )
}

export function CopyButton({ text, label }: { text: string; label?: string }) {
  const { toast } = useStore()
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(text)
      toast('Copied')
    } catch {
      toast('Could not copy. Press and hold the text to copy it.', 'bad')
    }
  }
  return (
    <button className="btn sm" onClick={copy}>
      <Icon name="copy" /> {label ?? 'Copy'}
    </button>
  )
}

/** Keeps a button from being pressed twice while a save is running. */
export function useBusy(): [boolean, (fn: () => Promise<unknown>) => Promise<void>] {
  const [busy, setBusy] = useState(false)
  const wrap = async (fn: () => Promise<unknown>) => {
    if (busy) return
    setBusy(true)
    try {
      await fn()
    } finally {
      setBusy(false)
    }
  }
  return [busy, wrap]
}
