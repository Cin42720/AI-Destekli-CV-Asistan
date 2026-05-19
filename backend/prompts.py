from schemas import CareerProfile


ACTION_TITLES = {
    "summary": "CV Özeti",
    "cover_letter": "Ön Yazı",
    "linkedin": "LinkedIn Açıklaması",
    "organize_skills": "Yetenekleri Düzenle",
    "review": "CV Analizi",
}


def _language_name(code: str) -> str:
    return "İngilizce" if code == "en" else "Türkçe"


def profile_to_text(profile: CareerProfile) -> str:
    return f"""
Ad Soyad: {profile.full_name or "Belirtilmedi"}
Okul: {profile.school or "Belirtilmedi"}
Bölüm: {profile.department or "Belirtilmedi"}
Yetenekler: {profile.skills or "Belirtilmedi"}
Deneyimler: {profile.experiences or "Belirtilmedi"}
Projeler: {profile.projects or "Belirtilmedi"}
Sertifikalar: {profile.certificates or "Belirtilmedi"}
Başvurulan Pozisyon: {profile.target_position or "Belirtilmedi"}
Dil: {_language_name(profile.language)}
Ton: {profile.tone}
""".strip()


def build_prompt(action: str, profile: CareerProfile) -> str:
    base = profile_to_text(profile)
    language = _language_name(profile.language)

    prompts = {
        "summary": f"""
Sen profesyonel bir kariyer danışmanısın.
Aşağıdaki kullanıcı bilgilerine göre kısa, sade ve etkili bir CV profili yaz.

{base}

Kurallar:
- {language} yaz.
- 4-5 cümle kullan.
- Öğrenci veya yeni mezun seviyesine uygun yaz.
- Abartılı, gerçek dışı veya kanıtlanmamış ifadeler kullanma.
- Başvurulan pozisyonla ilgili beceri ve projeleri öne çıkar.
""",
        "cover_letter": f"""
Sen profesyonel bir işe başvuru danışmanısın.
Aşağıdaki kullanıcı bilgilerine göre başvurulan pozisyona uygun bir ön yazı hazırla.

{base}

Kurallar:
- {language} yaz.
- Giriş, gelişme ve kapanış paragrafı olsun.
- Gereksiz uzun olmasın.
- Öğrenci veya yeni mezun seviyesine uygun yaz.
- Yalan deneyim ekleme.
- Metin doğal, profesyonel ve başvuruya hazır olsun.
""",
        "linkedin": f"""
Sen LinkedIn profil danışmanısın.
Aşağıdaki bilgilere göre LinkedIn profilinin Hakkında alanına yazılabilecek doğal ama profesyonel bir metin üret.

{base}

Kurallar:
- {language} yaz.
- 2 kısa paragraf kullan.
- Birinci şahıs dili kullan.
- Teknik ilgi alanlarını ve hedef pozisyonu doğal biçimde bağla.
- Fazla iddialı pazarlama dili kullanma.
""",
        "organize_skills": f"""
Sen teknik CV düzenleme uzmanısın.
Aşağıdaki yetenekleri kategorilere ayır ve okunabilir bir liste haline getir.

{base}

Kurallar:
- {language} yaz.
- Kategoriler kullan.
- Aynı yeteneği tekrarlama.
- Belirtilmeyen yetenek ekleme.
- Kısa ve düzenli yaz.
""",
        "review": f"""
Sen deneyimli bir kariyer danışmanısın.
Aşağıdaki CV bilgilerini analiz et ve kullanıcıya uygulanabilir öneriler ver.

{base}

Kurallar:
- {language} yaz.
- "Güçlü Yönler" ve "Geliştirilmesi Gerekenler" başlıklarını kullan.
- En fazla 3 güçlü yön ve 3 geliştirme önerisi ver.
- Başvurulan pozisyon için eklenebilecek anahtar kelimeleri öner.
- Eleştirileri yapıcı ve net yaz.
""",
    }

    return prompts[action].strip()

