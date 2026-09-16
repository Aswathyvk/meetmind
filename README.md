# 🧠 MeetMind

**AI-powered meeting assistant** that transcribes recordings, generates summaries and action items, and emails them automatically — no manual note-taking required.

🔗 **Live Demo:** [meetmind-frontend-e5lm.onrender.com](https://meetmind-frontend-e5lm.onrender.com)

---

## ✨ Features

- 🎙️ **Upload any recording** — audio or video (mp3, wav, mp4, etc.)
- 📝 **Automatic transcription** powered by [faster-whisper](https://github.com/SYSTRAN/faster-whisper), running locally at zero API cost
- 🤖 **AI summarization** via [Groq](https://groq.com) — concise summary + extracted action items
- 📧 **Automated email delivery** through [Resend](https://resend.com)
- ⚡ **Live status tracking** — watch progress from `uploaded → processing → done` in real time
- 🎨 **Custom dark UI** built with React + Vite

---

## 🏗️ Architecture

```mermaid
flowchart TD
    A[React Frontend] -->|POST /meetings/upload| B[FastAPI Backend]
    B -->|triggers background task| C[Processing Pipeline]
    C --> D[1. faster-whisper<br/>transcribes audio]
    D --> E[2. Groq API<br/>generates summary + action items]
    E --> F[3. Resend API<br/>emails the summary]
    B --> G[(SQLite Database<br/>status, transcript, summary, action items)]
```
(status, transcript,
summary, action items)
