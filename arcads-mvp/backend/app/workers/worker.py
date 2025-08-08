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
                try:
                    from app.core.config import settings
                    from app.utils.s3 import upload_bytes
                    # If D-ID and ElevenLabs configured, we could render here.
                    # For now, write a tiny placeholder file to S3 so signed URL works.
                    demo_key = "demo/demo.mp4"
                    upload_bytes(settings.s3_bucket, demo_key, b"demo", content_type="video/mp4")
                    video_key = demo_key
                    time.sleep(1)
                except Exception as e:
                    job.status = "failed"
                    job.error = str(e)
                    job.updated_at = datetime.utcnow()
                    db.commit()
                    continue
                video = Video(project_id=job.project_id, s3_key=video_key, duration_ms=15000)
                db.add(video)
                job.status = "completed"
                job.stage = "done"
                job.updated_at = datetime.utcnow()
                db.commit()
            else:
                time.sleep(1)

if __name__ == "__main__":
    process_jobs_forever()