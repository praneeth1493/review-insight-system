import { LayoutDashboard, BarChart2, MessageSquare, Zap, FlaskConical } from 'lucide-react'
import './Sidebar.css'

const NAV = [
  { key: 'dashboard', label: 'Dashboard',  icon: LayoutDashboard },
  { key: 'aspects',   label: 'Aspects',    icon: BarChart2 },
  { key: 'reviews',   label: 'Reviews',    icon: MessageSquare },
  { key: 'analyzer',  label: 'Analyzer',   icon: Zap },
  { key: 'metrics',   label: 'Evaluation', icon: FlaskConical },
]

export default function Sidebar({ active, onNav }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon-wrap">🔍</div>
        <div>
          <div className="logo-text">ReviewIQ</div>
          <div className="logo-badge">AI Powered</div>
        </div>
      </div>
      <nav className="sidebar-nav">
        {NAV.map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            className={`nav-item ${active === key ? 'active' : ''}`}
            onClick={() => onNav(key)}
          >
            <div className="nav-icon-wrap">
              <Icon size={16} />
            </div>
            <span>{label}</span>
            <div className="nav-dot" />
          </button>
        ))}
      </nav>
      <div className="sidebar-footer">
        <div className="footer-badge">
          <div className="footer-dot" />
          <span className="footer-text">VADER + NLP Engine</span>
        </div>
      </div>
    </aside>
  )
}
