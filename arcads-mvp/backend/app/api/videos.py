from fastapi import APIRouter

router = APIRouter()

@router.get("/videos/{video_id}/signed-url")
def get_signed_url(video_id: int):
    # For MVP, return a public demo URL. Integrate boto3 generate_presigned_url later.
    return {"url": "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"}