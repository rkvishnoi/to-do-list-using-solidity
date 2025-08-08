# Arcads-like MVP

An MVP SaaS that generates UGC-style video ads using a stubbed pipeline: script generation, TTS preview, avatar selection, render job queue, and S3 delivery via MinIO.

## Stack
- Frontend: Next.js (App Router, TypeScript), NextAuth (Credentials), Tailwind
- Backend: FastAPI, SQLAlchemy, PostgreSQL, Redis + RQ worker
- Storage: MinIO (S3-compatible)

## Quick start (Docker)
1. Copy envs
```bash
cp .env.example .env
```
2. Start services
```bash
docker compose up -d --build
```
3. Open
- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs
- MinIO console: http://localhost:9001 (admin/admin)

## Local development
- Frontend runs dev server (hot reload)
- Backend auto-reloads with Uvicorn
- Worker processes render jobs

## Notes
- ElevenLabs preview integrated: set `ELEVENLABS_API_KEY` (and optional `ELEVENLABS_DEFAULT_VOICE_ID`). Previews are uploaded to S3/MinIO and served via presigned URL.
- D-ID client scaffolded: set `DID_API_KEY` to enable talking-head renders in the worker (currently placeholder upload; wire real flow as needed).
- S3/MinIO: set `S3_ENDPOINT_URL`, `S3_BUCKET`, and AWS credentials. Bucket will auto-create on first upload.

## Structure
```
frontend/
backend/
scripts/
```