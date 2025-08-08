from pydantic import BaseModel, Field
from typing import Optional, Literal

class ScriptIn(BaseModel):
    project_id: int
    language: str = "en"
    text: str

class ScriptOut(BaseModel):
    id: int
    project_id: int
    language: str
    text: str
    version: int

class JobCreate(BaseModel):
    project_id: int
    script_id: int
    voice_id: Optional[str] = None
    avatar_id: Optional[str] = None
    style: Optional[str] = None

class JobOut(BaseModel):
    id: int
    status: str
    stage: Optional[str] = None
    error: Optional[str] = None

class VoicePreviewIn(BaseModel):
    text: str = Field(min_length=1, max_length=400)
    voice_id: Optional[str] = None
    language: Optional[str] = "en"

class AvatarsOut(BaseModel):
    id: str
    name: str
    thumbnail_url: str