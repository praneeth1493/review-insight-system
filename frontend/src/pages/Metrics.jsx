import { useEffect, useState } from 'react'
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'
import { getMetrics } from '../api'
import Card, { KpiCard } from '../components/Card'
import Loader from '../components/Loader'
import './Metrics.css'

const TOOLTIP_STYLE = { background: '#0e1220', border: '1px solid rgba(139,92,246,0.3)', borderRadius: 10, fontSize: 13 }

export default function Metrics() {
  const [m, setM] = useState(null)
  useEffect(() => { getMetrics().then(setM) }, [])
  if (!m) return <Loader />

  const radarData = Object.entries(m.per_class).map(([label, v]) => ({
    label: label.charAt(0).toUpperCase() + label.slice(1),
    Precision: +(v.precision * 100).toFixed(1),
    Recall: +(v.recall * 100).toFixed(1),
    F1: +(v.f1 * 100).toFixed(1),
  }))

  const barData = Object.entries(m.per_class).map(([label, v]) => ({
    name: label,
    Precision: +(v.precision * 100).toFixed(1),
    Recall: +(v.recall * 100).toFixed(1),
    F1: +(v.f1 * 100).toFixed(1),
    Support: v.support,
  }))

  const labels = m.confusion_labels || []
  const cm = m.confusion_matrix || []

  return (
    <div className="metrics-page">
      <div className="page-header">
        <h1>Model Evaluation</h1>
        <p>Accuracy, precision, recall and F1-score across all sentiment classes</p>
      </div>

      <div className="kpi-grid">
        <KpiCard label="Accuracy"          value={`${(m.accuracy * 100).toFixed(1)}%`}         color="var(--accent2)" />
        <KpiCard label="Precision (macro)" value={`${(m.precision_macro * 100).toFixed(1)}%`}  color="var(--positive)" />
        <KpiCard label="Recall (macro)"    value={`${(m.recall_macro * 100).toFixed(1)}%`}     color="var(--neutral)" />
        <KpiCard label="F1 (weighted)"     value={`${(m.f1_weighted * 100).toFixed(1)}%`}      color="var(--negative)" />
      </div>

      <div className="metrics-row">
        <Card title="Per-Class Metrics (Radar)" className="radar-card">
          <ResponsiveContainer width="100%" height={280}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="rgba(139,92,246,0.2)" />
              <PolarAngleAxis dataKey="label" tick={{ fill: '#a78bfa', fontSize: 12 }} />
              <Radar name="Precision" dataKey="Precision" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.2} />
              <Radar name="Recall"    dataKey="Recall"    stroke="#22c55e" fill="#22c55e" fillOpacity={0.2} />
              <Radar name="F1"        dataKey="F1"        stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.2} />
              <Tooltip contentStyle={TOOLTIP_STYLE} />
            </RadarChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Per-Class Bar Comparison" className="bar-card">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(139,92,246,0.08)" />
              <XAxis dataKey="name" tick={{ fill: '#a78bfa', fontSize: 12 }} />
              <YAxis domain={[0, 100]} tick={{ fill: '#a78bfa', fontSize: 12 }} unit="%" />
              <Tooltip contentStyle={TOOLTIP_STYLE} formatter={v => `${v}%`} />
              <Bar dataKey="Precision" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Recall"    fill="#22c55e" radius={[4, 4, 0, 0]} />
              <Bar dataKey="F1"        fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <Card title="Confusion Matrix">
        <div className="cm-wrap">
          <table className="cm-table">
            <thead>
              <tr>
                <th className="cm-corner">Actual ↓ / Predicted →</th>
                {labels.map(l => <th key={l} className="cm-head">{l}</th>)}
              </tr>
            </thead>
            <tbody>
              {cm.map((row, i) => {
                const rowSum = row.reduce((a, b) => a + b, 0)
                return (
                  <tr key={i}>
                    <td className="cm-row-label">{labels[i]}</td>
                    {row.map((val, j) => {
                      const intensity = rowSum > 0 ? val / rowSum : 0
                      const isDiag = i === j
                      return (
                        <td key={j} className="cm-cell" style={{
                          background: isDiag
                            ? `rgba(139,92,246,${0.12 + intensity * 0.7})`
                            : `rgba(244,63,94,${intensity * 0.5})`,
                          color: intensity > 0.4 ? '#fff' : 'var(--text)',
                          fontWeight: isDiag ? 800 : 400,
                        }}>
                          {val}
                        </td>
                      )
                    })}
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </Card>

      <Card title="Per-Class Detail">
        <table className="detail-table">
          <thead>
            <tr><th>Class</th><th>Precision</th><th>Recall</th><th>F1 Score</th><th>Support</th></tr>
          </thead>
          <tbody>
            {Object.entries(m.per_class).map(([label, v]) => (
              <tr key={label}>
                <td className="class-label">{label}</td>
                <td><MetricBar value={v.precision} color="#8b5cf6" /></td>
                <td><MetricBar value={v.recall}    color="#22c55e" /></td>
                <td><MetricBar value={v.f1}        color="#f59e0b" /></td>
                <td className="support">{v.support}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  )
}

function MetricBar({ value, color }) {
  return (
    <div className="metric-bar-cell">
      <div className="metric-bar-bg">
        <div className="metric-bar-fill" style={{ width: `${value * 100}%`, background: color }} />
      </div>
      <span style={{ color }}>{(value * 100).toFixed(1)}%</span>
    </div>
  )
}
