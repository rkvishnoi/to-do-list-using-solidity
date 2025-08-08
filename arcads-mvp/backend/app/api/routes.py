from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import SessionLocal, Base, engine
from app.schemas.schemas import ProjectIn, ProjectOut, ScriptIn, ScriptOut, JobCreate, JobOut, VoicePreviewIn, AvatarsOut
from app.models.models import Script, Job, Project
from datetime import datetime

api_router = APIRouter()

# Ensure tables exist (simple for MVP)
Base.metadata.create_all(bind=engine)

# Sub-routers
from app.api.videos import router as videos_router
api_router.include_router(videos_router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@api_router.post("/projects", response_model=ProjectOut)
def create_project(payload: ProjectIn, db: Session = Depends(get_db)):
    project = Project(name=payload.name, user_id=1)
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectOut(id=project.id, name=project.name)

@api_router.get("/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return [ProjectOut(id=p.id, name=p.name) for p in projects]

@api_router.post("/scripts", response_model=ScriptOut)
def create_script(payload: ScriptIn, db: Session = Depends(get_db)):
    script = Script(project_id=payload.project_id, language=payload.language, text=payload.text)
    db.add(script)
    db.commit()
    db.refresh(script)
    return ScriptOut(id=script.id, project_id=script.project_id, language=script.language, text=script.text, version=script.version)

@api_router.post("/jobs", response_model=JobOut)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    job = Job(project_id=payload.project_id, status="queued", stage="submitted", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(job)
    db.commit()
    db.refresh(job)
    # Enqueue using Redis/RQ would go here; for MVP, we simulate async worker
    return JobOut(id=job.id, status=job.status, stage=job.stage)

@api_router.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobOut(id=job.id, status=job.status, stage=job.stage, error=job.error)

@api_router.post("/voices/preview")
def voice_preview(payload: VoicePreviewIn):
    # Stub: return a demo MP3 URL
    return {"url": "https://file-examples.com/storage/fe5fbf0a7c039f03adcf9f3/2017/11/file_example_MP3_700KB.mp3"}

@api_router.get("/avatars", response_model=list[AvatarsOut])
def list_avatars():
    return [
        {"id": "demo1", "name": "Alex", "thumbnail_url": "https://picsum.photos/seed/alex/200"},
        {"id": "demo2", "name": "Jamie", "thumbnail_url": "https://picsum.photos/seed/jamie/200"},
    ]