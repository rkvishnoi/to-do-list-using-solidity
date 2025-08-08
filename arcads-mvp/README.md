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
- Providers (ElevenLabs, D-ID/HeyGen) are stubbed. Add keys in `.env` and wire real calls in `app/api` and `app/workers`.
- Videos use a sample URL until integration is completed.

## Structure
```
frontend/
backend/
scripts/
```