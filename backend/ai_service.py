import os
from typing import Callable

from dotenv import load_dotenv

from prompts import ACTION_TITLES, build_prompt
from schemas import CareerProfile

load_dotenv()


def _clean_items(text: str) -> list[str]:
    separators = [",", ";", "\n", "•", "-"]
    normalized = text
    for separator in separators:
        normalized = normalized.replace(separator, ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def _sentence_join(parts: list[str]) -> str:
    return " ".join(part.strip() for part in parts if part.strip())


def _language(profile: CareerProfile) -> str:
    return "en" if profile.language == "en" else "tr"


def _role(profile: CareerProfile) -> str:
    return profile.target_position.strip() or (
        "entry-level technology role" if _language(profile) == "en" else "başlangıç seviyesi teknoloji rolü"
    )


def _name(profile: CareerProfile) -> str:
    return profile.full_name.strip() or ("The candidate" if _language(profile) == "en" else "Aday")


def _education(profile: CareerProfile) -> str:
    school = profile.school.strip()
    department = profile.department.strip()
    if school and department:
        return f"{school} {department}"
    return school or department or ("technology education" if _language(profile) == "en" else "teknoloji eğitimi")


def _top_skills(profile: CareerProfile) -> str:
    skills = _clean_items(profile.skills)
    if not skills:
        return "technical fundamentals" if _language(profile) == "en" else "temel teknik beceriler"
    return ", ".join(skills[:5])


def _project_phrase(profile: CareerProfile) -> str:
    projects = profile.projects.strip()
    if projects:
        return projects
    return "small-scale academic and personal projects" if _language(profile) == "en" else "akademik ve kişisel küçük ölçekli projeler"


def _mock_summary(profile: CareerProfile) -> str:
    if _language(profile) == "en":
        return _sentence_join(
            [
                f"{_name(profile)} is developing a career foundation in {_education(profile)}.",
                f"The candidate focuses on {_top_skills(profile)} and aims to grow in {_role(profile)}.",
                f"Project experience includes {_project_phrase(profile)}, which supports practical learning and problem solving.",
                "They are motivated to improve through structured work, clear communication, and continuous technical practice.",
            ]
        )

    return _sentence_join(
        [
            f"{_name(profile)}, {_education(profile)} alanında kendini geliştiren bir adaydır.",
            f"{_top_skills(profile)} konularında temel becerilere sahiptir ve {_role(profile)} hedefiyle ilerlemektedir.",
            f"{_project_phrase(profile)} gibi çalışmalar sayesinde teknik bilgisini uygulamalı olarak güçlendirmiştir.",
            "Düzenli çalışma, öğrenmeye açıklık ve problem çözme odağıyla profesyonel gelişimini sürdürmektedir.",
        ]
    )


def _mock_cover_letter(profile: CareerProfile) -> str:
    if _language(profile) == "en":
        return (
            f"Dear Hiring Team,\n\n"
            f"I am writing to apply for the {_role(profile)} position. My background in {_education(profile)} "
            f"and my interest in {_top_skills(profile)} have helped me build a practical foundation for this role.\n\n"
            f"Through my projects and learning experiences, including {_project_phrase(profile)}, I have improved my ability "
            f"to research, solve problems, and produce clear technical work. I am especially interested in contributing to a team "
            f"where I can keep learning while taking responsibility for real tasks.\n\n"
            f"Thank you for considering my application. I would be pleased to share more details about my work and motivation in an interview."
        )

    return (
        f"Sayın Yetkili,\n\n"
        f"{_role(profile)} pozisyonu için başvurumu iletmek isterim. {_education(profile)} alanındaki eğitimim ve "
        f"{_top_skills(profile)} konularına olan ilgim, bu pozisyon için gerekli temel yetkinlikleri geliştirmeme yardımcı oldu.\n\n"
        f"{_project_phrase(profile)} gibi çalışmalar sayesinde araştırma yapma, problem çözme ve teknik çıktılar üretme konusunda "
        f"deneyim kazandım. Kendimi geliştirebileceğim, aynı zamanda ekibe katkı sunabileceğim bir ortamda sorumluluk almak istiyorum.\n\n"
        f"Başvurumu değerlendirdiğiniz için teşekkür ederim. Çalışmalarımı ve motivasyonumu görüşmede daha detaylı paylaşmaktan memnuniyet duyarım."
    )


def _mock_linkedin(profile: CareerProfile) -> str:
    if _language(profile) == "en":
        return (
            f"I am building my career in {_education(profile)} with a focus on {_top_skills(profile)}. "
            f"I enjoy turning what I learn into practical projects and improving my technical foundation step by step.\n\n"
            f"My current goal is to grow toward {_role(profile)}. I am interested in opportunities where I can learn from real workflows, "
            f"contribute with discipline, and keep improving through feedback."
        )

    return (
        f"{_education(profile)} alanında eğitim alıyor ve özellikle {_top_skills(profile)} konularında kendimi geliştiriyorum. "
        f"Öğrendiklerimi projelere dönüştürmeyi ve teknik temelimi adım adım güçlendirmeyi önemsiyorum.\n\n"
        f"Güncel hedefim {_role(profile)} alanında gelişmek. Gerçek iş süreçlerinden öğrenebileceğim, disiplinli şekilde katkı sunabileceğim "
        f"ve geri bildirimlerle ilerleyebileceğim fırsatlara ilgi duyuyorum."
    )


def _mock_organize_skills(profile: CareerProfile) -> str:
    skills = _clean_items(profile.skills)
    lower_map = {skill.lower(): skill for skill in skills}

    categories: dict[str, list[str]] = {
        "Frontend": [],
        "Backend / Programlama": [],
        "Test Otomasyonu": [],
        "Araçlar": [],
        "Diğer": [],
    }

    for lower, original in lower_map.items():
        if any(key in lower for key in ["html", "css", "react", "javascript", "typescript", "frontend", "flutter"]):
            categories["Frontend"].append(original)
        elif any(key in lower for key in ["python", "fastapi", "node", "express", "api", "backend", "sql"]):
            categories["Backend / Programlama"].append(original)
        elif any(key in lower for key in ["playwright", "selenium", "test", "automation", "otomasyon"]):
            categories["Test Otomasyonu"].append(original)
        elif any(key in lower for key in ["git", "github", "figma", "docker", "postman"]):
            categories["Araçlar"].append(original)
        else:
            categories["Diğer"].append(original)

    if _language(profile) == "en":
        title_map = {
            "Backend / Programlama": "Backend / Programming",
            "Araçlar": "Tools",
            "Diğer": "Other",
            "Test Otomasyonu": "Test Automation",
        }
    else:
        title_map = {}

    lines = []
    for category, values in categories.items():
        if values:
            title = title_map.get(category, category)
            lines.append(f"{title}: {', '.join(values)}")
    return "\n".join(lines) or (
        "No skills were provided yet." if _language(profile) == "en" else "Henüz yetenek bilgisi girilmedi."
    )


def _mock_review(profile: CareerProfile) -> str:
    if _language(profile) == "en":
        return (
            "Strong Points\n"
            f"- The target role is clear: {_role(profile)}.\n"
            f"- Technical skills are visible, especially {_top_skills(profile)}.\n"
            "- Project information helps show practical learning.\n\n"
            "Areas to Improve\n"
            "- Add measurable details to projects, such as tools used, scope, or results.\n"
            "- Keep the experience section action-oriented with verbs like developed, tested, improved, or documented.\n"
            f"- Add role-specific keywords such as {_role(profile)}, collaboration, problem solving, Git, API, and responsive design where accurate."
        )

    return (
        "Güçlü Yönler\n"
        f"- Hedef pozisyon net görünüyor: {_role(profile)}.\n"
        f"- Teknik beceriler açık yazılmış, özellikle {_top_skills(profile)} öne çıkıyor.\n"
        "- Proje bilgileri adayın uygulamalı öğrenme sürecini destekliyor.\n\n"
        "Geliştirilmesi Gerekenler\n"
        "- Projelerde kullanılan araçlar, kapsam veya sonuç gibi ölçülebilir detaylar eklenebilir.\n"
        "- Deneyim kısmı geliştirdim, test ettim, iyileştirdim, dokümante ettim gibi eylem odaklı ifadelerle güçlendirilebilir.\n"
        f"- {_role(profile)} için uygun anahtar kelimeler, Git, API, ekip çalışması, problem çözme ve responsive tasarım gibi doğru becerilerle desteklenebilir."
    )


MOCK_GENERATORS: dict[str, Callable[[CareerProfile], str]] = {
    "summary": _mock_summary,
    "cover_letter": _mock_cover_letter,
    "linkedin": _mock_linkedin,
    "organize_skills": _mock_organize_skills,
    "review": _mock_review,
}


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
    provider = os.getenv("AI_PROVIDER", "mock").lower().strip()

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
        content = MOCK_GENERATORS[action](profile)
        used_provider = "mock"

    return {
        "action": action,
        "title": ACTION_TITLES[action],
        "content": content,
        "provider": used_provider,
    }
