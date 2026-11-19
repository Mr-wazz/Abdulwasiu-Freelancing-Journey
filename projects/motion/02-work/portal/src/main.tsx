import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { App } from './App'
import type { Backend } from './data/backend'
import { makeDemo } from './data/demo'
import './styles.css'

async function pickBackend(): Promise<Backend> {
  if (import.meta.env.VITE_DEMO === '1') return makeDemo()
  const url = import.meta.env.VITE_SUPABASE_URL as string | undefined
  const key = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined
  // No database keys yet: run on sample data so the screens can still be tried.
  if (!url || !key) return makeDemo()
  const { makeLive } = await import('./data/supabase')
  return makeLive(url, key)
}

pickBackend().then((backend) => {
  createRoot(document.getElementById('root')!).render(
    <StrictMode>
      <App backend={backend} />
    </StrictMode>,
  )
})
