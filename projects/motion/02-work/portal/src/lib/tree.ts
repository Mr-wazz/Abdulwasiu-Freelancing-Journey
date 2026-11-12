import type { Profile } from './types'

export type ChildMap = Map<string, Profile[]>

/** Sponsor id to the people they sponsored. */
export function childMap(profiles: Profile[]): ChildMap {
  const map: ChildMap = new Map()
  for (const p of profiles) {
    if (!p.sponsor_id) continue
    const list = map.get(p.sponsor_id) ?? []
    list.push(p)
    map.set(p.sponsor_id, list)
  }
  for (const list of map.values()) list.sort((a, b) => a.full_name.localeCompare(b.full_name))
  return map
}

/** Everyone under a person, at any depth. */
export function descendants(id: string, map: ChildMap): Profile[] {
  const out: Profile[] = []
  const seen = new Set<string>([id])
  const stack = [...(map.get(id) ?? [])]
  while (stack.length) {
    const p = stack.pop()!
    if (seen.has(p.id)) continue
    seen.add(p.id)
    out.push(p)
    stack.push(...(map.get(p.id) ?? []))
  }
  return out
}

export interface TreeRow {
  profile: Profile
  depth: number
  downline: number
}

/** Flat list in tree order, for an indented team list. */
export function treeRows(profiles: Profile[], rootIds: string[], map: ChildMap): TreeRow[] {
  const byId = new Map(profiles.map((p) => [p.id, p]))
  const rows: TreeRow[] = []
  const seen = new Set<string>()
  const walk = (id: string, depth: number) => {
    const p = byId.get(id)
    if (!p || seen.has(id)) return
    seen.add(id)
    rows.push({ profile: p, depth, downline: descendants(id, map).length })
    for (const c of map.get(id) ?? []) walk(c.id, depth + 1)
  }
  rootIds.forEach((id) => walk(id, 0))
  return rows
}

/** People with no visible sponsor: the tops of the tree. */
export function roots(profiles: Profile[]): string[] {
  const ids = new Set(profiles.map((p) => p.id))
  return profiles
    .filter((p) => !p.sponsor_id || !ids.has(p.sponsor_id))
    .sort((a, b) => (a.role === 'admin' ? -1 : b.role === 'admin' ? 1 : a.full_name.localeCompare(b.full_name)))
    .map((p) => p.id)
}
