const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function generateCareerText(action, profile) {
  const response = await fetch(`${API_URL}/api/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ action, profile }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(error?.detail || "Metin üretilemedi.");
  }

  return response.json();
}

