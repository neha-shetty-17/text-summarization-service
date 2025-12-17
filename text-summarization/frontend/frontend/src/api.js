
const BACKEND = process.env.REACT_APP_BACKEND || "http://backend:8000";

export async function summarize(text, opts = { max_length: 60, min_length: 10 }) {
  const resp = await fetch(`${BACKEND}/summarize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text,
      max_length: opts.max_length,
      min_length: opts.min_length
    })
  });
  if (!resp.ok) {
    const err = await resp.json();
    throw new Error(err.detail || "Server error");
  }
  return resp.json();
}

export async function fetchHistory(limit = 20) {
  const resp = await fetch(`${BACKEND}/history?limit=${limit}`);
  if (!resp.ok) throw new Error("Failed to fetch history");
  return resp.json();
}
