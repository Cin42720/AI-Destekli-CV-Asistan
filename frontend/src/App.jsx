import React, { useEffect, useMemo, useState } from "react";
import {
  BadgeCheck,
  BriefcaseBusiness,
  ClipboardCopy,
  Download,
  FileText,
  Languages,
  Linkedin,
  Loader2,
  RefreshCw,
  Sparkles,
  UserRound,
} from "lucide-react";

import { generateCareerText } from "./api.js";

const initialProfile = {
  full_name: "",
  school: "",
  department: "",
  skills: "",
  experiences: "",
  projects: "",
  certificates: "",
  target_position: "",
  language: "tr",
  tone: "sade",
};

const actions = [
  { id: "summary", label: "CV Özeti", icon: FileText },
  { id: "cover_letter", label: "Ön Yazı", icon: BriefcaseBusiness },
  { id: "linkedin", label: "LinkedIn", icon: Linkedin },
  { id: "organize_skills", label: "Yetenekler", icon: BadgeCheck },
  { id: "review", label: "CV Analizi", icon: Sparkles },
];

const sampleProfile = {
  full_name: "Ayşe Yılmaz",
  school: "Ankara Üniversitesi",
  department: "Bilgisayar Programcılığı",
  skills: "React, HTML, CSS, JavaScript, Python, FastAPI, Playwright, GitHub",
  experiences: "Üniversite projelerinde frontend geliştirme ve test otomasyonu çalışmaları yaptım.",
  projects: "Kişisel portfolyo sitesi, görev takip uygulaması, Playwright ile form testleri",
  certificates: "BTK Akademi Python Temelleri, Git ve GitHub Eğitimi",
  target_position: "Frontend stajyeri",
  language: "tr",
  tone: "sade",
};

function Field({ label, name, value, onChange, placeholder, textarea = false }) {
  const id = `field-${name}`;
  const commonProps = {
    id,
    name,
    value,
    onChange,
    placeholder,
  };

  return (
    <label className="field" htmlFor={id}>
      <span>{label}</span>
      {textarea ? <textarea rows="4" {...commonProps} /> : <input {...commonProps} />}
    </label>
  );
}

function App() {
  const [profile, setProfile] = useState(initialProfile);
  const [result, setResult] = useState(null);
  const [activeAction, setActiveAction] = useState(null);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("careerCraftProfile");
    if (saved) {
      setProfile({ ...initialProfile, ...JSON.parse(saved) });
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("careerCraftProfile", JSON.stringify(profile));
  }, [profile]);

  const completionScore = useMemo(() => {
    const importantFields = [
      profile.full_name,
      profile.school,
      profile.department,
      profile.skills,
      profile.projects,
      profile.target_position,
    ];
    const completed = importantFields.filter((field) => field.trim().length > 0).length;
    return Math.round((completed / importantFields.length) * 100);
  }, [profile]);

  function updateProfile(event) {
    const { name, value } = event.target;
    setProfile((current) => ({ ...current, [name]: value }));
  }

  async function handleGenerate(actionId) {
    setError("");
    setCopied(false);
    setActiveAction(actionId);

    try {
      const data = await generateCareerText(actionId, profile);
      setResult(data);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setActiveAction(null);
    }
  }

  async function copyResult() {
    if (!result?.content) return;
    await navigator.clipboard.writeText(result.content);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1500);
  }

  function downloadResult() {
    if (!result?.content) return;
    const blob = new Blob([result.content], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${result.title.toLowerCase().replaceAll(" ", "-")}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <main className="app-shell">
      <section className="topbar" aria-label="Uygulama başlığı">
        <div>
          <p className="eyebrow">CareerCraft AI</p>
          <h1>AI Destekli CV ve Ön Yazı Asistanı</h1>
        </div>
        <div className="score" title="Form doluluk oranı">
          <span>{completionScore}%</span>
          <small>Hazırlık</small>
        </div>
      </section>

      <section className="workspace">
        <form className="panel form-panel" onSubmit={(event) => event.preventDefault()}>
          <div className="panel-title">
            <UserRound size={20} aria-hidden="true" />
            <div>
              <h2>Kullanıcı Bilgileri</h2>
              <p>Bilgileri ne kadar net yazarsan çıktı o kadar kullanışlı olur.</p>
            </div>
          </div>

          <div className="grid two">
            <Field
              label="Ad Soyad"
              name="full_name"
              value={profile.full_name}
              onChange={updateProfile}
              placeholder="Örn. Ayşe Yılmaz"
            />
            <Field
              label="Başvurulacak Pozisyon"
              name="target_position"
              value={profile.target_position}
              onChange={updateProfile}
              placeholder="Örn. Frontend stajyeri"
            />
            <Field
              label="Okul"
              name="school"
              value={profile.school}
              onChange={updateProfile}
              placeholder="Örn. Ankara Üniversitesi"
            />
            <Field
              label="Bölüm"
              name="department"
              value={profile.department}
              onChange={updateProfile}
              placeholder="Örn. Bilgisayar Programcılığı"
            />
          </div>

          <Field
            label="Yetenekler"
            name="skills"
            value={profile.skills}
            onChange={updateProfile}
            placeholder="React, HTML, CSS, Python, Playwright, GitHub"
            textarea
          />

          <Field
            label="Deneyimler"
            name="experiences"
            value={profile.experiences}
            onChange={updateProfile}
            placeholder="Stajlar, okul çalışmaları veya gönüllü deneyimler"
            textarea
          />

          <Field
            label="Projeler"
            name="projects"
            value={profile.projects}
            onChange={updateProfile}
            placeholder="Portfolyo sitesi, otomasyon projesi, mobil uygulama..."
            textarea
          />

          <Field
            label="Sertifikalar"
            name="certificates"
            value={profile.certificates}
            onChange={updateProfile}
            placeholder="BTK Akademi, Coursera, Udemy veya okul sertifikaları"
            textarea
          />

          <div className="grid two compact">
            <label className="field" htmlFor="language">
              <span>Dil</span>
              <select id="language" name="language" value={profile.language} onChange={updateProfile}>
                <option value="tr">Türkçe</option>
                <option value="en">İngilizce</option>
              </select>
            </label>
            <label className="field" htmlFor="tone">
              <span>Ton</span>
              <select id="tone" name="tone" value={profile.tone} onChange={updateProfile}>
                <option value="sade">Sade</option>
                <option value="resmi">Resmi</option>
                <option value="etkileyici">Etkileyici</option>
              </select>
            </label>
          </div>

          <div className="form-actions">
            <button type="button" className="ghost-button" onClick={() => setProfile(sampleProfile)}>
              <RefreshCw size={17} aria-hidden="true" />
              Örnek Doldur
            </button>
            <button type="button" className="ghost-button muted" onClick={() => setProfile(initialProfile)}>
              Formu Temizle
            </button>
          </div>
        </form>

        <section className="panel output-panel">
          <div className="panel-title">
            <Languages size={20} aria-hidden="true" />
            <div>
              <h2>AI Çıktısı</h2>
              <p>Bir işlem seç, çıktı burada hazır hale gelsin.</p>
            </div>
          </div>

          <div className="action-grid" aria-label="AI işlemleri">
            {actions.map((action) => {
              const Icon = action.icon;
              const loading = activeAction === action.id;
              return (
                <button
                  type="button"
                  key={action.id}
                  className="action-button"
                  onClick={() => handleGenerate(action.id)}
                  disabled={Boolean(activeAction)}
                  title={`${action.label} oluştur`}
                >
                  {loading ? <Loader2 className="spin" size={18} aria-hidden="true" /> : <Icon size={18} aria-hidden="true" />}
                  <span>{action.label}</span>
                </button>
              );
            })}
          </div>

          {error && <p className="error">{error}</p>}

          <article className="result-box" aria-live="polite">
            {result ? (
              <>
                <div className="result-header">
                  <div>
                    <h3>{result.title}</h3>
                    <span>{result.provider === "mock" ? "Demo AI modu" : `${result.provider} API`}</span>
                  </div>
                  <div className="result-tools">
                    <button type="button" onClick={copyResult} title="Çıktıyı kopyala">
                      <ClipboardCopy size={17} aria-hidden="true" />
                      {copied ? "Kopyalandı" : "Kopyala"}
                    </button>
                    <button type="button" onClick={downloadResult} title="Metin dosyası indir">
                      <Download size={17} aria-hidden="true" />
                      İndir
                    </button>
                  </div>
                </div>
                <pre>{result.content}</pre>
              </>
            ) : (
              <div className="empty-state">
                <Sparkles size={30} aria-hidden="true" />
                <h3>Henüz çıktı oluşturulmadı</h3>
                <p>CV özeti, ön yazı veya LinkedIn metni üretmek için yukarıdaki işlemlerden birini kullan.</p>
              </div>
            )}
          </article>
        </section>
      </section>
    </main>
  );
}

export default App;
