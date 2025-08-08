import boto3
from botocore.client import Config as BotoConfig
from botocore.exceptions import ClientError
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


def ensure_bucket(bucket: str) -> None:
    try:
        _s3.head_bucket(Bucket=bucket)
    except ClientError:
        params = {"Bucket": bucket}
        # Some S3 providers require LocationConstraint when not us-east-1
        if settings.aws_region and settings.aws_region != "us-east-1" and not settings.s3_endpoint_url:
            params["CreateBucketConfiguration"] = {"LocationConstraint": settings.aws_region}
        _s3.create_bucket(**params)


def upload_bytes(bucket: str, key: str, data: bytes, content_type: str = "application/octet-stream") -> None:
    try:
        _s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") in {"NoSuchBucket", "404"}:
            ensure_bucket(bucket)
            _s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
        else:
            raise


def generate_presigned_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    return _s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )