from fastapi import APIRouter

router = APIRouter()

@router.get("/videos/{video_id}/signed-url")
def get_signed_url(video_id: int):
    # Placeholder: in production, look up by video_id. For demo, sign a fixed key.
    from app.utils.s3 import generate_presigned_url
    from app.core.config import settings
    url = generate_presigned_url(settings.s3_bucket, "demo/demo.mp4", expires_in=900)
    return {"url": url}