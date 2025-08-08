import time
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.models import Job, Video
from datetime import datetime


def process_jobs_forever():
    while True:
        with SessionLocal() as db:
            job = (
                db.query(Job)
                .filter(Job.status == "queued")
                .order_by(Job.created_at.asc())
                .first()
            )
            if job:
                job.status = "processing"
                job.stage = "rendering"
                job.updated_at = datetime.utcnow()
                db.commit()
                # Simulate work
                time.sleep(2)
                # Create a demo video row
                video = Video(project_id=job.project_id, s3_key="demo/demo.mp4", duration_ms=15000)
                db.add(video)
                job.status = "completed"
                job.stage = "done"
                job.updated_at = datetime.utcnow()
                db.commit()
            else:
                time.sleep(1)

if __name__ == "__main__":
    process_jobs_forever()