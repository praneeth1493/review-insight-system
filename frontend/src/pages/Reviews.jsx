import { useEffect, useState } from 'react'
import { getReviews, getKeywords } from '../api'
import Card from '../components/Card'
import Badge from '../components/Badge'
import Loader from '../components/Loader'
import './Reviews.css'

const STARS = n => '★'.repeat(n || 0) + '☆'.repeat(5 - (n || 0))

export default function Reviews() {
  const [data, setData] = useState(null)
  const [keywords, setKeywords] = useState(null)
  const [page, setPage] = useState(1)
  const [filter, setFilter] = useState('')

  useEffect(() => {
    setData(null)
    getReviews(page, 10, filter).then(setData)
  }, [page, filter])

  useEffect(() => { getKeywords().then(setKeywords) }, [])

  const totalPages = data ? Math.ceil(data.total / 10) : 1

  return (
    <div className="reviews-page">
      <div className="page-header">
        <h1>Review Explorer</h1>
        <p>Browse and filter all classified reviews</p>
      </div>

      {/* Keyword clouds */}
      {keywords && (
        <div className="kw-row">
          {['positive', 'negative', 'neutral'].map(s => (
            <Card key={s} title={`${s} keywords`} className="kw-card">
              <div className="kw-cloud">
                {keywords[s].slice(0, 15).map(k => (
                  <span key={k.word} className={`kw-tag kw-${s}`} style={{ fontSize: `${10 + k.count / 4}px` }}>
                    {k.word}
                  </span>
                ))}
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Filter */}
      <div className="filter-bar">
        {['', 'positive', 'negative', 'neutral'].map(s => (
          <button key={s} className={`filter-btn ${filter === s ? 'active' : ''}`} onClick={() => { setFilter(s); setPage(1) }}>
            {s || 'All'}
          </button>
        ))}
        {data && <span className="total-count">{data.total} reviews</span>}
      </div>

      {/* Reviews list */}
      {!data ? <Loader /> : (
        <div className="reviews-list">
          {data.reviews.map(r => (
            <div key={r.review_id} className="review-card">
              <div className="review-top">
                <div className="review-meta">
                  <span className="stars" style={{ color: r.rating >= 4 ? '#f59e0b' : r.rating <= 2 ? '#ef4444' : '#8b90b8' }}>
                    {STARS(r.rating)}
                  </span>
                  <Badge label={r.predicted_sentiment} />
                  <span className="confidence">conf: {(r.sentiment_confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="review-aspects">
                  {(r.aspects || []).map(a => (
                    <span key={a} className="aspect-tag">{a.replace('_', ' ')}</span>
                  ))}
                </div>
              </div>
              <p className="review-text">{r.text}</p>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      <div className="pagination">
        <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>← Prev</button>
        <span>Page {page} of {totalPages}</span>
        <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)}>Next →</button>
      </div>
    </div>
  )
}
