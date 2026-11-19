import { childMap } from '../lib/tree'
import { useStore } from '../store'
import { PageHead, Pill } from '../ui'

// From the three NeoLife Nigeria event flyers. Qualification period: August 2026 to January 2027.
const PERIOD_START = '2026-08-01'
const PERIOD_END = '2027-01-31'

const EVENTS = [
  {
    name: 'Senior and Executive Manager Seminar',
    sponsor: 6,
    rules: ['Qualify for 5 of the 6 months.', 'Personally sponsor 6 new Distributors in the period.'],
    extra: 'New Executive Managers in the last month who personally sponsored at least 1 person in the period are also invited.',
  },
  {
    name: 'Director School',
    sponsor: 4,
    rules: ['Qualify for 4 of the 6 months.', 'Personally sponsor 4 new Distributors in the period.'],
    extra: 'New Directors in the last qualification month who personally sponsored at least 1 new Distributor are also invited.',
  },
  {
    name: 'World Team Workshop 2027',
    sponsor: 3,
    rules: ['Qualify at title for 4 of the 6 months.', 'Personally sponsor at least 3 new Distributors in the period.', 'Sponsor at least 12 in your Director team.'],
    extra: 'New World Team Members in the last month of the period get a special invitation.',
  },
]

export function Incentives() {
  const { data, me, isAdmin } = useStore()
  const counted = data.profiles.filter((p) => p.status !== 'pending')
  const map = childMap(counted)
  const newlySponsored = (id: string) => (map.get(id) ?? []).filter((p) => p.joined_on && p.joined_on >= PERIOD_START && p.joined_on <= PERIOD_END).length
  const mine = newlySponsored(me.id)
  const board = counted
    .filter((p) => p.status === 'active')
    .map((p) => ({ p, n: newlySponsored(p.id) }))
    .sort((a, b) => b.n - a.n)

  return (
    <>
      <PageHead title="Incentives" sub="NeoLife Nigeria events you can qualify for. Period: August 2026 to January 2027." back="more" />

      <div className="card hero">
        <span className="label">New Distributors you sponsored in the period</span>
        <div className="big">{mine}</div>
        <p className="small muted">Counted from the people added under you in this portal with a join date from 1 August 2026.</p>
      </div>

      {EVENTS.map((ev) => {
        const pct = Math.min(100, (mine / ev.sponsor) * 100)
        return (
          <div key={ev.name} className="card">
            <div className="card-head">
              <h2>{ev.name}</h2>
              {mine >= ev.sponsor ? <Pill tone="ok">Sponsoring done</Pill> : <Pill>{ev.sponsor - mine} more to sponsor</Pill>}
            </div>
            <div className={'track ' + (mine >= ev.sponsor ? 'hit' : '')} role="progressbar" aria-valuemin={0} aria-valuemax={ev.sponsor} aria-valuenow={Math.min(mine, ev.sponsor)} aria-label="New Distributors sponsored">
              <i style={{ width: pct + '%' }} />
            </div>
            <p className="small muted num">
              {Math.min(mine, ev.sponsor)} of {ev.sponsor} new Distributors sponsored
            </p>
            <ul style={{ margin: 0, paddingLeft: 20 }}>
              {ev.rules.map((r) => (
                <li key={r}>{r}</li>
              ))}
            </ul>
            <p className="small muted">{ev.extra}</p>
          </div>
        )
      })}

      <p className="note">The portal tracks the sponsoring part. The “qualify for X of 6 months” part is checked in your NeoLife back office. Dates and venues are shared by NeoLife closer to each event.</p>

      {isAdmin && (
        <div className="card">
          <h2>Who is sponsoring</h2>
          <div className="tablewrap">
            <table>
              <thead>
                <tr>
                  <th>Member</th>
                  <th>Rank</th>
                  <th className="r">New in period</th>
                </tr>
              </thead>
              <tbody>
                {board.map(({ p, n }) => (
                  <tr key={p.id}>
                    <td>{p.full_name}</td>
                    <td>{p.rank}</td>
                    <td className="r">{n}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </>
  )
}
