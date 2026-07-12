import { useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/analyze'

function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const onSubmit = async (event) => {
    event.preventDefault()
    if (!file) {
      setError('Please select an image first.')
      return
    }

    setLoading(true)
    setError('')

    const formData = new FormData()
    formData.append('image', file)
    formData.append('crop', 'Rice')

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      })
      const payload = await response.json()
      if (!response.ok) {
        throw new Error(payload.detail ?? 'Unable to process image')
      }
      setResult(payload)
    } catch (submitError) {
      setError(submitError.message)
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page">
      <h1>AgriGuard AI</h1>
      <p className="subtitle">Upload a crop image to detect insects and receive treatment guidance.</p>

      <form onSubmit={onSubmit} className="card">
        <input
          type="file"
          accept="image/*"
          onChange={(event) => setFile(event.target.files?.[0] ?? null)}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze image'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <section className="card result">
          <h2>Analysis summary</h2>
          <p><strong>Total insects:</strong> {result.insect_count}</p>
          <p><strong>Infestation severity:</strong> {result.infestation_severity}</p>
          <p><strong>Pesticide recommendation:</strong> {result.pesticide.message}</p>
          <p>
            <strong>Economic decision:</strong>{' '}
            {result.cost_benefit.economically_worthwhile ? 'Spraying is economically worthwhile.' : 'Spraying is not economically worthwhile.'}
          </p>

          <h3>Detected insects</h3>
          <ul>
            {result.detections.map((item, index) => (
              <li key={`${item.label}-${index}`}>
                {item.label} ({item.impact}) - confidence: {item.confidence}
              </li>
            ))}
          </ul>

          <img
            src={`data:image/jpeg;base64,${result.annotated_image_base64}`}
            alt="Annotated crop with insect detections"
            className="annotated"
          />
        </section>
      )}
    </main>
  )
}

export default App
