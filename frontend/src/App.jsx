import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [file, setFile] = useState(null)
  const [email, setEmail] = useState('')
  const [meetings, setMeetings] = useState([])
  const [uploading, setUploading] = useState(false)

  const fetchMeetings = async () => {
    try {
      const res = await axios.get(`${API_URL}/meetings`)
      setMeetings(res.data.reverse())
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchMeetings()
    const interval = setInterval(fetchMeetings, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)
    if (email) formData.append('email_to', email)

    setUploading(true)
    try {
      await axios.post(`${API_URL}/meetings/upload`, formData)
      setFile(null)
      setEmail('')
      document.getElementById('fileInput').value = ''
      fetchMeetings()
    } catch (err) {
      alert('Upload failed')
      console.error(err)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>MeetMind</h1>
        <p>Upload a meeting recording. Get transcript, summary, and action items — automatically.</p>
      </header>

      <form className="upload-card" onSubmit={handleUpload}>
        <input
          id="fileInput"
          type="file"
          accept="audio/*,video/*"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <input
          type="email"
          placeholder="Email to send summary (optional)"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button type="submit" disabled={uploading || !file}>
          {uploading ? 'Uploading...' : 'Upload Meeting'}
        </button>
      </form>

      <section className="meetings-list">
        {meetings.length === 0 && <p className="empty">No meetings yet.</p>}
        {meetings.map((m) => (
          <div key={m.id} className={`meeting-card status-${m.status}`}>
            <div className="meeting-header">
              <h3>{m.title}</h3>
              <span className={`badge badge-${m.status}`}>{m.status}</span>
            </div>
            {m.summary && (
              <div className="meeting-body">
                <strong>Summary:</strong>
                <p>{m.summary}</p>
                <strong>Action Items:</strong>
                <p>{m.action_items}</p>
              </div>
            )}
          </div>
        ))}
      </section>
    </div>
  )
}

export default App