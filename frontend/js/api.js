// Centralized fetch calls for frontend (simple token-based auth)
// Allow overriding API base to bypass proxy in dev if headers are dropped.
const API_BASE = (typeof window !== 'undefined' && window.API_BASE_URL) || '/api';

function getAuthHeaders() {
  const token = localStorage.getItem('authToken');
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
}

async function postJSON(path, data) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  const text = await res.text();
  if (!text) return { ok: res.ok, status: res.status, data: null };
  try { return { ok: res.ok, status: res.status, data: JSON.parse(text) }; }
  catch (e) { return { ok: res.ok, status: res.status, error: 'invalid_json', raw: text }; }
}

async function getJSON(path) {
  const res = await fetch(`${API_BASE}${path}`, { headers: getAuthHeaders() });
  const text = await res.text();
  if (!text) return { ok: res.ok, status: res.status, data: null };
  try { return { ok: res.ok, status: res.status, data: JSON.parse(text) }; }
  catch (e) { return { ok: res.ok, status: res.status, error: 'invalid_json', raw: text }; }
}

const API = {
  runQuery: (script) => postJSON('/run/', { query: script }),
  login: (email, password) => postJSON('/auth/login', { email, password }),
  getCourse: async (id) => (await getJSON(`/courses/${id}`)).data,
  getCourses: async () => (await getJSON('/courses')).data,
};

export default API;
