import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Aspects from './pages/Aspects'
import Reviews from './pages/Reviews'
import Analyzer from './pages/Analyzer'
import Metrics from './pages/Metrics'
import './App.css'

const PAGES = { dashboard: Dashboard, aspects: Aspects, reviews: Reviews, analyzer: Analyzer, metrics: Metrics }

export default function App() {
  const [page, setPage] = useState('dashboard')
  const Page = PAGES[page]
  return (
    <div className="app-shell">
      <Sidebar active={page} onNav={setPage} />
      <main className="app-main">
        <Page />
      </main>
    </div>
  )
}
