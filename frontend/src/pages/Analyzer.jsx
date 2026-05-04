import { useState } from 'react'
import { analyzeText } from '../api'
import Card from '../components/Card'
import Badge from '../components/Badge'
import './Analyzer.css'

const SAMPLES = [
  "The battery life on this phone is absolutely incredible. Lasts two full days!",
  "Camera is blurry and washed out. Terrible in any lighting condition.",
  "Great camera but the battery life is disappointing for the price.",
  "Customer service was rude and unhelpful. Refused to honor the warranty.",
  "Noise cancellation is top notch. Perfect for working from home.",
]

export default function Analyzer() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const analyze = async () => {
    if (!text.trim()) return
    setLoading(true); setError(''); setResult(null)
    try {
      const r = await analyzeText(text)
      setResult(r)
    } catch {
      setError('Could not connect to API. Make sure the Flask server is running on port 5000.')
    } finally {
      setLoading(false)
    }
  }

  const sentColor = { positive: '#22c55e', negative: '#f43f5e', neutral: '#f59e0b' }
  const sentEmoji = { positive: '😊', negative: '😞', neutral: '😐' }

  return (
    <div className="analyzer-page">
      <div className="page-header">
        <h1>Live Review Analyzer</h1>
        <p>Type or paste any review text to get instant AI-powered insights</p>
      </div>

      <Card title="Input Review">
        <textarea
          className="review-input"
          placeholder="Type or paste a product review here..."
          value={text}
          onChange={e => setText(e.target.value)}
          rows={5}
        />
        <div className="input-actions">
          <div className="samples">
            <span className="samples-label">Try a sample:</span>
            {SAMPLES.map((s, i) => (
              <button key={i} className="sample-btn" onClick={() => setText(s)}>#{i + 1}</button>
            ))}
          </div>
          <button className="analyze-btn" onClick={analyze} disabled={loading || !text.trim()}>
            {loading ? '⏳ Analyzing...' : '⚡ Analyze'}
          </button>
        </div>
        {error && <p className="error-msg">{error}</p>}
      </Card>

      {result && (
        <div className="results-grid">
          <Card title="Sentiment Result">
            <div className="sentiment-result">
              <div className="sentiment-big" style={{ color: sentColor[result.sentiment] }}>
                <span style={{ fontSize: 48 }}>{sentEmoji[result.sentiment]}</span>
                <span>{result.sentiment.toUpperCase()}</span>
              </div>
              <div className="confidence-ring">
                <svg viewBox="0 0 80 80" width="88" height="88">
                  <circle cx="40" cy="40" r="32" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="8" />
                  <circle
                    cx="40" cy="40" r="32" fill="none"
                    stroke={sentColor[result.sentiment]} strokeWidth="8"
                    strokeDasharray={`${result.confidence * 201} 201`}
                    strokeLinecap="round"
                    transform="rotate(-90 40 40)"
                    style={{ filter: `drop-shadow(0 0 6px ${sentColor[result.sentiment]})` }}
                  />
                </svg>
                <span className="ring-label">{(result.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>
          </Card>

          <Card title="Detected Aspects">
            <div className="aspect-results">
              {Object.entries(result.aspect_sentiments).map(([aspect, sentiment]) => (
                <div key={aspect} className="aspect-result-row">
                  <span className="aspect-result-name">{aspect.replace('_', ' ')}</span>
                  <Badge label={sentiment} />
                </div>
              ))}
            </div>
          </Card>

          <Card title="Extracted Keywords">
            <div className="keyword-results">
              {result.keywords.map(kw => (
                <span key={kw} className="kw-result-tag">{kw}</span>
              ))}
            </div>
          </Card>
        </div>
      )}

      {result && (
        <Card title="Original Text">
          <p className="analyzed-text">"{result.text}"</p>
        </Card>
      )}
    </div>
  )
}
