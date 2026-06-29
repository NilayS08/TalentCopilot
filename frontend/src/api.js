const BASE = "/api";

async function uploadFile(url, file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE}${url}`, { method: "POST", body: form });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text.slice(0, 200));
  }
  return res.json();
}

async function postJSON(url, body) {
  const res = await fetch(`${BASE}${url}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text.slice(0, 200));
  }
  return res.json();
}

export function uploadJD(file) {
  return uploadFile("/jd/extract-requirements", file);
}

export function uploadResume(file) {
  return uploadFile("/resume/extract-profile", file);
}

export function rankCandidates(jd, candidates) {
  return postJSON("/evaluation/rank", { jd, candidates });
}

export function generateInsight(jd, candidate, evaluation) {
  return postJSON("/evaluation/insight", { jd, candidate, evaluation });
}
