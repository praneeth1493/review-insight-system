import './Badge.css'

const COLORS = {
  positive: '#22c55e',
  negative: '#f43f5e',
  neutral: '#f59e0b',
  critical: '#f43f5e',
  high: '#fb923c',
  medium: '#f59e0b',
  low: '#8b5cf6',
}

export default function Badge({ label }) {
  const key = label?.toLowerCase()
  const color = COLORS[key] || '#a78bfa'
  return (
    <span className="badge" style={{ background: color + '18', color, border: `1px solid ${color}40` }}>
      {label}
    </span>
  )
}
