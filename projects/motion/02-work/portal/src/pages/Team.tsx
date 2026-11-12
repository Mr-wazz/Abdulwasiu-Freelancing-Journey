import { useState } from 'react'
import { childMap, roots, treeRows } from '../lib/tree'
import { initials, nameOf, useStore } from '../store'
import { Empty, Icon, PageHead, Pill, Stat } from '../ui'
import { MemberForm } from './Member'

type Filter = 'all' | 'with' | 'without' | 'pending'

export function Team() {
  const { data, me, isAdmin, go } = useStore()
  const [filter, setFilter] = useState<Filter>('all')
  const [search, setSearch] = useState('')
  const [adding, setAdding] = useState(false)

  // Downline counts ignore people who are still waiting for approval.
  const counted = data.profiles.filter((p) => p.status !== 'pending')
  const countMap = childMap(counted)
  const fullMap = childMap(data.profiles)
  const rootIds = isAdmin ? roots(data.profiles) : [me.id]
  const rows = treeRows(data.profiles, rootIds, fullMap).map((r) => ({
    ...r,
    downline: treeRows(counted, [r.profile.id], countMap).length - 1,
  }))

  const team = rows.filter((r) => r.profile.id !== me.id && r.profile.status !== 'pending')
  const withDown = team.filter((r) => r.downline > 0).length
  const pending = rows.filter((r) => r.profile.status === 'pending').length

  const q = search.trim().toLowerCase()
  const flat = filter !== 'all' || q !== ''
  const shown = rows.filter((r) => {
    if (q && !r.profile.full_name.toLowerCase().includes(q)) return false
    if (filter === 'pending') return r.profile.status === 'pending'
    if (filter === 'with') return r.profile.status !== 'pending' && r.downline > 0 && r.profile.id !== me.id
    if (filter === 'without') return r.profile.status !== 'pending' && r.downline === 0 && r.profile.id !== me.id
    return true
  })

  return (
    <>
      <PageHead
        title={isAdmin ? 'Team' : 'My team'}
        sub={isAdmin ? 'Everyone in the team, shown under the person who sponsored them.' : `You and the people under you. Your sponsor is ${nameOf(data, me.sponsor_id)}.`}
      >
        <button className="btn primary" onClick={() => setAdding(true)}>
          <Icon name="plus" /> Add member
        </button>
      </PageHead>

      <div className="stats">
        <Stat label={isAdmin ? 'Team members' : 'In my downline'} value={team.length} onClick={() => setFilter('all')} />
        <Stat label="Have a downline" value={withDown} onClick={() => setFilter('with')} />
        <Stat label="No downline yet" value={team.length - withDown} onClick={() => setFilter('without')} />
      </div>

      <div className="stack">
        <input id="team-search" className="input" type="search" placeholder="Search by name" value={search} onChange={(e) => setSearch(e.target.value)} />
        <div className="chips">
          {(
            [
              ['all', 'Everyone'],
              ['with', 'Has a downline'],
              ['without', 'No downline'],
              ['pending', `Waiting for approval${pending ? ` (${pending})` : ''}`],
            ] as [Filter, string][]
          ).map(([id, label]) => (
            <button key={id} className="chip" aria-pressed={filter === id} onClick={() => setFilter(id)}>
              {label}
            </button>
          ))}
        </div>
      </div>

      {shown.length === 0 ? (
        <Empty title="Nobody here yet">{filter === 'all' && !q ? 'Tap “Add member” to add the first person you sponsored.' : 'No one matches this view.'}</Empty>
      ) : (
        <div className="card">
          <div className="list">
            {shown.map((r) => (
              <button key={r.profile.id} className="item" onClick={() => go('member-' + r.profile.id)}>
                {!flat && Array.from({ length: Math.min(r.depth, 5) }, (_, i) => <span key={i} className="indent" style={{ marginLeft: i === 0 ? 8 : 0 }} />)}
                <span className="avatar">{initials(r.profile.full_name)}</span>
                <span className="grow">
                  <span className="title">
                    {r.profile.full_name}
                    {r.profile.id === me.id ? ' (you)' : ''}
                  </span>
                  <br />
                  <span className="small muted">
                    {r.profile.rank}
                    {flat && r.profile.sponsor_id ? ' · under ' + nameOf(data, r.profile.sponsor_id) : ''}
                  </span>
                </span>
                {r.profile.status === 'pending' ? (
                  <Pill tone="warn">Waiting</Pill>
                ) : r.profile.status === 'inactive' ? (
                  <Pill>Inactive</Pill>
                ) : r.downline > 0 ? (
                  <Pill tone="brand">{r.downline} downline</Pill>
                ) : (
                  <Pill>No downline</Pill>
                )}
              </button>
            ))}
          </div>
        </div>
      )}

      {adding && <MemberForm onClose={() => setAdding(false)} />}
    </>
  )
}
