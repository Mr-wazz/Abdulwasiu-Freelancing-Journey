import { useMemo, useState } from 'react'
import { calcSvb, cartTotals, DIRECTOR_QPV, MIN_PERSONAL_PV, SVB_CHART } from '../lib/calc'
import { naira, num } from '../lib/dates'
import { childMap, descendants } from '../lib/tree'
import { useStore } from '../store'
import { Field, Icon, NumInput, PageHead, Pill } from '../ui'

interface LegRow {
  key: string
  name: string
  people: number
  qpv: number
}

export function Calculator() {
  const { data, me } = useStore()
  const products = data.products.filter((p) => p.active)

  const startLegs = useMemo<LegRow[]>(() => {
    const map = childMap(data.profiles.filter((p) => p.status === 'active'))
    return (map.get(me.id) ?? []).map((p) => {
      const people = 1 + descendants(p.id, map).length
      return { key: p.id, name: p.full_name, people, qpv: 250 * people }
    })
    // Only build the starting rows once, so typing is not overwritten.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const [mode, setMode] = useState<'pv' | 'products'>('pv')
  const [ownPv, setOwnPv] = useState(250)
  const [qty, setQty] = useState<Record<string, number>>({})
  const [legs, setLegs] = useState<LegRow[]>(startLegs)
  const [each, setEach] = useState(250)
  const [rate, setRate] = useState(data.settings.bv_per_pv)

  const cart = cartTotals(products.map((p) => ({ ...p, qty: qty[p.id] ?? 0 })))
  const myPv = mode === 'products' ? cart.pv : ownPv
  const myBv = mode === 'products' ? cart.bv : ownPv * rate
  const result = calcSvb({ ownPv: myPv, ownBv: myBv, legs: legs.map((l) => ({ name: l.name, qpv: l.qpv, bv: l.qpv * rate })) })
  const noRate = rate <= 0

  const applyEach = () => {
    setMode('pv')
    setOwnPv(each)
    setLegs((ls) => ls.map((l) => ({ ...l, qpv: each * l.people })))
  }
  const setLeg = (key: string, patch: Partial<LegRow>) => setLegs((ls) => ls.map((l) => (l.key === key ? { ...l, ...patch } : l)))
  const bump = (id: string, d: number) => setQty((q) => ({ ...q, [id]: Math.max(0, (q[id] ?? 0) + d) }))

  return (
    <>
      <PageHead title="Bonus calculator" sub="See what you would earn from your own points and your team's points." />

      <div className="card hero">
        <span className="label">Your Sales Volume Bonus for the month</span>
        <div className="big" data-testid="svb-total">
          {noRate && mode === 'pv' ? result.pct + '%' : naira(result.total)}
        </div>
        <div className="row">
          <span className="pill" style={{ background: 'var(--brand-ink)', color: 'var(--brand)' }}>
            {num(result.qpv)} QPV
          </span>
          <span className="pill" style={{ background: 'var(--brand-ink)', color: 'var(--brand)' }}>
            {result.pct}% level{result.pct > 0 && result.rank ? ' · ' + result.rank : ''}
          </span>
        </div>
        <p className="small muted">
          {!result.eligible
            ? `You need at least ${MIN_PERSONAL_PV} personal PV in the month to be paid a bonus. You have ${num(myPv)}.`
            : result.pct === 0
              ? `You need 250 QPV to start earning. You are ${num(250 - result.qpv)} PV away.`
              : result.next
                ? `${num(result.toNext)} more PV takes you to ${result.next.pct}% (${result.next.rank}).`
                : 'You are at the top of the chart: 25%.'}
        </p>
      </div>

      <div className="card">
        <div className="card-head">
          <h2>Try a team target</h2>
        </div>
        <p className="small muted">What if you and every person in your team each do the same points?</p>
        <div className="chips">
          {[100, 250, 500].map((n) => (
            <button key={n} className="chip" aria-pressed={each === n} onClick={() => setEach(n)}>
              {n} PV each
            </button>
          ))}
        </div>
        <div className="row">
          <div className="grow">
            <NumInput id="calc-each" value={each} onChange={setEach} />
          </div>
          <button className="btn primary" onClick={applyEach}>
            Apply to everyone
          </button>
        </div>
      </div>

      <div className="card">
        <div className="card-head">
          <h2>1. Your own order</h2>
          <div className="chips">
            <button className="chip" aria-pressed={mode === 'pv'} onClick={() => setMode('pv')}>
              Type PV
            </button>
            <button className="chip" aria-pressed={mode === 'products'} onClick={() => setMode('products')}>
              Pick products
            </button>
          </div>
        </div>
        {mode === 'pv' ? (
          <Field label="Your personal PV this month" hint="PV is the point value of the products you buy and sell.">
            <NumInput id="calc-own-pv" value={ownPv} onChange={setOwnPv} />
          </Field>
        ) : products.length === 0 ? (
          <p className="note">No products have been added yet. Ask your team leader to add the price list, or use “Type PV”.</p>
        ) : (
          <>
            <div className="list">
              {products.map((p) => (
                <div key={p.id} className="item">
                  <span className="grow">
                    <span className="title">{p.name}</span>
                    <br />
                    <span className="small muted num">
                      {num(p.pv)} PV · BV {naira(p.bv)} · {naira(p.dp)}
                    </span>
                  </span>
                  <span className="stepper">
                    <button aria-label={`One less ${p.name}`} onClick={() => bump(p.id, -1)}>
                      −
                    </button>
                    <output>{qty[p.id] ?? 0}</output>
                    <button aria-label={`One more ${p.name}`} onClick={() => bump(p.id, 1)}>
                      +
                    </button>
                  </span>
                </div>
              ))}
            </div>
            <div className="stats">
              <div className="stat">
                <span className="label">Your PV</span>
                <b>{num(cart.pv)}</b>
              </div>
              <div className="stat">
                <span className="label">Your BV</span>
                <b>{naira(cart.bv)}</b>
              </div>
              <div className="stat">
                <span className="label">You pay</span>
                <b>{naira(cart.cost)}</b>
              </div>
              <div className="stat">
                <span className="label">Retail profit</span>
                <b>{naira(cart.profit)}</b>
                <span className="small muted">if all sold at retail price</span>
              </div>
            </div>
          </>
        )}
      </div>

      <div className="card">
        <div className="card-head">
          <h2>2. Your team</h2>
          <button
            className="btn sm"
            onClick={() => setLegs((ls) => [...ls, { key: 'x' + Date.now(), name: `New person ${ls.length + 1}`, people: 1, qpv: each }])}
          >
            <Icon name="plus" /> Add person
          </button>
        </div>
        <p className="small muted">One row for each person you sponsored yourself. Enter the total PV of that person and everyone under them.</p>
        {legs.length === 0 ? (
          <p className="note">You have no downline yet. Tap “Add person” to see what sponsoring someone would add.</p>
        ) : (
          <div className="list">
            {legs.map((l) => (
              <div key={l.key} className="row">
                <div className="grow">
                  <input className="input" aria-label="Name" value={l.name} onChange={(e) => setLeg(l.key, { name: e.target.value })} />
                  {l.people > 1 && <span className="small muted">{l.people} people in this line</span>}
                </div>
                <div style={{ width: 110 }}>
                  <input
                    className="input num"
                    type="number"
                    inputMode="decimal"
                    min="0"
                    aria-label={`Total PV for ${l.name}`}
                    value={l.qpv || ''}
                    placeholder="0"
                    onChange={(e) => setLeg(l.key, { qpv: Math.max(0, Number(e.target.value) || 0) })}
                  />
                </div>
                <button className="iconbtn" aria-label={`Remove ${l.name}`} onClick={() => setLegs((ls) => ls.filter((x) => x.key !== l.key))}>
                  <Icon name="x" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card">
        <h2>3. Value of one point</h2>
        <Field
          label="Bonus Volume (BV) per 1 PV, in Naira"
          hint="Bonuses are paid on BV, not PV. This average turns points into Naira. Your team leader sets it from the NeoLife price list."
        >
          <NumInput id="calc-rate" value={rate} onChange={setRate} />
        </Field>
        {noRate && <p className="note warn">No rate is set yet, so Naira amounts show as zero. The percentages are still correct.</p>}
      </div>

      <div className="card">
        <h2>How the bonus adds up</h2>
        <div className="tablewrap">
          <table>
            <thead>
              <tr>
                <th>From</th>
                <th className="r">PV</th>
                <th className="r">They get</th>
                <th className="r">You get</th>
                <th className="r">Naira</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Your own order</td>
                <td className="r">{num(myPv)}</td>
                <td className="r"></td>
                <td className="r">{result.pct}%</td>
                <td className="r">{naira(result.ownEarn)}</td>
              </tr>
              {result.legs.map((l, i) => (
                <tr key={i}>
                  <td>
                    {l.name} {l.directorLeg && <Pill tone="brand">Director line</Pill>}
                  </td>
                  <td className="r">{num(l.qpv)}</td>
                  <td className="r">{l.legPct}%</td>
                  <td className="r">{l.directorLeg ? 'LDB' : l.diffPct + '%'}</td>
                  <td className="r">{l.directorLeg ? 'separate' : naira(l.earn)}</td>
                </tr>
              ))}
              <tr className="now">
                <td>Total bonus</td>
                <td className="r">{num(result.qpv)}</td>
                <td className="r"></td>
                <td className="r"></td>
                <td className="r">{naira(result.total)}</td>
              </tr>
              {mode === 'products' && cart.profit > 0 && (
                <tr className="now">
                  <td>Bonus plus retail profit</td>
                  <td className="r"></td>
                  <td className="r"></td>
                  <td className="r"></td>
                  <td className="r">{naira(result.total + cart.profit)}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        {result.legs.some((l) => l.directorLeg) && (
          <p className="note">
            A line with {num(DIRECTOR_QPV)} QPV or more is a Director line. Its points leave your QPV, and NeoLife pays you a Leadership Development Bonus on it instead. That bonus is
            not counted here.
          </p>
        )}
        <p className="small muted">
          You earn your % on your own order. On each person you sponsored, you earn the gap between your % and the % they earn themselves. This is an estimate to help you plan, not
          a promise of income. NeoLife pays on the true BV of each product.
        </p>
      </div>

      <div className="card">
        <h2>Sales Volume Bonus chart</h2>
        <div className="tablewrap">
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th className="r">Monthly QPV</th>
                <th className="r">Bonus</th>
              </tr>
            </thead>
            <tbody>
              {[...SVB_CHART].reverse().map((l) => (
                <tr key={l.qpv} className={result.pct === l.pct ? 'now' : ''}>
                  <td>{l.rank}</td>
                  <td className="r">{num(l.qpv)}</td>
                  <td className="r">{l.pct}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="small muted">From the NeoLife Compensation Plan for Africa, March 2026. You need {MIN_PERSONAL_PV} personal PV each month to be paid.</p>
      </div>
    </>
  )
}
