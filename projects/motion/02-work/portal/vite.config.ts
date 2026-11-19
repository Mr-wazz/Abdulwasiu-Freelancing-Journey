import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'

// "demo" mode builds one self contained HTML file that runs on sample data
// in the browser, with no server. The normal build talks to Supabase.
export default defineConfig(({ mode }) => ({
  plugins: [react(), ...(mode === 'demo' ? [viteSingleFile()] : [])],
  define: mode === 'demo' ? { 'import.meta.env.VITE_DEMO': '"1"' } : {},
}))
