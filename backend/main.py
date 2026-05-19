import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ai_service import generate_content
from schemas import GenerateRequest, GenerateResponse

load_dotenv()


def _allowed_origins() -> list[str]:
    raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(
    title="AI Destekli CV ve Ön Yazı Asistanı",
    description="CV özeti, ön yazı ve LinkedIn açıklaması üreten FastAPI servisi.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "CareerCraft AI backend çalışıyor."}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    try:
        result = await generate_content(request.action, request.profile)
        return GenerateResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Metin üretilemedi: {exc}") from exc

