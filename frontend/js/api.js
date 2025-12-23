// Centralized fetch calls for frontend
const API_BASE = '/api';

async function postJSON(path, data) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const text = await res.text()
  if (!text) return { ok: res.ok, status: res.status, data: null }
  try{ return { ok: res.ok, status: res.status, data: JSON.parse(text) } }
  catch(e){ return { ok: res.ok, status: res.status, error: 'invalid_json', raw: text } }
}

const API = {
  runQuery: (script) => postJSON('/run/', { query: script }),
  login: (email, password) => postJSON('/auth/login', { email, password }),
  getCourse: (id) => fetch(`${API_BASE}/courses/${id}`).then(r => r.json()),
};

export default API;
