# CareerCraft AI - AI Destekli CV ve Ön Yazı Asistanı

CareerCraft AI, öğrenciler ve yeni mezunlar için hazırlanmış yapay zekâ destekli bir kariyer metni oluşturma uygulamasıdır. Kullanıcıdan alınan eğitim, beceri, deneyim, proje ve hedef pozisyon bilgilerine göre CV özeti, ön yazı, LinkedIn açıklaması, yetenek düzenlemesi ve CV analizi üretir.

## Nasıl Kullanılır?

1. Kullanıcı uygulamayı açar.
2. Form alanlarına ad soyad, okul, bölüm, yetenekler, deneyimler, projeler, sertifikalar ve başvurulacak pozisyon bilgilerini girer.
3. Çıktı dili olarak Türkçe veya İngilizce seçer.
4. Metin tonunu sade, resmi veya etkileyici olarak belirler.
5. İhtiyacına göre `CV Özeti`, `Ön Yazı`, `LinkedIn`, `Yetenekler` veya `CV Analizi` butonlarından birine tıklar.
6. Sistem, girilen bilgileri backend tarafındaki hazır promptlarla işler ve yapay zekâ destekli bir metin üretir.
7. Oluşturulan metin ekranda görüntülenir.
8. Kullanıcı sonucu `Kopyala` butonu ile panoya kopyalayabilir veya `İndir` butonu ile `.txt` dosyası olarak indirebilir.

Demo kullanım için API anahtarı zorunlu değildir. Proje varsayılan olarak demo modunda çalışır ve örnek yapay zekâ çıktıları üretir. Gerçek OpenAI veya Gemini API kullanılmak istenirse `backend/.env` dosyasına API anahtarı eklenebilir.

## Özellikler

- Kullanıcı bilgilerinin form ile alınması
- CV profili oluşturma
- Ön yazı oluşturma
- LinkedIn "Hakkında" metni oluşturma
- Yetenekleri kategorilere ayırma
- CV için güçlü yönler ve geliştirme önerileri üretme
- Türkçe / İngilizce dil seçimi
- Resmi, sade veya etkileyici ton seçimi
- LocalStorage ile form bilgisini saklama
- Çıktıyı kopyalama ve `.txt` olarak indirme

## Kullanılan Teknolojiler

- Frontend: React + Vite
- Backend: FastAPI
- Yapay zekâ: Demo modu, Groq Llama 3.3 70B, OpenAI API veya Gemini API
- Veri saklama: Tarayıcı LocalStorage

## Gereklilikler

Projeyi çalıştırmak için bilgisayarda aşağıdaki araçların kurulu olması gerekir:

- Node.js
- npm
- Python 3.10 veya üzeri
- pip

Demo modunda çalıştırmak için API anahtarı gerekmez. Gerçek yapay zekâ modeli kullanılacaksa ilgili API anahtarı `backend/.env` dosyasına eklenmelidir. Ödev için önerilen gerçek model seçeneği Groq üzerinden çalışan `llama-3.3-70b-versatile` modelidir.

## Önemli Notlar

- API anahtarları frontend tarafında tutulmaz.
- `.env` dosyası normalde gizli bilgiler içerdiği için GitHub'a yüklenmemelidir.
- Ödev kontrolü için API anahtarı görünür bırakılacaksa yalnızca bu proje için oluşturulmuş, limitli ve sonradan iptal edilecek bir demo anahtarı kullanılmalıdır.
- Proje eğitim ve ödev amacıyla hazırlanmıştır.
- Üretilen CV ve ön yazı metinleri kullanıcı tarafından kontrol edilmelidir.
- Uygulama kullanıcının girdiği bilgilere göre metin üretir, gerçek dışı deneyim eklememeyi hedefler.

## Klasör Yapısı

```text
career-ai-assistant/
  frontend/
    src/
      App.jsx
      api.js
      main.jsx
      styles.css
  backend/
    main.py
    ai_service.py
    prompts.py
    schemas.py
    requirements.txt
    .env.example
```

## Çalıştırma

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Uygulama varsayılan olarak `http://localhost:5173` adresinde çalışır. Backend `http://localhost:8000` adresindedir.

## Yapay Zekâ API Kullanımı

Proje varsayılan olarak `AI_PROVIDER=mock` ile çalışır. Bu mod internet veya API anahtarı gerektirmez ve demo için profesyonel örnek metinler üretir.

Ödev için Llama 3.3 70B kullanmak istenirse `backend/.env` dosyası şu şekilde düzenlenebilir:

```env
AI_PROVIDER=groq
GROQ_API_KEY=groq_api_anahtariniz
GROQ_MODEL=llama-3.3-70b-versatile
```

Alternatif olarak OpenAI kullanmak için:

```env
AI_PROVIDER=openai
OPENAI_API_KEY=api_anahtariniz
OPENAI_MODEL=gpt-4o-mini
```

veya:

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=api_anahtariniz
GEMINI_MODEL=gemini-1.5-flash
```

## Projede Yapay Zekâ Araçları Nasıl Kullanıldı?

Bu projede yapay zekâ iki şekilde kullanılmıştır:

1. Geliştirme sürecinde yapay zekâ; proje fikrini netleştirme, arayüz planlama, dosya yapısı kurma, prompt tasarlama, hata ayıklama ve README metnini düzenleme aşamalarında yardımcı araç olarak kullanılmıştır.
2. Uygulamanın içinde yapay zekâ; kullanıcının girdiği eğitim, beceri, deneyim, proje ve hedef pozisyon bilgilerini backend tarafındaki hazır promptlarla işleyerek CV özeti, ön yazı, LinkedIn açıklaması ve CV önerileri üretmek için kullanılmıştır.

API anahtarları güvenlik nedeniyle frontend tarafında tutulmaz. Frontend yalnızca FastAPI backend'e istek gönderir; gerçek yapay zekâ API çağrısı backend tarafından yapılır.

Ödev kontrolü için limitli ve ücretsiz Groq/Llama anahtarı kullanılırsa da anahtar frontend kodunda değil, backend tarafındaki `.env` dosyasında tutulur. Böylece uygulama mimarisi güvenli kullanım mantığını göstermeye devam eder.

## Prompt Mantığı

Backend'de her işlem için ayrı prompt şablonu bulunur. Örneğin CV özeti üretiminde modelden 4-5 cümlelik, doğal, abartısız ve başvurulan pozisyona uygun bir metin istenir. Ön yazı üretiminde ise giriş, gelişme ve kapanış paragrafları olan, öğrenci seviyesine uygun ve gerçek dışı deneyim eklemeyen bir metin istenir.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakılabilir.
