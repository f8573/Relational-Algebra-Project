import React, { useState, useEffect } from 'react'
import Editor from './components/Editor'
import Results from './components/Results'
import History from './components/History'
import CourseSelector from './components/CourseSelector'
import Login from './pages/Login'
import api from './lib/api'
import AdminDashboard from './pages/admin/AdminDashboard'
import AssignmentSidebar from './components/AssignmentSidebar'
import { useNavigate } from 'react-router-dom'

// Small helper: try to parse a textual table-like output into rows/cols.
function parseTableText(txt){
  if (!txt || typeof txt !== 'string') return null
  const trimmed = txt.trim()
  // try JSON first
  if ((trimmed.startsWith('[') || trimmed.startsWith('{'))){
    try{ const parsed = JSON.parse(trimmed)
      if (Array.isArray(parsed) && parsed.length>0 && typeof parsed[0] === 'object'){
        const cols = Array.from(new Set(parsed.flatMap(r=>Object.keys(r))))
        const rows = parsed.map(r=>cols.map(c=>r[c] == null ? '' : String(r[c])))
        return { cols, rows }
      }
    }catch(e){}
  }
  const lines = trimmed.split(/\r?\n/).map(l=>l.trim()).filter(l=>l.length>0)
  if (lines.length === 0) return null
  // detect delimiter
  const delimCandidates = ['\t','\|',',']
  for (const d of delimCandidates){
    const parts = lines[0].split(new RegExp(d))
    if (parts.length>1){
      const cols = parts.map(p=>p.trim())
      const rows = lines.map(l=>l.split(new RegExp(d)).map(c=>c.trim()))
      return { cols, rows }
    }
  }
  // fallback: single-column rows
  return { cols: ['value'], rows: lines.map(l=>[l]) }
}

function TableView({text}){
  const parsed = parseTableText(text)
  if (!parsed) return <pre style={{background:'#f8f8f8',padding:8,borderRadius:4,overflow:'auto'}}>{text}</pre>
  return (
    <div style={{overflowX:'auto',border:'1px solid #eee',borderRadius:6}}>
      <table style={{borderCollapse:'collapse',width:'100%'}}>
        <thead>
          <tr>
            {parsed.cols.map((c,i)=> <th key={i} style={{textAlign:'left',padding:'8px',borderBottom:'1px solid #eee',background:'#fafafa'}}>{c}</th>)}
          </tr>
        </thead>
        <tbody>
          {parsed.rows.map((r,ri)=> (
            <tr key={ri} style={{background:ri%2? '#fff':'#fcfcff'}}>
              {r.map((cell,ci)=>(<td key={ci} style={{padding:'8px',borderBottom:'1px solid #f6f6f6'}}>{cell}</td>))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function App({ defaultShowAdmin = false }){
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [course, setCourse] = useState(null)
  const [coursesKey, setCoursesKey] = useState(0)
  const [showCreate, setShowCreate] = useState(false)
  const [newCourseTitle, setNewCourseTitle] = useState('')
  const [newCourseTerm, setNewCourseTerm] = useState('')
  const [newCourseDesc, setNewCourseDesc] = useState('')
  const [showAdmin, setShowAdmin] = useState(defaultShowAdmin)
  const [output, setOutput] = useState('')
  const [history, setHistory] = useState(() => [])
  const [selectedAssignment, setSelectedAssignment] = useState(null)
  const [assignmentQuestions, setAssignmentQuestions] = useState([])
  const [selectedQuestionId, setSelectedQuestionId] = useState(null)
  const [lastSubmissionResult, setLastSubmissionResult] = useState(null)
  const editorSetContentRef = React.useRef(null)
  const navigate = useNavigate()

  // Check for existing auth on mount
  useEffect(() => {
    let mounted = true
    ;(async ()=>{
      const savedToken = localStorage.getItem('authToken')
      const savedUser = localStorage.getItem('user')
      if (!savedToken || !savedUser) return
      try{
        // Optimistically set values so UI updates quickly
        if (mounted) {
          setToken(savedToken)
          try{ setUser(JSON.parse(savedUser)) }catch(e){ setUser(null) }
        }
        // Validate token with backend; if invalid, clear saved session
        const res = await api.getUser()
        if (!mounted) return
        if (res && res.unauthorized) {
          // token not accepted by backend
          localStorage.removeItem('authToken')
          localStorage.removeItem('user')
          setToken(null)
          setUser(null)
        } else if (res && res.ok && res.data && res.data.user) {
          // refresh user info from server to ensure roles/flags are current
          setUser(res.data.user)
        } else {
          // unexpected response: clear session to force login
          // (avoid locking the UI behind a stale token)
          if (!(res && res.ok)){
            localStorage.removeItem('authToken')
            localStorage.removeItem('user')
            setToken(null)
            setUser(null)
          }
        }
      }catch(e){
        console.error('Session validation failed', e)
        try{ localStorage.removeItem('authToken'); localStorage.removeItem('user') }catch(_){}
        if (mounted){ setToken(null); setUser(null) }
      }
    })()
    return ()=>{ mounted = false }
  }, [])

  const handleLoginSuccess = (userData, authToken) => {
    setUser(userData)
    setToken(authToken)
  }

  const handleLogout = () => {
    setUser(null)
    setToken(null)
    setCourse(null)
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
  }

  const handleCourseSelect = (selectedCourse) => {
    setCourse(selectedCourse)
  }

  // load questions when assignment changes
  useEffect(()=>{
    let mounted = true
    const load = async ()=>{
      if (!selectedAssignment) { setAssignmentQuestions([]); setSelectedQuestionId(null); return }
      try{
        const res = await api.getAssessmentQuestions(selectedAssignment.id)
        if (!mounted) return
        if (res.ok && res.data) {
          const qs = res.data.questions || []
          setAssignmentQuestions(qs)
          if (qs.length>0) setSelectedQuestionId(qs[0].id)
          else setSelectedQuestionId(null)
        } else {
          setAssignmentQuestions([]); setSelectedQuestionId(null)
        }
      }catch(e){ console.error('Failed to load questions', e); if (mounted){ setAssignmentQuestions([]); setSelectedQuestionId(null) } }
    }
    load()
    return ()=>{ mounted = false }
  }, [selectedAssignment])

  const handleRefreshSession = async () => {
    try{
      const res = await api.refresh()
      if (res.ok && res.data && res.data.token){
        setToken(res.data.token)
        localStorage.setItem('authToken', res.data.token)
      } else {
        console.warn('Session refresh failed', res)
      }
    }catch(e){
      console.error('Refresh error', e)
    }
  }

  const run = async (script, dbId) => {
    // remember last-run script so Submit Query can use it if needed
    try{ sessionStorage.setItem('__lastRunQuery', script) }catch(e){}
    setOutput('Running...')
    try{
      const res = await api.runQuery(script, dbId)
      if (!res.ok) {
        setOutput(`Server error: HTTP ${res.status}`)
      } else if (res.error) {
        setOutput('Error: ' + (res.error + ' — ' + (res.raw||'')))
      } else if (res.data && res.data.status === 'success'){
        setOutput(res.data.output || '')
        setHistory(h => [script, ...h].slice(0, 100))
      } else if (res.data && res.data.status === 'error'){
        // Prefer human-readable error text for backend error responses
        const errText = res.data.error || res.data.message || JSON.stringify(res.data)
        setOutput('Error: ' + errText)
      } else {
        setOutput('Error: ' + JSON.stringify(res.data || res))
      }
    }catch(e){
      setOutput('Network error: '+e.message)
    }
  }

  // History/load integration: provide a setter that History can call to
  // overwrite the editor contents.
  const registerEditorSetContent = (fn) => { editorSetContentRef.current = fn }

  const handleHistoryLoad = (s) => {
    if (editorSetContentRef.current) {
      editorSetContentRef.current(s)
    } else {
      // fallback: paste into output if editor not ready
      setOutput(s)
    }
  }

  const handleCreateCourse = async (e) => {
    e.preventDefault()
    try{
      const payload = { title: newCourseTitle, term: newCourseTerm, description: newCourseDesc }
      const res = await api.createCourse(payload)
      if (res.ok && res.data && res.data.course) {
        // refresh courses list by bumping key which remounts CourseSelector
        setCoursesKey(k => k + 1)
        setCourse(res.data.course)
        setShowCreate(false)
        setNewCourseTitle('')
        setNewCourseTerm('')
        setNewCourseDesc('')
      } else {
        console.warn('Create course failed', res)
        alert('Failed to create course: ' + (res.data?.message || res.status))
      }
    }catch(e){
      console.error('Create error', e)
      alert('Network error: '+e.message)
    }
  }

  if (!user || !token) {
    return <Login onLoginSuccess={handleLoginSuccess} />
  }

  return (
    <div className="app-root">
      {showCreate && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Create Course</h3>
            <form onSubmit={handleCreateCourse}>
              <div>
                <label>Title</label>
                <input value={newCourseTitle} onChange={(e)=>setNewCourseTitle(e.target.value)} required />
              </div>
              <div>
                <label>Term</label>
                <input value={newCourseTerm} onChange={(e)=>setNewCourseTerm(e.target.value)} />
              </div>
              <div>
                <label>Description</label>
                <textarea value={newCourseDesc} onChange={(e)=>setNewCourseDesc(e.target.value)} />
              </div>
              <div style={{marginTop:8}}>
                <button type="submit">Create</button>
                <button type="button" onClick={()=>setShowCreate(false)} style={{marginLeft:8}}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
      <div className="app-header">
        <div className="header-left">
          <h2>Relational Algebra</h2>
          <CourseSelector key={coursesKey} onCourseSelect={handleCourseSelect} userRole={user.role} onUnauthorized={handleLogout} />
          {course && (
            <div className="active-course" style={{marginLeft:12}}>
              {course.title} ({course.role})
            </div>
          )}
        </div>
          <div className="user-info">
          <span>{user.name || user.email}</span>
          <button onClick={()=>navigate('/profile')} style={{marginLeft:8}}>Profile</button>
          {user.is_platform_admin && (
            <button className="admin-button" onClick={()=>{
              // navigate to admin route for a dedicated admin page
              navigate('/admin')
            }} style={{marginLeft:8}}>Admin</button>
          )}
          <button className="refresh-button" onClick={handleRefreshSession} style={{marginLeft:8}}>Refresh</button>
          <button className="logout-button" onClick={handleLogout} style={{marginLeft:8}}>Logout</button>
        </div>
      </div>

      <div style={{display:'flex',gap:12,alignItems:'flex-start'}}>
        <AssignmentSidebar course={course} selectedAssignment={selectedAssignment} onSelect={(a)=>setSelectedAssignment(a)} />
        <div className="left main-editor" style={{flex:1}}>
          {selectedAssignment && (
            <div style={{marginBottom:8,display:'flex',flexDirection:'column',gap:8}}>
              <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',gap:12}}>
                <div>
                  <strong>{selectedAssignment.title}</strong>
                  <div style={{fontSize:12,color:'#666'}}>{course?.title}</div>
                </div>
                <div style={{minWidth:320}}>
                  {selectedQuestionId ? (
                    <div style={{padding:10,background:'#fbfbff',border:'1px solid #f0f4ff',borderRadius:6}}>
                      <div style={{fontWeight:700,marginBottom:6}}>Question</div>
                      <div style={{fontSize:14,color:'#222'}}>{(assignmentQuestions.find(q=>q.id===selectedQuestionId)?.prompt) || 'No prompt available'}</div>
                      <div style={{fontSize:12,color:'#666',marginTop:6}}>{(() => {
                        const q = assignmentQuestions.find(q=>q.id===selectedQuestionId)
                        return q ? (q.score!=null ? `${q.score}/${q.points}` : `-/${q.points}`) : ''
                      })()}</div>
                    </div>
                  ) : (
                    <div style={{padding:10,background:'#fff',border:'1px solid #f6f6f6',borderRadius:6,color:'#999'}}>No question selected</div>
                  )}
                </div>
              </div>

              <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',gap:8}}>
                  <div style={{flex:1}}>
                    <label style={{display:'block',fontSize:12,marginBottom:6}}>Questions</label>
                    <div style={{display:'flex',gap:8,flexWrap:'wrap',maxWidth:880}}>
                    {assignmentQuestions.map((q, idx)=> {
                      const selected = q.id === selectedQuestionId
                      return (
                        <button
                          key={q.id}
                          onClick={()=>setSelectedQuestionId(q.id)}
                          style={{
                            padding:'8px 12px',
                            borderRadius:18,
                            border: selected ? '2px solid #2b7cff' : '1px solid #ddd',
                            background: selected ? '#e8f0ff' : '#fff',
                            cursor:'pointer',
                            boxShadow: selected ? '0 1px 4px rgba(43,124,255,0.15)' : 'none',
                            display:'flex',
                            flexDirection:'column',
                            alignItems:'flex-start',
                            gap:4
                          }}
                        >
                          <div style={{fontWeight:700,fontSize:13}}>Q{idx+1}</div>
                          <div style={{fontSize:12,color:'#444',maxWidth:240,whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}}>{(q.prompt||'').slice(0,60)}</div>
                          <div style={{fontSize:11,color:'#666'}}>{q.score!=null ? `${q.score}/${q.points}` : `-/${q.points}`}</div>
                        </button>
                      )
                    })}
                  </div>
                </div>
                <div>
                  {/* Submit button moved into MathEditor; no-op placeholder kept to preserve layout */}
                </div>
              </div>
            </div>
          )}
          <Editor onRun={run} course={course} registerSetContent={registerEditorSetContent}
            onSubmit={async ()=>{
              const query = (window.__lastRunQuery || '')
              if (!query) {
                alert('No query to submit. Use Run Query or enter text in the editor.')
                return
              }
              if (!selectedQuestionId){ alert('Select a question'); return }
              try{
                const payload = { user_id: user.id, assessment_id: selectedAssignment.id, question_id: selectedQuestionId, query }
                const res = await api.submitAnswer(payload)
                if (res.ok && res.data){
                  setLastSubmissionResult(res.data.result || res.data)
                  const qres = await api.getAssessmentQuestions(selectedAssignment.id)
                  if (qres.ok && qres.data){ setAssignmentQuestions(qres.data.questions || []); }
                } else {
                  alert('Submit failed')
                }
              }catch(e){ console.error('Submit failed', e); alert('Submit failed') }
            }}
          />
          {lastSubmissionResult && (
            <div style={{marginTop:12,padding:8,border:'1px solid #eee',borderRadius:6,background:'#fff'}}>
              <h4>Submission Result</h4>
              {lastSubmissionResult.comparison ? (
                <div>
                  <div style={{fontWeight:600,marginBottom:8}}>Matching: {String(lastSubmissionResult.comparison.match)}</div>
                  <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:12}}>
                    <div>
                      <div style={{fontWeight:600,marginBottom:6}}>Expected (solution_query)</div>
                      <TableView text={lastSubmissionResult.comparison.solution_output || ''} />
                    </div>
                    <div>
                      <div style={{fontWeight:600,marginBottom:6}}>Your output</div>
                      <TableView text={lastSubmissionResult.comparison.student_output || ''} />
                    </div>
                  </div>
                </div>
              ) : (
                <div>No comparison available. Feedback:
                  <pre style={{background:'#fff',padding:8,borderRadius:4,whiteSpace:'pre-wrap'}}>{JSON.stringify(lastSubmissionResult.feedback||lastSubmissionResult,null,2)}</pre>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {showAdmin && (
        <AdminDashboard onClose={() => {
          setShowAdmin(false)
          // if this view was opened via route, navigate back to root
          try { navigate('/') } catch (e) {}
        }} />
      )}

      <div className="below">
        <div className="center results">
          <Results output={output} />
        </div>
        <div className="right history">
          <History items={history} onLoad={handleHistoryLoad} />
        </div>
      </div>
    </div>
  )
}
