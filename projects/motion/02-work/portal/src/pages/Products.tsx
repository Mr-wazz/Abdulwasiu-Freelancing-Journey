import { type FormEvent, useState } from 'react'
import { naira, num } from '../lib/dates'
import type { Product } from '../lib/types'
import { useStore } from '../store'
import { Confirm, Empty, Field, Icon, MoneyInput, NumInput, PageHead, Sheet, useBusy } from '../ui'

type Draft = Pick<Product, 'name' | 'code' | 'pv' | 'bv' | 'dp' | 'srp'>

const toNumber = (s: string | undefined) => Number((s ?? '').replace(/[^\d.]/g, '')) || 0

/**
 * Reads rows copied from a spreadsheet: name, code, PV, BV, distributor price, retail price.
 * Columns copied from Excel or Google Sheets are split by tabs. Typed lists can use commas.
 */
export function parseProducts(text: string): Draft[] {
  const out: Draft[] = []
  for (const line of text.split(/\r?\n/)) {
    if (!line.trim()) continue
    const cells = (line.includes('\t') ? line.split('\t') : line.split(',')).map((c) => c.trim())
    const [name, code, pv, bv, dp, srp] = cells
    if (!name || cells.length < 3) continue
    if (!/\d/.test(pv ?? '')) continue // heading row
    out.push({ name, code: code || null, pv: toNumber(pv), bv: toNumber(bv), dp: toNumber(dp), srp: toNumber(srp) })
  }
  return out
}

function ProductForm({ product, onClose }: { product?: Product; onClose: () => void }) {
  const { backend, run } = useStore()
  const [d, setD] = useState<Draft>(product ?? { name: '', code: '', pv: 0, bv: 0, dp: 0, srp: 0 })
  const [busy, wrap] = useBusy()
  const set = (patch: Partial<Draft>) => setD((x) => ({ ...x, ...patch }))

  const save = (e: FormEvent) => {
    e.preventDefault()
    void wrap(async () => {
      const row = { name: d.name.trim(), code: (d.code ?? '').trim() || null, pv: d.pv, bv: d.bv, dp: d.dp, srp: d.srp }
      const ok = product
        ? await run(() => backend.update('products', { id: product.id }, row), 'Product saved')
        : await run(() => backend.insert<Product>('products', { ...row, active: true }), 'Product added')
      if (ok) onClose()
    })
  }

  return (
    <Sheet title={product ? 'Edit product' : 'Add a product'} onClose={onClose}>
      <form className="stack" onSubmit={save}>
        <Field label="Product name">
          <input id="prod-name" className="input" required maxLength={120} value={d.name} onChange={(e) => set({ name: e.target.value })} />
        </Field>
        <div className="grid2">
          <Field label="Code (optional)">
            <input id="prod-code" className="input" maxLength={30} value={d.code ?? ''} onChange={(e) => set({ code: e.target.value })} />
          </Field>
          <Field label="PV (points)">
            <NumInput id="prod-pv" value={d.pv} onChange={(pv) => set({ pv })} />
          </Field>
        </div>
        <div className="grid2">
          <Field label="BV (₦)" hint="Bonus Volume. Bonuses are paid on this.">
            <MoneyInput id="prod-bv" value={d.bv} onChange={(bv) => set({ bv })} />
          </Field>
          <Field label="Distributor price (₦)">
            <MoneyInput id="prod-dp" value={d.dp} onChange={(dp) => set({ dp })} />
          </Field>
        </div>
        <Field label="Retail price (₦)" hint="Suggested Retail Price. Retail profit is this minus the distributor price.">
          <MoneyInput id="prod-srp" value={d.srp} onChange={(srp) => set({ srp })} />
        </Field>
        <button className="btn primary block" disabled={busy}>
          {product ? 'Save product' : 'Add product'}
        </button>
      </form>
    </Sheet>
  )
}

function ImportForm({ onClose }: { onClose: () => void }) {
  const { backend, run } = useStore()
  const [text, setText] = useState('')
  const [busy, wrap] = useBusy()
  const rows = parseProducts(text)

  const save = () =>
    wrap(async () => {
      const ok = await run(async () => {
        for (let i = 0; i < rows.length; i += 10) {
          await Promise.all(rows.slice(i, i + 10).map((r) => backend.insert<Product>('products', { ...r, active: true })))
        }
      }, `${rows.length} products added`)
      if (ok) onClose()
    })

  return (
    <Sheet title="Paste a price list" onClose={onClose}>
      <p className="small muted">
        Put the list in Excel or Google Sheets with these columns, in this order: <b>Name, Code, PV, BV, Distributor price, Retail price</b>. Select the rows, copy, and paste
        them here.
      </p>
      <textarea id="import-text" className="input" rows={8} value={text} onChange={(e) => setText(e.target.value)} placeholder={'Product name\tCode\t25\t22000\t30000\t36000'} />
      {rows.length > 0 && (
        <p className="note ok">
          {rows.length} {rows.length === 1 ? 'product' : 'products'} found. First one: {rows[0].name}, {num(rows[0].pv)} PV, BV {naira(rows[0].bv)}.
        </p>
      )}
      {text.trim() && rows.length === 0 && <p className="note warn">No products found yet. Check that each line has a name, a code and a PV number.</p>}
      <button className="btn primary block" disabled={busy || rows.length === 0} onClick={() => void save()}>
        {busy ? 'Adding' : `Add ${rows.length || ''} products`}
      </button>
    </Sheet>
  )
}

export function Products() {
  const { data, isAdmin, backend, run } = useStore()
  const [sheet, setSheet] = useState<'add' | 'import' | null>(null)
  const [editing, setEditing] = useState<Product | null>(null)
  const [removing, setRemoving] = useState<Product | null>(null)
  const [search, setSearch] = useState('')
  const list = data.products.filter((p) => p.name.toLowerCase().includes(search.trim().toLowerCase()))

  return (
    <>
      <PageHead title="Products" sub="The price list the bonus calculator uses: points (PV), Bonus Volume (BV) and prices." back="more" />

      {isAdmin && (
        <div className="row">
          <button className="btn primary grow" onClick={() => setSheet('add')}>
            <Icon name="plus" /> Add product
          </button>
          <button className="btn grow" onClick={() => setSheet('import')}>
            Paste a price list
          </button>
        </div>
      )}

      {data.products.length === 0 ? (
        <Empty title="No products yet">
          {isAdmin ? 'Add products one by one, or paste the whole NeoLife price list from a spreadsheet.' : 'Your team leader has not added the price list yet.'}
        </Empty>
      ) : (
        <>
          <input id="prod-search" className="input" type="search" placeholder="Search products" value={search} onChange={(e) => setSearch(e.target.value)} />
          <div className="card">
            <div className="tablewrap">
              <table>
                <thead>
                  <tr>
                    <th>Product</th>
                    <th className="r">PV</th>
                    <th className="r">BV</th>
                    <th className="r">Distributor</th>
                    <th className="r">Retail</th>
                    {isAdmin && <th></th>}
                  </tr>
                </thead>
                <tbody>
                  {list.map((p) => (
                    <tr key={p.id}>
                      <td>
                        {p.name}
                        {p.code && (
                          <>
                            <br />
                            <span className="small muted">{p.code}</span>
                          </>
                        )}
                      </td>
                      <td className="r">{num(p.pv)}</td>
                      <td className="r">{naira(p.bv)}</td>
                      <td className="r">{naira(p.dp)}</td>
                      <td className="r">{naira(p.srp)}</td>
                      {isAdmin && (
                        <td className="r">
                          <button className="btn ghost sm" onClick={() => setEditing(p)}>
                            Edit
                          </button>
                          <button className="btn ghost sm" aria-label={`Delete ${p.name}`} onClick={() => setRemoving(p)}>
                            Delete
                          </button>
                        </td>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      {sheet === 'add' && <ProductForm onClose={() => setSheet(null)} />}
      {sheet === 'import' && <ImportForm onClose={() => setSheet(null)} />}
      {editing && <ProductForm product={editing} onClose={() => setEditing(null)} />}
      {removing && (
        <Confirm
          title={`Delete ${removing.name}?`}
          body="It is removed from the price list and the calculator."
          action="Delete"
          danger
          onClose={() => setRemoving(null)}
          onYes={() => {
            const id = removing.id
            setRemoving(null)
            void run(() => backend.remove('products', { id }), 'Product deleted')
          }}
        />
      )}
    </>
  )
}
