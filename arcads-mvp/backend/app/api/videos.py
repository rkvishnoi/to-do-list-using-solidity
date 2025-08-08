from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.models import Video

router = APIRouter()

@router.get("/videos/{video_id}/signed-url")
def get_signed_url(video_id: int):
    with SessionLocal() as db:
        video = db.get(Video, video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        from app.utils.s3 import generate_presigned_url
        from app.core.config import settings
        url = generate_presigned_url(settings.s3_bucket, video.s3_key, expires_in=900)
        return {"url": url}