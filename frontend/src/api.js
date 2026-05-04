import axios from 'axios'

// Uses VITE_API_URL env variable in production (Vercel)
// Falls back to localhost:5000 in development
const BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : 'http://localhost:5000/api'

export const getSummary            = () => axios.get(`${BASE}/summary`).then(r => r.data)
export const getSentimentDist      = () => axios.get(`${BASE}/sentiment-distribution`).then(r => r.data)
export const getAspectSummary      = () => axios.get(`${BASE}/aspect-summary`).then(r => r.data)
export const getProblems           = () => axios.get(`${BASE}/problems`).then(r => r.data)
export const getPositiveFeatures   = () => axios.get(`${BASE}/positive-features`).then(r => r.data)
export const getRecommendations    = () => axios.get(`${BASE}/recommendations`).then(r => r.data)
export const getKeywords           = () => axios.get(`${BASE}/keywords`).then(r => r.data)
export const getMetrics            = () => axios.get(`${BASE}/metrics`).then(r => r.data)
export const getReviews            = (page = 1, perPage = 10, sentiment = '') =>
  axios.get(`${BASE}/reviews`, { params: { page, per_page: perPage, sentiment } }).then(r => r.data)
export const analyzeText           = (text) =>
  axios.post(`${BASE}/analyze`, { text }).then(r => r.data)
