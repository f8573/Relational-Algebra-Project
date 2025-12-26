// Prefer explicit API base to avoid proxy header stripping; fallback to Vite proxy.
const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE_URL) || '/api'

function getAuthHeaders(){
  const token = localStorage.getItem('authToken')
  const headers = { 'Content-Type': 'application/json' }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  return headers
}

async function postJSON(path, data){
  const headers = getAuthHeaders()
  const hasAuth = !!headers['Authorization']
  try{ console.debug(`API POST ${path} (auth=${hasAuth})`) }catch(e){}
  const res = await fetch(`${API_BASE}${path}`, {
    method:'POST', headers, body:JSON.stringify(data)
  })
  // Defensive parsing: handle empty or non-JSON responses without throwing
  const text = await res.text()
  if (res.status === 401) {
    // Unauthorized — dispatch global event so app can respond centrally,
    // and surface explicitly so caller can clear session too.
    try{ window.dispatchEvent(new CustomEvent('ra:unauthorized', { detail: { path: path } })) }catch(e){}
    return { ok: false, status: 401, unauthorized: true }
  }
  if (!text) {
    return { ok: res.ok, status: res.status, data: null }
  }
  try{
    const parsed = JSON.parse(text)
    return { ok: res.ok, status: res.status, data: parsed }
  }catch(e){
    return { ok: res.ok, status: res.status, error: 'invalid_json', raw: text }
  }
}

async function getJSON(path){
  const headers = getAuthHeaders()
  const hasAuth = !!headers['Authorization']
  try{ console.debug(`API GET ${path} (auth=${hasAuth})`) }catch(e){}
  const res = await fetch(`${API_BASE}${path}`, { method:'GET', headers })
  const text = await res.text()
  if (res.status === 401) {
    try{ window.dispatchEvent(new CustomEvent('ra:unauthorized', { detail: { path: path } })) }catch(e){}
    return { ok: false, status: 401, unauthorized: true }
  }
  if (!text) {
    return { ok: res.ok, status: res.status, data: null }
  }
  try{
    const parsed = JSON.parse(text)
    return { ok: res.ok, status: res.status, data: parsed }
  }catch(e){
    return { ok: res.ok, status: res.status, error: 'invalid_json', raw: text }
  }
}

export default {
  runQuery: (script, dbId) => postJSON('/run/', { query: script, db_id: dbId }),
  login: (email, password) => postJSON('/auth/login', { email, password }),
  getCourse: (id) => getJSON(`/courses/${id}`),
  getCourses: () => getJSON('/courses'),
  getAssignmentSubmissions: (assignmentId) => getJSON(`/assessments/${assignmentId}/submissions`),
  getCourseAssignmentsPublic: (courseId) => getJSON(`/courses/${courseId}/assignments`),
    getAssessmentQuestions: (assessmentId) => getJSON(`/assessments/${assessmentId}/questions`),
  createCourse: (payload) => postJSON('/courses', payload),
  getUser: () => getJSON('/auth/user'),
  refresh: () => postJSON('/auth/refresh', {}),
  submitAnswer: (payload) => postJSON('/assessments/submit', payload),
}

// Auth helpers
export const auth = {
  register: (payload) => postJSON('/auth/register', payload),
  updateUser: (payload) => fetch(`${API_BASE}/auth/user`, { method: 'PUT', headers: getAuthHeaders(), body: JSON.stringify(payload) }).then(async r=>{ const t = await r.text(); try{ return { ok: r.ok, status: r.status, data: JSON.parse(t)} }catch(e){ return { ok: r.ok, status: r.status, raw: t } } }),
  changePassword: (newPassword) => postJSON('/auth/user/password', { new_password: newPassword })
}

// Admin helpers
export const admin = {
  listCourses: () => getJSON('/admin/courses'),
  getCourseAssignments: (courseId) => getJSON(`/admin/courses/${courseId}/assignments`),
  getAssignmentSubmissions: (assignmentId) => getJSON(`/admin/assignments/${assignmentId}/submissions`),
  gradeSubmission: (submissionId, payload) => postJSON(`/admin/submissions/${submissionId}/grade`, payload)
}

// Course member management
admin.getCourseMembers = (courseId) => getJSON(`/admin/courses/${courseId}/members`)
admin.enrollMember = (courseId, payload) => postJSON(`/admin/courses/${courseId}/members`, payload)
admin.removeMember = (courseId, userId) => fetch(`${API_BASE}/admin/courses/${courseId}/members/${userId}`, { method: 'DELETE', headers: getAuthHeaders() }).then(async r=>{ const t = await r.text(); try{ return { ok: r.ok, status: r.status, data: JSON.parse(t)} }catch(e){ return { ok: r.ok, status: r.status, raw: t } } })
admin.updateMember = (courseId, userId, payload) => fetch(`${API_BASE}/admin/courses/${courseId}/members/${userId}`, { method: 'PUT', headers: getAuthHeaders(), body: JSON.stringify(payload) }).then(async r=>{ const t = await r.text(); try{ return { ok: r.ok, status: r.status, data: JSON.parse(t)} }catch(e){ return { ok: r.ok, status: r.status, raw: t } } })
// User search for enroll modal
admin.searchUsers = (q, limit=20) => getJSON(`/admin/users?q=${encodeURIComponent(q)}&limit=${limit}`)

// Admin create/update/delete helpers
admin.createCourse = (payload) => postJSON('/admin/courses', payload)
admin.updateCourse = (id, payload) => fetch(`${API_BASE}/admin/courses/${id}`, { method: 'PUT', headers: getAuthHeaders(), body: JSON.stringify(payload) }).then(async r=>{ const t = await r.text(); try{ return { ok: r.ok, status: r.status, data: JSON.parse(t)} }catch(e){ return { ok: r.ok, status: r.status, raw: t } } })
admin.deleteCourse = (id) => fetch(`${API_BASE}/admin/courses/${id}`, { method: 'DELETE', headers: getAuthHeaders() }).then(async r=>{ const t = await r.text(); try{ return { ok: r.ok, status: r.status, data: JSON.parse(t)} }catch(e){ return { ok: r.ok, status: r.status, raw: t } } })

admin.createAssignment = (courseId, payload) => postJSON(`/admin/courses/${courseId}/assignments`, payload)
admin.updateAssignment = (id, payload) => fetch(`${API_BASE}/admin/assignments/${id}`, { method: 'PUT', headers: getAuthHeaders(), body: JSON.stringify(payload) }).then(async r=>{ const t = await r.text(); try{ return { ok: r.ok, status: r.status, data: JSON.parse(t)} }catch(e){ return { ok: r.ok, status: r.status, raw: t } } })
admin.deleteAssignment = (id) => fetch(`${API_BASE}/admin/assignments/${id}`, { method: 'DELETE', headers: getAuthHeaders() }).then(async r=>{ const t = await r.text(); try{ return { ok: r.ok, status: r.status, data: JSON.parse(t)} }catch(e){ return { ok: r.ok, status: r.status, raw: t } } })
// Database management (admin)
admin.listDatabases = () => getJSON('/admin/databases')
admin.uploadDatabase = (file, name) => {
  const form = new FormData()
  form.append('file', file)
  if (name) form.append('name', name)
  return fetch(`${API_BASE}/admin/databases`, { method: 'POST', headers: { 'Authorization': getAuthHeaders()['Authorization'] }, body: form }).then(async r=>{ const t = await r.text(); try{ return { ok: r.ok, status: r.status, data: JSON.parse(t)} }catch(e){ return { ok: r.ok, status: r.status, raw: t } } })
}
admin.deleteDatabase = (id) => fetch(`${API_BASE}/admin/databases/${id}`, { method: 'DELETE', headers: getAuthHeaders() }).then(async r=>{ const t = await r.text(); try{ return { ok: r.ok, status: r.status, data: JSON.parse(t)} }catch(e){ return { ok: r.ok, status: r.status, raw: t } } })
admin.getDatabasePreview = (id) => getJSON(`/admin/databases/${id}/preview`)
// Optional: get full submission details if backend exposes this endpoint
admin.getSubmissionDetails = (submissionId) => getJSON(`/admin/submissions/${submissionId}`)
// Question helpers
admin.getQuestion = (questionId) => getJSON(`/admin/questions/${questionId}`)
admin.updateQuestion = (questionId, payload) => fetch(`${API_BASE}/admin/questions/${questionId}`, { method: 'PUT', headers: getAuthHeaders(), body: JSON.stringify(payload) }).then(async r=>{ const t = await r.text(); try{ return { ok: r.ok, status: r.status, data: JSON.parse(t)} }catch(e){ return { ok: r.ok, status: r.status, raw: t } } })
