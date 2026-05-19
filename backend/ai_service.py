import os

from dotenv import load_dotenv

from prompts import ACTION_TITLES, build_prompt
from schemas import CareerProfile

load_dotenv()


async def _generate_openai(action: str, profile: CareerProfile) -> str:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    prompt = build_prompt(action, profile)
    response = await client.chat.completions.create(
        model=model,
        temperature=0.4,
        messages=[
            {
                "role": "system",
                "content": "Sen profesyonel, dürüst ve kullanıcıya gerçek dışı bilgi eklemeyen bir kariyer danışmanısın.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


async def _generate_groq(action: str, profile: CareerProfile) -> str:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    prompt = build_prompt(action, profile)
    response = await client.chat.completions.create(
        model=model,
        temperature=0.4,
        messages=[
            {
                "role": "system",
                "content": "Sen profesyonel, dürüst ve kullanıcıya gerçek dışı bilgi eklemeyen bir kariyer danışmanısın.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


async def _generate_gemini(action: str, profile: CareerProfile) -> str:
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))
    response = await model.generate_content_async(build_prompt(action, profile))
    return response.text.strip()


async def generate_content(action: str, profile: CareerProfile) -> dict[str, str]:
    provider = os.getenv("AI_PROVIDER", "groq").lower().strip()

    if provider == "openai" and os.getenv("OPENAI_API_KEY"):
        content = await _generate_openai(action, profile)
        used_provider = "openai"
    elif provider == "groq" and os.getenv("GROQ_API_KEY"):
        content = await _generate_groq(action, profile)
        used_provider = "groq"
    elif provider == "gemini" and os.getenv("GEMINI_API_KEY"):
        content = await _generate_gemini(action, profile)
        used_provider = "gemini"
    else:
        raise ValueError(
            "Geçerli bir yapay zekâ sağlayıcısı bulunamadı. "
            "AI_PROVIDER değerini groq, openai veya gemini yapın ve ilgili API anahtarını .env dosyasına ekleyin."
        )

    return {
        "action": action,
        "title": ACTION_TITLES[action],
        "content": content,
        "provider": used_provider,
    }
