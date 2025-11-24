// const BASE_URL = "http://127.0.0.1:8000";
const BASE_URL =
  import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export async function getRandomPostings(count = 10) {
  const res = await fetch(`${BASE_URL}/postings/random?count=${count}`);
  return res.json();
}

export async function getAIPrediction(postingId) {
  const res = await fetch(`${BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ posting_id: postingId })
  });
  return res.json();
}

export async function submitResponse(payload) {
  const res = await fetch(`${BASE_URL}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return res.json();
}
