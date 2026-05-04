import { useEffect, useState } from 'react'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'
import { getSummary, getSentimentDist, getProblems, getPositiveFeatures, getRecommendations } from '../api'
import Card, { KpiCard } from '../components/Card'
import Badge from '../components/Badge'
import Loader from '../components/Loader'
import './Dashboard.css'

const TOOLTIP_STYLE = { background: '#0e1220', border: '1px solid rgba(139,92,246,0.3)', borderRadius: 10, fontSize: 13 }
const PIE_COLORS = { positive: '#22c55e', negative: '#f43f5e', neutral: '#f59e0b' }

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [dist, setDist] = useState([])
  const [problems, setProblems] = useState([])
  const [features, setFeatures] = useState([])
  const [recs, setRecs] = useState([])

  useEffect(() => {
    getSummary().then(setSummary)
    getSentimentDist().then(setDist)
    getProblems().then(d => setProblems(d.slice(0, 8)))
    getPositiveFeatures().then(d => setFeatures(d.slice(0, 8)))
    getRecommendations().then(d => setRecs(d.slice(0, 6)))
  }, [])

  if (!summary) return <Loader />

  const barData = problems.map(p => ({ name: p.aspect.replace('_', ' '), complaints: p.complaint_count }))
  const featureData = features.map(f => ({ name: f.aspect.replace('_', ' '), praise: f.praise_count }))

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1>Customer Review Intelligence</h1>
        <p>AI-powered sentiment analysis and product insight generation</p>
      </div>

      <div className="kpi-grid">
        <KpiCard label="Total Reviews"   value={summary.total_reviews}                          color="var(--accent2)" />
        <KpiCard label="Positive"        value={`${summary.positive_pct}%`}  sub={`${summary.positive} reviews`}  color="var(--positive)" />
        <KpiCard label="Negative"        value={`${summary.negative_pct}%`}  sub={`${summary.negative} reviews`}  color="var(--negative)" />
        <KpiCard label="Avg Confidence"  value={`${(summary.avg_confidence * 100).toFixed(1)}%`}                  color="var(--neutral)" />
      </div>

      <div className="charts-row">
        <Card title="Sentiment Distribution" className="chart-card-sm">
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie
                data={dist} dataKey="value" nameKey="label"
                cx="50%" cy="50%" outerRadius={88} innerRadius={40}
                label={({ label, percent }) => `${label} ${(percent * 100).toFixed(0)}%`}
                labelLine={false}
              >
                {dist.map(d => <Cell key={d.key} fill={PIE_COLORS[d.key] || '#06b6d4'} />)}
              </Pie>
              <Tooltip contentStyle={TOOLTIP_STYLE} />
            </PieChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Top Recurring Problems" className="chart-card-lg">
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={barData} layout="vertical" margin={{ left: 10, right: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(139,92,246,0.08)" />
              <XAxis type="number" tick={{ fill: '#a78bfa', fontSize: 12 }} />
              <YAxis type="category" dataKey="name" tick={{ fill: '#a78bfa', fontSize: 12 }} width={100} />
              <Tooltip contentStyle={TOOLTIP_STYLE} />
              <Bar dataKey="complaints" fill="#f43f5e" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <div className="charts-row">
        <Card title="Top Praised Features" className="chart-card-lg">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={featureData} layout="vertical" margin={{ left: 10, right: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(139,92,246,0.08)" />
              <XAxis type="number" tick={{ fill: '#a78bfa', fontSize: 12 }} />
              <YAxis type="category" dataKey="name" tick={{ fill: '#a78bfa', fontSize: 12 }} width={100} />
              <Tooltip contentStyle={TOOLTIP_STYLE} />
              <Bar dataKey="praise" fill="#22c55e" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Sentiment Breakdown" className="chart-card-sm">
          <div className="sentiment-stats">
            {[
              { label: 'Positive', val: summary.positive, pct: summary.positive_pct, color: 'var(--positive)' },
              { label: 'Negative', val: summary.negative, pct: summary.negative_pct, color: 'var(--negative)' },
              { label: 'Neutral',  val: summary.neutral,  pct: summary.neutral_pct,  color: 'var(--neutral)' },
            ].map(s => (
              <div key={s.label} className="stat-row">
                <span className="stat-label">{s.label}</span>
                <div className="stat-bar-wrap">
                  <div className="stat-bar" style={{ width: `${s.pct || 0}%`, background: s.color }} />
                </div>
                <span className="stat-pct" style={{ color: s.color }}>{s.pct || 0}%</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <Card title="Product Improvement Recommendations">
        <div className="recs-grid">
          {recs.map((r, i) => (
            <div key={i} className="rec-card">
              <div className="rec-header">
                <span className="rec-aspect">{r.aspect.replace('_', ' ')}</span>
                <Badge label={r.severity} />
              </div>
              <p className="rec-text">{r.recommendation}</p>
              <div className="rec-stats">
                <span className="neg-stat">⚠ {r.negative_count} complaints</span>
                <span className="pos-stat">✓ {r.positive_count} praise</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
