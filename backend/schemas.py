from typing import Literal

from pydantic import BaseModel, Field


class CareerProfile(BaseModel):
    full_name: str = Field(default="", max_length=120)
    school: str = Field(default="", max_length=180)
    department: str = Field(default="", max_length=180)
    skills: str = Field(default="", max_length=1400)
    experiences: str = Field(default="", max_length=1800)
    projects: str = Field(default="", max_length=1800)
    certificates: str = Field(default="", max_length=1200)
    target_position: str = Field(default="", max_length=160)
    language: Literal["tr", "en"] = "tr"
    tone: Literal["resmi", "sade", "etkileyici"] = "sade"


class GenerateRequest(BaseModel):
    action: Literal[
        "summary",
        "cover_letter",
        "linkedin",
        "organize_skills",
        "review",
    ]
    profile: CareerProfile


class GenerateResponse(BaseModel):
    action: str
    title: str
    content: str
    provider: str

