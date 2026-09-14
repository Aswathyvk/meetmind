from fastapi import FastAPI, UploadFile, File, Depends, BackgroundTasks, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas
import shutil, os
from transcription import transcribe_meeting

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MeetMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"status": "MeetMind API running"}

@app.post("/meetings/upload", response_model=schemas.MeetingOut)
def upload_meeting(background_tasks: BackgroundTasks, file: UploadFile = File(...), email_to: str = Form(None), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    meeting = models.Meeting(
        title=file.filename,
        audio_filename=file.filename,
        email_to=email_to,
        status="uploaded"
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    background_tasks.add_task(transcribe_meeting, meeting.id, file_path)

    return meeting

@app.get("/meetings", response_model=list[schemas.MeetingOut])
def list_meetings(db: Session = Depends(get_db)):
    return db.query(models.Meeting).all()