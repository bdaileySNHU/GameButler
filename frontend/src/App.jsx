import { useState } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = 'http://localhost:8000'

function App() {
  const [recommendation, setRecommendation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [uploadMsg, setUploadMsg] = useState('')
  
  // Filters
  const [genre, setGenre] = useState('')
  const [tag, setTag] = useState('')
  const [length, setLength] = useState('') // short, medium, long
  const [unplayed, setUnplayed] = useState(false)

  const handleUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      setLoading(true)
      const res = await axios.post(`${API_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setUploadMsg(`Success! Loaded ${res.data.games_count} games.`)
      setError(null)
    } catch (err) {
      setError('Upload failed.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getRecommendation = async () => {
    setLoading(true)
    setError(null)
    setRecommendation(null)

    try {
      const params = {}
      if (genre) params.genre = genre
      if (tag) params.tag = tag
      if (length) params.length = length
      if (unplayed) params.unplayed_only = true

      const res = await axios.get(`${API_URL}/recommend`, { params })
      setRecommendation(res.data)
    } catch (err) {
      if (err.response && err.response.status === 404) {
        setError('No game found matching your criteria.')
      } else {
        setError('Failed to get recommendation.')
      }
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <h1>🎩 GameButler</h1>
        <p>Your personal gaming concierge.</p>
      </header>

      <main>
        <section className="card upload-section">
          <h2>1. Update Library</h2>
          <input type="file" accept=".csv" onChange={handleUpload} />
          {uploadMsg && <p className="success-msg">{uploadMsg}</p>}
        </section>

        <section className="card filter-section">
          <h2>2. Preferences</h2>
          
          <div className="filter-group">
            <label>Genre:</label>
            <input 
              type="text" 
              placeholder="e.g. Action" 
              value={genre} 
              onChange={(e) => setGenre(e.target.value)} 
            />
          </div>

          <div className="filter-group">
            <label>Tag:</label>
            <input 
              type="text" 
              placeholder="e.g. Sci-Fi" 
              value={tag} 
              onChange={(e) => setTag(e.target.value)} 
            />
          </div>

          <div className="filter-group">
            <label>Length:</label>
            <select value={length} onChange={(e) => setLength(e.target.value)}>
              <option value="">Any Length</option>
              <option value="short">Short (&lt; 5h)</option>
              <option value="medium">Medium (5h - 20h)</option>
              <option value="long">Long (&gt; 20h)</option>
            </select>
          </div>

          <div className="filter-group checkbox">
            <label>
              <input 
                type="checkbox" 
                checked={unplayed} 
                onChange={(e) => setUnplayed(e.target.checked)} 
              />
              Unplayed Only
            </label>
          </div>

          <button className="primary-btn" onClick={getRecommendation} disabled={loading}>
            {loading ? 'Consulting...' : 'Recommend a Game'}
          </button>
        </section>

        {error && <div className="error-card">{error}</div>}

        {recommendation && (
          <section className="result-card">
            <h3>I recommend:</h3>
            <div className="game-title">{recommendation.Name}</div>
            <div className="game-details">
              <span className="badge">{recommendation.Genre}</span>
              <span className="badge secondary">{recommendation.Tags.split(';')[0]}</span>
            </div>
            <p><strong>Playtime:</strong> {recommendation.Playtime_Forever} mins</p>
            {recommendation.Average_Playtime && (
              <p><strong>Est. Length:</strong> {recommendation.Average_Playtime} mins</p>
            )}
          </section>
        )}
      </main>
    </div>
  )
}

export default App