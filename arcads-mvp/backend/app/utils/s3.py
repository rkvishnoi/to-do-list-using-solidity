import boto3
from botocore.client import Config as BotoConfig
from app.core.config import settings

_session = boto3.session.Session(
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region,
)

_s3 = _session.client(
    "s3",
    endpoint_url=settings.s3_endpoint_url,
    config=BotoConfig(signature_version="s3v4"),
)


def upload_bytes(bucket: str, key: str, data: bytes, content_type: str = "application/octet-stream") -> None:
    _s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)


def generate_presigned_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    return _s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )