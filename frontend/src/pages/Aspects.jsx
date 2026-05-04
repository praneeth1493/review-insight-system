import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, Radar, PolarGrid, PolarAngleAxis } from 'recharts'
import { getAspectSummary } from '../api'
import Card from '../components/Card'
import Loader from '../components/Loader'
import './Aspects.css'

const TOOLTIP_STYLE = { background: '#0e1220', border: '1px solid rgba(139,92,246,0.3)', borderRadius: 10, fontSize: 13 }

export default function Aspects() {
  const [data, setData] = useState([])

  useEffect(() => { getAspectSummary().then(setData) }, [])
  if (!data.length) return <Loader />

  const stackData = data.map(d => ({
    name: d.aspect.replace('_', ' '),
    Positive: d.positive || 0,
    Neutral: d.neutral || 0,
    Negative: d.negative || 0,
  }))

  const scoreData = data.map(d => ({
    aspect: d.aspect.replace('_', ' '),
    score: d.sentiment_score,
    total: d.total,
  })).sort((a, b) => b.score - a.score)

  const radarData = data.slice(0, 8).map(d => ({
    aspect: d.aspect.replace('_', ' '),
    score: Math.round(((d.sentiment_score + 1) / 2) * 100),
  }))

  return (
    <div className="aspects-page">
      <div className="page-header">
        <h1>Aspect Analysis</h1>
        <p>Sentiment breakdown across 12 product dimensions</p>
      </div>

      <Card title="Stacked Sentiment by Aspect">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={stackData} margin={{ bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(139,92,246,0.08)" />
            <XAxis dataKey="name" tick={{ fill: '#a78bfa', fontSize: 11 }} angle={-25} textAnchor="end" />
            <YAxis tick={{ fill: '#a78bfa', fontSize: 12 }} />
            <Tooltip contentStyle={TOOLTIP_STYLE} />
            <Legend wrapperStyle={{ color: '#a78bfa', fontSize: 13 }} />
            <Bar dataKey="Positive" stackId="a" fill="#22c55e" />
            <Bar dataKey="Neutral"  stackId="a" fill="#f59e0b" />
            <Bar dataKey="Negative" stackId="a" fill="#f43f5e" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </Card>

      <div className="aspects-row">
        <Card title="Sentiment Score per Aspect (−1 to +1)" className="score-card">
          <div className="score-list">
            {scoreData.map(d => (
              <div key={d.aspect} className="score-row">
                <span className="score-name">{d.aspect}</span>
                <div className="score-bar-wrap">
                  <div className="score-zero" />
                  <div
                    className="score-bar"
                    style={{
                      width: `${Math.abs(d.score) * 50}%`,
                      background: d.score >= 0 ? '#22c55e' : '#f43f5e',
                      marginLeft: d.score >= 0 ? '50%' : `${50 - Math.abs(d.score) * 50}%`,
                    }}
                  />
                </div>
                <span className="score-val" style={{ color: d.score >= 0 ? '#22c55e' : '#f43f5e' }}>
                  {d.score > 0 ? '+' : ''}{d.score.toFixed(2)}
                </span>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Aspect Health Radar" className="radar-card">
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="rgba(139,92,246,0.2)" />
              <PolarAngleAxis dataKey="aspect" tick={{ fill: '#a78bfa', fontSize: 11 }} />
              <Radar name="Health Score" dataKey="score" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.3} />
              <Tooltip contentStyle={TOOLTIP_STYLE} />
            </RadarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <Card title="Aspect Detail Table">
        <table className="aspect-table">
          <thead>
            <tr>
              <th>Aspect</th><th>Total</th><th>Positive</th><th>Neutral</th><th>Negative</th><th>Score</th>
            </tr>
          </thead>
          <tbody>
            {data.map(d => (
              <tr key={d.aspect}>
                <td className="aspect-name">{d.aspect.replace('_', ' ')}</td>
                <td>{d.total}</td>
                <td className="pos">{d.positive || 0}</td>
                <td className="neu">{d.neutral || 0}</td>
                <td className="neg">{d.negative || 0}</td>
                <td style={{ color: d.sentiment_score >= 0 ? '#22c55e' : '#f43f5e', fontWeight: 700 }}>
                  {d.sentiment_score > 0 ? '+' : ''}{d.sentiment_score?.toFixed(3)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  )
}
