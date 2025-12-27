import React, { useState, useEffect } from 'react'
import api, { admin } from '../../lib/api'
import Modal from '../../components/Modal'

export default function AdminDashboard({ onClose, fullPage = false }){
  const [courses, setCourses] = useState([])
  const [selectedCourse, setSelectedCourse] = useState(null)
  const [assignments, setAssignments] = useState([])
  const [selectedAssignment, setSelectedAssignment] = useState(null)
  const [submissions, setSubmissions] = useState([])
  const [members, setMembers] = useState([])
  const [modalOpen, setModalOpen] = useState(false)
  const [modalMode, setModalMode] = useState(null)
  const [modalPrevMode, setModalPrevMode] = useState(null)
  const [modalPayload, setModalPayload] = useState({})
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [searchLoading, setSearchLoading] = useState(false)
  const [selectedUser, setSelectedUser] = useState(null)
  const [modalSubmitting, setModalSubmitting] = useState(false)
  const [dbList, setDbList] = useState([])
  const [dbUploading, setDbUploading] = useState(false)
  const [dbPreview, setDbPreview] = useState(null)
  const [dbPreviewOpen, setDbPreviewOpen] = useState(false)
  const [dbPreviewName, setDbPreviewName] = useState('')
  const [modalError, setModalError] = useState('')
  const [fdTextMap, setFdTextMap] = useState({})

  const computeModalValidation = () => {
    if (modalMode === 'editQuestion'){
      const val = (modalPayload.solution_query||'').trim()
      if (!val) return { disabled: true, reason: 'Solution query is required.' }
      return { disabled: false, reason: '' }
    }
    if (modalMode === 'createAssignment' || modalMode === 'editAssignment'){
      const qs = (modalPayload.questions||[])
      const missing = qs.some(q => {
        const qtype = (q.question_type || 'ra').toLowerCase()
        if (qtype === 'ra') {
          return !(q.solution_query && String(q.solution_query).trim())
        }
        if (qtype === 'mcq') {
          return !q.answer_key_json || !String(q.answer_key_json.correct || '').trim()
        }
        if (qtype === 'msq') {
          const correct = q.answer_key_json?.correct
          return !q.answer_key_json || !(Array.isArray(correct) && correct.length > 0) && !String(correct || '').trim()
        }
        if (qtype === 'norm') {
          const hasForms = q.answer_key_json && Array.isArray(q.answer_key_json.correct_forms) && q.answer_key_json.correct_forms.length > 0
          const hasText = q.answer_key_json && ((Array.isArray(q.answer_key_json.acceptable) && q.answer_key_json.acceptable.length > 0) || (q.answer_key_json.regex && String(q.answer_key_json.regex).trim()))
          const hasDecompSet = q.answer_key_json && Array.isArray(q.answer_key_json.decomposition_signatures) && q.answer_key_json.decomposition_signatures.length > 0
          const targetNF = (q.answer_key_json && (q.answer_key_json.target_nf||'').toString().toUpperCase()) || ''
          const needsFDs = targetNF === '2NF' || targetNF === '3NF' || targetNF === 'BCNF' || targetNF === '4NF' || targetNF === '5NF'
          const fdCount = ((q.options_json && q.options_json.schema && Array.isArray(q.options_json.schema.fds)) ? q.options_json.schema.fds.length : 0)
          if (needsFDs && fdCount === 0) return true
          // At least one grading path must be defined
          return !(hasForms || hasText || hasDecompSet || (needsFDs && fdCount>0))
        }
        if (qtype === 'sql') {
          return !q.options_json?.database_file_id || !String(q.answer_key_json?.expected_result_sql || '').trim()
        }
        // free
        return !q.answer_key_json || ((!(Array.isArray(q.answer_key_json.acceptable) && q.answer_key_json.acceptable.length > 0)) && !(q.answer_key_json.regex && String(q.answer_key_json.regex).trim()))
      })
      if (missing) return { disabled: true, reason: 'Each question must have a valid answer: solution (RA), correct choice(s) (MCQ/MSQ), normal forms or text/regex (Normalization), text/regex (Free), or database + expected result (SQL).' }
      return { disabled: false, reason: '' }
    }
    return { disabled: false, reason: '' }
  }

  useEffect(()=>{
    const load = async ()=>{
      const res = await admin.listCourses()
      if (res.ok && res.data) setCourses(res.data.courses)
    }
    load()
  },[])

  useEffect(()=>{
    if (modalOpen && (modalMode === 'createAssignment' || modalMode === 'editAssignment')) {
      refreshDbList()
    }
  }, [modalOpen, modalMode])

  const refreshCourses = async ()=>{
    const res = await admin.listCourses()
    if (res.ok && res.data) setCourses(res.data.courses)
  }

  // modal-driven create/edit course
  const openCreateCourse = ()=>{ setModalMode('createCourse'); setModalPayload({ title: '' }); setModalOpen(true) }
  const openEditCourse = (course)=>{ setModalMode('editCourse'); setModalPayload({ id: course.id, title: course.title }); setModalOpen(true); refreshDbList() }
  const submitCourseModal = async ()=>{
    const t = (modalPayload.title||'').trim()
    if (!t){ alert('Title required'); return }
    if (modalMode === 'createCourse'){
      const res = await admin.createCourse({ title: t })
      if (res.ok) { refreshCourses(); setModalOpen(false) }
      else alert('Create failed')
    } else if (modalMode === 'editCourse'){
      const res = await admin.updateCourse(modalPayload.id, { title: t })
      if (res.ok) { refreshCourses(); setModalOpen(false) }
      else alert('Update failed')
    }
  }

  const loadAssignments = async (courseId)=>{
    const res = await admin.getCourseAssignments(courseId)
    if (res.ok && res.data) setAssignments(res.data.assignments || [])
  }

  const refreshDbList = async ()=>{
    try{
      const res = await admin.listDatabases()
      if (res.ok && res.data) setDbList(res.data.databases || [])
    }catch(e){ console.error('Failed to list DBs', e) }
  }

  const uploadDatabase = async (file, name)=>{
    if (!file) return
    setDbUploading(true)
    try{
      const res = await admin.uploadDatabase(file, name)
      if (res.ok && res.data){
        await refreshDbList()
        return res.data.database
      } else {
        alert('Upload failed')
      }
    }catch(e){ console.error('Upload error', e); alert('Upload failed') }
    finally{ setDbUploading(false) }
  }

  const openDbPreview = async (dbId, name) =>{
    if (!dbId) return
    try{
      const res = await admin.getDatabasePreview(dbId)
      if (res.ok && res.data){
        setDbPreview(res.data.tables || [])
        setDbPreviewName(name || '')
        setDbPreviewOpen(true)
      } else {
        alert('Preview failed')
      }
    }catch(e){ console.error('Preview error', e); alert('Preview failed') }
  }

  const loadAssignmentQuestions = async (assignmentId)=>{
    // load course assignments and find this one
    try{
      const res = await admin.getCourseAssignments(selectedCourse.id)
      if (res.ok && res.data){
        const found = (res.data.assignments||[]).find(a=>String(a.id)===String(assignmentId))
          if (found){
              const questions = (found.questions||[]).map(q=>({
                prompt: q.prompt,
                points: q.points,
                db_id: q.db_id || null,
                solution_query: q.solution_query || '',
                id: q.id,
                question_type: q.question_type || 'ra',
                options_json: q.options_json || {},
                answer_key_json: q.answer_key_json || {},
                submission_limit: q.submission_limit || 0
              }))
              setModalPayload(p=>({...p, questions, type: found.type || 'assignment', time_limit_minutes: found.time_limit_minutes || null }))
            // Initialize FD text map
            const newFdMap = {}
            questions.forEach((q, idx) => {
              const fds = q.options_json?.schema?.fds || []
              newFdMap[idx] = fds.map(fd => `${(fd.lhs||[]).join(',')} -> ${(fd.rhs||[]).join(',')}`).join('\n')
            })
            setFdTextMap(newFdMap)
          }
      }
    }catch(e){ console.error('Failed to load assignment questions', e) }
  }

  const loadSubmissions = async (assignmentId)=>{
    const res = await admin.getAssignmentSubmissions(assignmentId)
    if (res.ok && res.data) setSubmissions(res.data.submissions)
  }

  const rootClass = fullPage ? 'admin-fullpage' : 'admin-modal'

  const loadMembers = async (courseId)=>{
    const res = await admin.getCourseMembers(courseId)
    if (res.ok && res.data) setMembers(res.data.members)
  }

  // search users when enroll modal is open and searchQuery changes
  useEffect(()=>{
    if (modalMode !== 'enrollMember') return
    let mounted = true
    let timer = null
    const doSearch = async ()=>{
      const q = (searchQuery||'').trim()
      if (!q){ setSearchResults([]); return }
      setSearchLoading(true)
      try{
        const res = await admin.searchUsers(q)
        if (!mounted) return
        if (res.ok && res.data) setSearchResults(res.data.users)
        else setSearchResults([])
      }catch(e){
        console.error('User search failed', e)
        if (mounted) setSearchResults([])
      }finally{
        if (mounted) setSearchLoading(false)
      }
    }
    // debounce
    timer = setTimeout(doSearch, 300)
    return ()=>{ mounted = false; if (timer) clearTimeout(timer) }
  },[searchQuery, modalMode])

  return (
    <div className={rootClass}>
      <div className="admin-pane">
        <div className="admin-left">
          <h3>Courses</h3>
          <div style={{marginBottom:8}}>
            <button onClick={openCreateCourse} style={{width:'100%'}}>New Course</button>
          </div>
          <ul>
            {courses.map(c=> (
              <li key={c.id} style={{display:'flex',gap:8,alignItems:'center'}}>
                <button style={{flex:1,textAlign:'left'}} onClick={()=>{setSelectedCourse(c); loadAssignments(c.id); loadMembers(c.id)}}>{c.title}</button>
                <button onClick={()=>openEditCourse(c)} style={{marginLeft:6}}>Edit</button>
                <button onClick={()=>{ setModalMode('confirmDeleteCourse'); setModalPayload({ courseId: c.id, courseTitle: c.title }); setModalOpen(true) }} style={{marginLeft:6,background:'#e74c3c'}}>Del</button>
              </li>
            ))}
          </ul>
        </div>
        <div className="admin-center">
          <h3>Assignments</h3>
          {selectedCourse && <div><strong>{selectedCourse.title}</strong></div>}
          {selectedCourse && (
            <div style={{marginTop:8,marginBottom:8}}>
              <strong>Members</strong>
              <div style={{marginTop:6,marginBottom:6}}>
                <button onClick={()=>{ setModalMode('enrollMember'); setModalPayload({ email: '', role: 'student' }); setSearchQuery(''); setSearchResults([]); setSelectedUser(null); setModalOpen(true) }} style={{width:'100%'}}>Enroll Student</button>
              </div>
              <ul style={{marginTop:6,marginBottom:6}}>
                {members.map(m => (
                  <li key={m.id} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'6px 0'}}>
                    <div>{m.name || m.email} — <small style={{color:'#666'}}>{m.role}</small></div>
                    <div>
                      <button onClick={()=>{ setModalMode('changeRole'); setModalPayload({ userId: m.id, role: m.role }); setModalOpen(true) }} style={{marginRight:8}}>Change</button>
                      <button onClick={()=>{ setModalMode('confirmRemoveMember'); setModalPayload({ userId: m.id, userName: m.name || m.email }); setModalOpen(true) }} style={{background:'#e74c3c'}}>Remove</button>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
          <div style={{marginBottom:8}}>
            {selectedCourse && <button onClick={()=>{ setModalMode('createAssignment'); setModalPayload({ title: '', questions: [], type: 'assignment', time_limit_minutes: null }); setFdTextMap({}); setModalOpen(true); refreshDbList() }} style={{width:'100%'}}>New Assignment</button>}
          </div>
          <ul>
            {assignments.map(a=> (
              <li key={a.id} style={{display:'flex',gap:8,alignItems:'center'}}>
                <button style={{flex:1,textAlign:'left'}} onClick={()=>{setSelectedAssignment(a); loadSubmissions(a.id)}}>{a.title}</button>
                <button onClick={async ()=>{ setModalMode('editAssignment'); setModalPayload({ id: a.id, title: a.title, courseId: selectedCourse?.id, questions: [] }); setModalOpen(true); await refreshDbList(); await loadAssignmentQuestions(a.id) }} style={{marginLeft:6}}>Edit</button>
                <button onClick={()=>{ setModalMode('confirmDeleteAssignment'); setModalPayload({ assignmentId: a.id, assignmentTitle: a.title }); setModalOpen(true) }} style={{marginLeft:6,background:'#e74c3c'}}>Del</button>
              </li>
            ))}
          </ul>
        </div>
        <div className="admin-right">
          <h3>Submissions</h3>
          <ul>
            {submissions.map(s => (
              <li key={s.submission_id} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'6px 0'}}>
                <div>
                  <div><strong>Student</strong> {s.student_name || s.student_id} <small style={{color:'#666'}}>— {new Date(s.created_at||s.created||s.timestamp||Date.now()).toLocaleString()}</small></div>
                  <div style={{color:'#222'}}>Score: {s.score ?? 'ungraded'}</div>
                </div>
                <div>
                  <button onClick={async ()=>{
                    // load submission details if API available
                    try{
                      const res = await admin.getSubmissionDetails ? await admin.getSubmissionDetails(s.submission_id) : null
                      if (res && res.ok && res.data){
                        setModalPayload({ viewSubmission: res.data.submission });
                      } else {
                        // fall back to payload we already have
                        setModalPayload({ viewSubmission: s });
                      }
                    }catch(e){ setModalPayload({ viewSubmission: s }) }
                    setModalMode('viewSubmission'); setModalOpen(true)
                  }} style={{marginRight:8}}>View</button>
                  <button onClick={()=>{ setModalMode('gradeSubmission'); setModalPayload({ submission_id: s.submission_id, score: s.score }); setModalOpen(true) }} style={{marginLeft:8}}>Grade</button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <button onClick={onClose}>{fullPage ? 'Back' : 'Close'}</button>

          {modalOpen && (
        <Modal
          title={
            modalMode==='createCourse'?'Create Course':
            modalMode==='editCourse'?'Edit Course':
            modalMode==='createAssignment'?'Create Assignment':
            modalMode==='editAssignment'?'Edit Assignment':
            modalMode==='enrollMember'?'Enroll Member':
            modalMode==='changeRole'?'Change Role':
            modalMode==='confirmDeleteCourse'?'Confirm Delete':
            modalMode==='confirmRemoveMember'?'Confirm Remove':
            modalMode==='confirmDeleteAssignment'?'Confirm Delete':
            modalMode==='gradeSubmission'?'Grade Submission':
            modalMode==='viewSubmission'?'View Submission':''
          }
          onClose={()=>{
            if (modalSubmitting) return
            // If we opened an editQuestion from within another modal, return
            // to that previous modal instead of closing everything.
            if (modalMode === 'editQuestion' && modalPrevMode){
              setModalMode(modalPrevMode)
              setModalPrevMode(null)
              // clear transient edit fields
              setModalPayload(p=>{ const mp = {...p}; delete mp.question_id; delete mp.solution_query; delete mp.question_index; return mp })
              return
            }
            setModalOpen(false)
          }}
          onSubmit={async ()=>{
            setModalSubmitting(true)
            try{
              if (modalMode==='createCourse' || modalMode==='editCourse'){
                await submitCourseModal()
                  } else if (modalMode==='createAssignment'){
                    const t = (modalPayload.title||'').trim(); if (!t){ alert('Title required'); return }
                    const payload = { title: t, questions: modalPayload.questions || [], type: modalPayload.type || 'assignment', time_limit_minutes: modalPayload.time_limit_minutes || null }
                    const res = await admin.createAssignment(selectedCourse.id, payload)
                    if (res.ok) { loadAssignments(selectedCourse.id); setModalOpen(false) } else alert('Create failed')
              } else if (modalMode==='editAssignment'){
                const t = (modalPayload.title||'').trim(); if (!t){ alert('Title required'); return }
                const payload = { title: t, questions: modalPayload.questions || [], type: modalPayload.type || 'assignment', time_limit_minutes: modalPayload.time_limit_minutes || null }
                const res = await admin.updateAssignment(modalPayload.id, payload)
                if (res.ok) { loadAssignments(modalPayload.courseId); setModalOpen(false) } else alert('Update failed')
              } else if (modalMode==='enrollMember'){
                const e = (modalPayload.email||'').trim(); if (!e){ alert('Email required'); return }
                const res = await admin.enrollMember(selectedCourse.id, { email: e, role: modalPayload.role })
                if (res.ok) { loadMembers(selectedCourse.id); setModalOpen(false) } else alert('Enroll failed')
              } else if (modalMode==='changeRole'){
                const res = await admin.updateMember(selectedCourse.id, modalPayload.userId, { role: modalPayload.role })
                if (res.ok) { loadMembers(selectedCourse.id); setModalOpen(false) } else alert('Update failed')
              } else if (modalMode==='confirmDeleteCourse'){
                const res = await admin.deleteCourse(modalPayload.courseId)
                if (res.ok){ await refreshCourses(); setModalOpen(false) } else alert('Delete failed')
              } else if (modalMode==='confirmRemoveMember'){
                const res = await admin.removeMember(selectedCourse.id, modalPayload.userId)
                if (res.ok){ await loadMembers(selectedCourse.id); setModalOpen(false) } else alert('Remove failed')
              } else if (modalMode==='confirmDeleteAssignment'){
                const res = await admin.deleteAssignment(modalPayload.assignmentId)
                if (res.ok){ await loadAssignments(selectedCourse.id); setModalOpen(false) } else alert('Delete failed')
              } else if (modalMode==='gradeSubmission'){
                const scoreVal = parseFloat(modalPayload.score)
                if (Number.isNaN(scoreVal)){ alert('Invalid score'); return }
                const res = await admin.gradeSubmission(modalPayload.submission_id, { score: scoreVal, feedback: { note: 'graded via admin UI' } })
                if (res.ok){ await loadSubmissions(selectedAssignment.id); setModalOpen(false) } else alert('Grade failed')
              } else if (modalMode==='viewSubmission'){
                // simply close on submit
                setModalOpen(false)
              } else if (modalMode==='editQuestion'){
                // Update a single question's solution_query.
                // If this is an unsaved/new question (no question_id), write the
                // solution into the local modalPayload.questions array at
                // modalPayload.question_index so it will be saved with the
                // parent assignment when the assignment is saved.
                const qid = modalPayload.question_id
                const sol = (modalPayload.solution_query||'').trim()
                if (!sol){ alert('Solution query is required'); return }
                if (!qid){
                  // local question: update modalPayload.questions
                  setModalPayload(p=>{
                    const mp = {...p}
                    if (mp.questions && mp.question_index !== undefined){
                      const qs = (mp.questions||[]).slice()
                      qs[mp.question_index] = {...qs[mp.question_index], solution_query: sol}
                      mp.questions = qs
                    }
                    return mp
                  })
                  // If this edit was invoked from another modal, restore that mode
                  if (modalPrevMode){
                    setModalMode(modalPrevMode)
                    setModalPrevMode(null)
                    // clear transient edit fields
                    setModalPayload(p=>{ const mp = {...p}; delete mp.question_id; delete mp.solution_query; delete mp.question_index; return mp })
                  } else {
                    setModalOpen(false)
                  }
                } else {
                  const res = await admin.updateQuestion(qid, { solution_query: sol })
                  if (res && res.ok){
                    // update local modalPayload.questions if present
                    setModalPayload(p=>{
                      const mp = {...p}
                      if (mp.questions && mp.question_index !== undefined){
                        const qs = (mp.questions||[]).slice()
                        qs[mp.question_index] = {...qs[mp.question_index], solution_query: sol}
                        mp.questions = qs
                      }
                      return mp
                    })
                    if (modalPrevMode){
                      setModalMode(modalPrevMode)
                      setModalPrevMode(null)
                      setModalPayload(p=>{ const mp = {...p}; delete mp.question_id; delete mp.solution_query; delete mp.question_index; return mp })
                    } else {
                      setModalOpen(false)
                    }
                  } else {
                    alert('Save failed')
                  }
                }
              }
            }catch(e){
              console.error('Modal action failed', e)
              alert('Action failed')
            }finally{
              setModalSubmitting(false)
            }
          }} submitLabel={modalMode && modalMode.startsWith('confirm') ? 'Delete' : modalMode==='gradeSubmission' ? 'Save' : modalMode==='viewSubmission' ? 'Close' : 'Save'} submitting={modalSubmitting} submitDisabled={computeModalValidation().disabled} submitDisabledReason={computeModalValidation().reason}>
          <div style={{display:'flex',flexDirection:'column',gap:8}}>
            {(modalMode==='createCourse' || modalMode==='editCourse') && (
              <>
                <label>Title</label>
                <input type="text" value={modalPayload.title||''} onChange={e=>setModalPayload(p=>({...p,title:e.target.value}))} />
                {modalMode==='editCourse' && (
                  <div style={{marginTop:12,borderTop:'1px solid #eee',paddingTop:12}}>
                    <label style={{display:'block',marginBottom:6}}>Manage Databases</label>
                    <div style={{display:'flex',gap:8,marginBottom:8}}>
                      <button onClick={refreshDbList}>Refresh DBs</button>
                    </div>
                    <div style={{display:'flex',gap:8,alignItems:'center',marginBottom:8}}>
                      <input type="file" id="course-dbfile" accept=".db,.sqlite,.sqlite3" />
                      <button onClick={async ()=>{
                        const el = document.getElementById('course-dbfile')
                        if (!el || !el.files || el.files.length===0){ alert('Pick a file'); return }
                        const f = el.files[0]
                        const allowed = ['.db','.sqlite','.sqlite3']
                        const name = f.name || ''
                        const dot = name.lastIndexOf('.')
                        const ext = dot >= 0 ? name.slice(dot).toLowerCase() : ''
                        if (!allowed.includes(ext)){
                          alert('Unsupported file type. Please upload a .db or .sqlite file.')
                          return
                        }
                        await uploadDatabase(f, f.name)
                        await refreshDbList()
                      }} disabled={dbUploading}>{dbUploading ? 'Uploading...' : 'Upload'}</button>
                    </div>
                    <div style={{maxHeight:160,overflow:'auto',border:'1px solid #f0f0f0',padding:8,borderRadius:6}}>
                      {dbList.length===0 && <div style={{color:'#666'}}>No databases uploaded.</div>}
                      {dbList.map(d=> (
                        <div key={d.id} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'6px 0',borderBottom:'1px dashed #f0f0f0'}}>
                          <div style={{flex:1}}>{d.name} <small style={{color:'#666'}}>({new Date(d.uploaded_at).toLocaleString()})</small></div>
                          <div>
                            <button onClick={()=>openDbPreview(d.id, d.name)} style={{marginRight:8}}>Preview</button>
                            <button onClick={async ()=>{
                              if (!confirm(`Delete database "${d.name}"? This cannot be undone.`)) return
                              try{
                                const res = await admin.deleteDatabase(d.id)
                                if (res.ok) { await refreshDbList(); } else { alert('Delete failed') }
                              }catch(e){ console.error('Delete failed', e); alert('Delete failed') }
                            }} style={{background:'#e74c3c'}}>Delete</button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
            {(modalMode==='createAssignment' || modalMode==='editAssignment') && (
              <>
                <label>Title</label>
                <input type="text" value={modalPayload.title||''} onChange={e=>setModalPayload(p=>({...p,title:e.target.value}))} />

                {/* database upload moved to course edit modal */}

                <div style={{marginTop:8}}>
                  <label>Assignment Type</label>
                  <select value={modalPayload.type || 'assignment'} onChange={e=>setModalPayload(p=>({...p, type: e.target.value}))}>
                    <option value="assignment">Assignment</option>
                    <option value="quiz">Quiz</option>
                    <option value="exam">Exam</option>
                  </select>
                  <div style={{marginTop:8}}>
                    <label>Time limit (minutes, optional)</label>
                    <input type="number" min="0" value={modalPayload.time_limit_minutes || ''} onChange={e=>setModalPayload(p=>({...p, time_limit_minutes: e.target.value ? parseInt(e.target.value) : null}))} />
                  </div>
                
                  <label>Questions</label>
                  <div style={{display:'flex',flexDirection:'column',gap:8}}>
                    {(modalPayload.questions||[]).map((q, idx)=>{
                      const qtype = (q.question_type || 'ra').toLowerCase()
                      return (
                      <div key={idx} style={{padding:8,border:'1px solid #eee',borderRadius:6,display:'flex',flexDirection:'column',gap:6}}>
                        <div style={{display:'flex',gap:8}}>
                          <input placeholder="Prompt" style={{flex:1}} value={q.prompt||''} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs[idx] = {...qs[idx], prompt: e.target.value}; return {...p, questions: qs} })} />
                          <input placeholder="Points" type="number" style={{width:88}} value={q.points||0} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs[idx] = {...qs[idx], points: parseInt(e.target.value||0)}; return {...p, questions: qs} })} />
                        </div>
                        <div style={{display:'flex',gap:8,alignItems:'center',flexWrap:'wrap'}}>
                          <label style={{margin:0}}>Type</label>
                          <select value={qtype} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); const newType = e.target.value; const defaultForms = ['1NF','2NF','3NF','BCNF','4NF','5NF'];
                            qs[idx] = {
                              ...qs[idx],
                              question_type: newType,
                              // initialize defaults when switching types
                              options_json: newType==='norm' ? ({ forms: (qs[idx]?.options_json?.forms || defaultForms) }) : (newType==='mcq' || newType==='msq' ? ({ choices: (qs[idx]?.options_json?.choices || []) }) : qs[idx]?.options_json),
                              answer_key_json: newType==='norm' ? (qs[idx]?.answer_key_json || { correct_forms: [] }) : qs[idx]?.answer_key_json
                            };
                            return {...p, questions: qs} })}>
                            <option value="ra">RA Query</option>
                            <option value="mcq">Multiple Choice</option>
                            <option value="msq">Multi-Select</option>
                            <option value="free">Free Response</option>
                            <option value="norm">Normalization</option>
                            <option value="sql">SQL Query</option>
                          </select>
                          {qtype === 'ra' && (
                            <>
                              <label style={{margin:0}}>Database</label>
                              <select value={q.db_id||''} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs[idx] = {...qs[idx], db_id: e.target.value||null}; return {...p, questions: qs} })}>
                                <option value="">(none)</option>
                                {dbList.map(d=> (<option key={d.id} value={d.id}>{d.name}</option>))}
                              </select>
                              {q.db_id && <button onClick={()=>{ const db = dbList.find(x=>String(x.id)===String(q.db_id)); openDbPreview(q.db_id, db?db.name:'' ) }} style={{marginLeft:6}}>Preview</button>}
                            </>
                          )}
                          <div style={{flexBasis:'100%', display:'flex', gap:8, alignItems:'center', marginTop:6}}>
                            <label style={{margin:0}}>Submission limit</label>
                            <input type="number" min="0" style={{width:80}} value={(q.submission_limit===undefined || q.submission_limit===null) ? 0 : q.submission_limit} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs[idx] = {...qs[idx], submission_limit: parseInt(e.target.value||0)}; return {...p, questions: qs} })} />
                          </div>
                          <div style={{width:'100%', display:'flex', justifyContent:'flex-end', marginTop:6}}>
                            <button onClick={()=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs.splice(idx,1); return {...p, questions: qs} })} style={{background:'#e74c3c'}}>Remove</button>
                          </div>
                        </div>
                        {qtype === 'ra' ? (
                          <>
                            <button onClick={()=>{
                              setModalPrevMode(modalMode)
                              setModalPayload(p=>({...p, question_id: q.id, solution_query: q.solution_query || '', question_index: idx }))
                              setModalMode('editQuestion')
                              setModalOpen(true)
                            }} style={{alignSelf:'flex-start'}}>Edit Solution</button>
                            {!q.solution_query || String(q.solution_query).trim()==='' ? (
                              <div style={{color:'red',fontSize:12}}>Solution query is required. Click "Edit Solution" to add one.</div>
                            ) : (
                              <div style={{color:'#666',fontSize:12}}>Solution query set</div>
                            )}
                          </>
                        ) : (
                          <>
                            {qtype === 'mcq' && (
                              <div style={{display:'flex',flexDirection:'column',gap:6}}>
                                <label style={{fontSize:12,fontWeight:'bold'}}>Options (one per line)</label>
                                <textarea rows={4} placeholder="A) Option 1&#10;B) Option 2&#10;C) Option 3" value={(q.options_json?.choices || []).join('\n')} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs[idx] = {...qs[idx], options_json: { choices: e.target.value.split('\n') }}; return {...p, questions: qs} })} />
                                <label style={{fontSize:12,fontWeight:'bold'}}>Correct Answer (e.g., "A" or index 0)</label>
                                <textarea rows={2} placeholder="A" value={q.answer_key_json?.correct || ''} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs[idx] = {...qs[idx], answer_key_json: { ...qs[idx].answer_key_json, correct: e.target.value }}; return {...p, questions: qs} })} />
                              </div>
                            )}
                            {qtype === 'msq' && (
                              <div style={{display:'flex',flexDirection:'column',gap:6}}>
                                <label style={{fontSize:12,fontWeight:'bold'}}>Options (one per line)</label>
                                <textarea rows={4} placeholder="A) Option 1&#10;B) Option 2&#10;C) Option 3" value={(q.options_json?.choices || []).join('\n')} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs[idx] = {...qs[idx], options_json: { choices: e.target.value.split('\n') }}; return {...p, questions: qs} })} />
                                <label style={{fontSize:12,fontWeight:'bold'}}>Correct Answers (select from options above)</label>
                                <div style={{display:'flex',flexDirection:'column',gap:4,maxHeight:150,overflowY:'auto',border:'1px solid #ddd',borderRadius:4,padding:8,background:'#fafafa'}}>
                                  {(q.options_json?.choices || []).map((choice, cidx) => (
                                    <label key={cidx} style={{display:'flex',alignItems:'center',gap:6,cursor:'pointer'}}>
                                      <input
                                        type="checkbox"
                                        checked={(q.answer_key_json?.correct || []).includes(choice)}
                                        onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); const current = new Set(qs[idx]?.answer_key_json?.correct || []); if (e.target.checked) current.add(choice); else current.delete(choice); qs[idx] = {...qs[idx], answer_key_json: { ...qs[idx].answer_key_json, correct: Array.from(current) }}; return {...p, questions: qs} })}
                                      />
                                      <span style={{fontSize:12}}>{choice}</span>
                                    </label>
                                  ))}
                                </div>
                              </div>
                            )}
                            {qtype === 'norm' && (
                              <div style={{display:'flex',flexDirection:'column',gap:6}}>
                                <label style={{fontSize:12,fontWeight:'bold'}}>Normal Forms (select options to present)</label>
                                {(() => { const defaultForms = ['1NF','2NF','3NF','BCNF','4NF','5NF']; const forms = (q.options_json?.forms || defaultForms);
                                  return (
                                    <div style={{display:'flex',flexWrap:'wrap',gap:8}}>
                                      {forms.map(form => (
                                        <label key={form} style={{display:'inline-flex',alignItems:'center',gap:6,border:'1px solid #eee',padding:'4px 8px',borderRadius:4}}>
                                          <input type="checkbox" checked={(q.answer_key_json?.correct_forms || []).includes(form)} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); const current = new Set(qs[idx]?.answer_key_json?.correct_forms || []); if (e.target.checked) current.add(form); else current.delete(form); qs[idx] = {...qs[idx], answer_key_json: { ...(qs[idx]?.answer_key_json||{}), correct_forms: Array.from(current) }}; return {...p, questions: qs} })} />
                                          <span>{form}</span>
                                        </label>
                                      ))}
                                    </div>
                                  ) })()}
                                <div style={{display:'flex',gap:8,alignItems:'center',marginTop:6}}>
                                  <label style={{margin:0}}>Target NF (optional)</label>
                                  <select value={(q.answer_key_json?.target_nf || '').toString()} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); const prev = qs[idx]?.answer_key_json || {}; qs[idx] = {...qs[idx], answer_key_json: { ...prev, target_nf: e.target.value }}; return {...p, questions: qs} })}>
                                    <option value="">(none)</option>
                                    <option value="1NF">1NF</option>
                                    <option value="2NF">2NF</option>
                                    <option value="3NF">3NF</option>
                                    <option value="BCNF">BCNF</option>
                                    <option value="4NF">4NF</option>
                                    <option value="5NF">5NF</option>
                                  </select>
                                </div>
                                <div style={{marginTop:6}}>
                                  <label style={{fontSize:12,fontWeight:'bold'}}>Functional Dependencies (one per line, e.g., "E → N,R,D")</label>
                                  <textarea rows={4} placeholder="A,B → C
T → K" value={fdTextMap[idx] || ''} onChange={e=>{
  const text = e.target.value
  setFdTextMap(prev => ({...prev, [idx]: text}))
}} onBlur={e=>{
  // Parse FDs on blur
  const lines = e.target.value.split('\n')
  const fds = lines.map(line => {
    const parts = line.split('->')
    if (parts.length<2) return null
    const lhs = parts[0].split(',').map(s=>s.trim()).filter(Boolean)
    const rhs = parts[1].split(',').map(s=>s.trim()).filter(Boolean)
    if (lhs.length===0 || rhs.length===0) return null
    return { lhs, rhs }
  }).filter(Boolean)
  setModalPayload(p=>{
    const qs = (p.questions||[]).slice()
    const prevOptions = qs[idx]?.options_json || {}
    qs[idx] = {...qs[idx], options_json: { ...prevOptions, schema: { ...(prevOptions.schema||{}), fds } } }
    return {...p, questions: qs}
  })
}} />
                                </div>
                                <div style={{marginTop:8}}>
                                  <label style={{fontSize:12}}>Optional: Acceptable textual answers (one per line) or regex</label>
                                  <textarea rows={3} placeholder="Correct answer 1&#10;Correct answer 2" value={(q.answer_key_json?.acceptable || []).join('\n')} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); const prev = qs[idx]?.answer_key_json || {}; qs[idx] = {...qs[idx], answer_key_json: { ...prev, acceptable: e.target.value.split('\n') }}; return {...p, questions: qs} })} />
                                  <input placeholder="Regex (optional)" value={q.answer_key_json?.regex || ''} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); const prev = qs[idx]?.answer_key_json || {}; qs[idx] = {...qs[idx], answer_key_json: { ...prev, regex: e.target.value }}; return {...p, questions: qs} })} />
                                  <label style={{fontSize:12,marginTop:8,display:'block'}}>Optional: Accepted decomposition signatures (one per line)</label>
                                  <textarea rows={3} placeholder="{A,B} | {C,D}&#10;{P,E,N,R} | {T,K,H,D,M}" value={(q.answer_key_json?.decomposition_signatures || []).join('\n')} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); const prev = qs[idx]?.answer_key_json || {}; qs[idx] = {...qs[idx], answer_key_json: { ...prev, decomposition_signatures: e.target.value.split('\n').map(s=>s.trim()).filter(Boolean) }}; return {...p, questions: qs} })} />
                                </div>
                              </div>
                            )}
                            {qtype === 'free' && (
                              <div style={{display:'flex',flexDirection:'column',gap:6}}>
                                <label style={{fontSize:12,fontWeight:'bold'}}>Acceptable Answers (one per line)</label>
                                <textarea rows={3} placeholder="Correct answer 1&#10;Correct answer 2" value={(q.answer_key_json?.acceptable || []).join('\n')} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs[idx] = {...qs[idx], answer_key_json: { acceptable: e.target.value.split('\n'), regex: qs[idx]?.answer_key_json?.regex }}; return {...p, questions: qs} })} />
                                <label style={{fontSize:12,fontWeight:'bold'}}>Or Regex Pattern (optional)</label>
                                <input placeholder="^[0-9]+NF$" value={q.answer_key_json?.regex || ''} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs[idx] = {...qs[idx], answer_key_json: { acceptable: qs[idx]?.answer_key_json?.acceptable || [], regex: e.target.value }}; return {...p, questions: qs} })} />
                              </div>
                            )}
                            {qtype === 'sql' && (
                              <div style={{display:'flex',flexDirection:'column',gap:6}}>
                                <label style={{fontSize:12,fontWeight:'bold'}}>Database</label>
                                <select value={(q.options_json?.database_file_id || '')} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs[idx] = {...qs[idx], options_json: {...(qs[idx]?.options_json || {}), database_file_id: e.target.value ? parseInt(e.target.value) : null}}; return {...p, questions: qs} })}>
                                  <option value="">-- Select a database --</option>
                                  {dbList.map(db => (
                                    <option key={db.id} value={db.id}>{db.name || db.filename || String(db.id)}</option>
                                  ))}
                                </select>
                                <label style={{fontSize:12,fontWeight:'bold'}}>Expected Result SQL Query</label>
                                <textarea rows={6} placeholder="SELECT id, name, age FROM users ORDER BY id" value={(q.answer_key_json?.expected_result_sql || '')} onChange={e=>setModalPayload(p=>{ const qs = (p.questions||[]).slice(); qs[idx] = {...qs[idx], answer_key_json: {...(qs[idx]?.answer_key_json || {}), expected_result_sql: e.target.value}}; return {...p, questions: qs} })} style={{width:'100%', fontFamily:'monospace'}} />
                              </div>
                            )}
                          </>
                        )}
                      </div>
                    )})}
                    <button onClick={()=>{
                      const newIdx = (modalPayload.questions||[]).length
                      setModalPayload(p=>({...p, questions: [...(p.questions||[]), { prompt:'', points:10, db_id: null, question_type: 'ra' }]}))
                      setFdTextMap(prev => ({...prev, [newIdx]: ''}))
                    }}>Add question</button>
                  </div>
                </div>
              </>
            )}
            {modalMode==='enrollMember' && (
              <>
                <label>Find user by name or email</label>
                <input type="text" placeholder="Search users..." value={searchQuery} onChange={e=>setSearchQuery(e.target.value)} />
                <div style={{marginTop:8,maxHeight:160,overflow:'auto',border:'1px solid #eee',borderRadius:6,padding:8}}>
                  {searchLoading && <div>Searching...</div>}
                  {!searchLoading && searchResults.length===0 && <div style={{color:'#666'}}>No matches. You can create a new user below by entering an email.</div>}
                  {!searchLoading && searchResults.map(u => (
                    <div key={u.id} style={{padding:'6px',display:'flex',justifyContent:'space-between',alignItems:'center',background:selectedUser?.id===u.id? '#eef' : 'transparent',borderRadius:4,marginBottom:4}}>
                      <div style={{flex:1,cursor:'pointer'}} onClick={()=>{ setSelectedUser(u); setModalPayload(p=>({...p,email:u.email,role:p.role})); }}>{u.name || u.email} <small style={{color:'#666'}}>— {u.email}</small></div>
                      <div><button onClick={()=>{ setSelectedUser(u); setModalPayload(p=>({...p,email:u.email,role:p.role})); }} style={{padding:'6px 8px'}}>Select</button></div>
                    </div>
                  ))}
                </div>
                <div style={{marginTop:8}}>
                  <label>Or create new (email)</label>
                  <input type="email" value={modalPayload.email||''} onChange={e=>{ setSelectedUser(null); setModalPayload(p=>({...p,email:e.target.value})) }} />
                </div>
                <label style={{marginTop:8}}>Role</label>
                <select value={modalPayload.role||'student'} onChange={e=>setModalPayload(p=>({...p,role:e.target.value}))}>
                  <option value="student">student</option>
                  <option value="ta">ta</option>
                  <option value="instructor">instructor</option>
                </select>
              </>
            )}
            {modalMode==='changeRole' && (
              <>
                <label>Role</label>
                <select value={modalPayload.role||'student'} onChange={e=>setModalPayload(p=>({...p,role:e.target.value}))}>
                  <option value="student">student</option>
                  <option value="ta">ta</option>
                  <option value="instructor">instructor</option>
                </select>
              </>
            )}
            {modalMode==='confirmDeleteCourse' && (
              <div>Are you sure you want to delete the course "{modalPayload.courseTitle}"? This cannot be undone.</div>
            )}
            {modalMode==='confirmRemoveMember' && (
              <div>Remove {modalPayload.userName} from this course?</div>
            )}
            {modalMode==='confirmDeleteAssignment' && (
              <div>Are you sure you want to delete the assignment "{modalPayload.assignmentTitle}"? This cannot be undone.</div>
            )}
            {modalMode==='gradeSubmission' && (
              <>
                <label>Score</label>
                <input type="number" step="0.1" value={modalPayload.score||''} onChange={e=>setModalPayload(p=>({...p,score:e.target.value}))} />
              </>
            )}
            {modalMode==='editQuestion' && (
              <>
                <label>Solution Query (required)</label>
                <textarea rows={6} value={modalPayload.solution_query||''} onChange={e=>setModalPayload(p=>({...p,solution_query:e.target.value}))} style={{width:'100%'}} />
              </>
            )}
            {modalMode==='viewSubmission' && (
              <div style={{display:'flex',flexDirection:'column',gap:8}}>
                {modalPayload.viewSubmission ? (
                  (()=>{
                    const s = modalPayload.viewSubmission
                    return (
                      <div>
                        <div><strong>Submission ID:</strong> {s.submission_id || s.id}</div>
                        <div><strong>Student:</strong> {s.student_name || s.student_id}</div>
                        <div><strong>Score:</strong> {s.score ?? 'ungraded'}</div>
                        <div style={{marginTop:8}}><strong>Submitted Query</strong>
                          <pre style={{background:'#f8f8f8',padding:8,borderRadius:4,overflow:'auto'}}>{s.query || s.answer || s.sql || JSON.stringify(s.query_text||s.payload||'')}</pre>
                        </div>
                        {s.feedback && <div style={{marginTop:8}}><strong>Feedback</strong><pre style={{background:'#fff',padding:8,borderRadius:4}}>{JSON.stringify(s.feedback,null,2)}</pre></div>}
                        {s.result && <div style={{marginTop:8}}><strong>Result</strong><pre style={{background:'#f8f8f8',padding:8,borderRadius:4,overflow:'auto'}}>{typeof s.result === 'string' ? s.result : JSON.stringify(s.result,null,2)}</pre></div>}
                      </div>
                    )
                  })()
                ) : (
                  <div>No submission details available.</div>
                )}
              </div>
            )}
          </div>
        </Modal>
      )}
      {dbPreviewOpen && (
        <Modal title={`Database Preview: ${dbPreviewName||''}`} onClose={()=>{ setDbPreviewOpen(false); setDbPreview(null); setDbPreviewName('') }} submitLabel="Close" onSubmit={()=>{ setDbPreviewOpen(false); setDbPreview(null); setDbPreviewName('') }}>
          <div style={{maxHeight:400,overflow:'auto'}}>
            {(!dbPreview || dbPreview.length===0) && <div style={{color:'#666'}}>No tables found.</div>}
            {(dbPreview||[]).map((t, i)=> (
              <div key={i} style={{padding:8,borderBottom:'1px solid #eee'}}>
                <strong>{t.name}</strong>
                <div style={{color:'#666',marginTop:6}}>Columns: { (t.columns||[]).join(', ') }</div>
                <div style={{marginTop:6}}>
                  {(t.sample||[]).length===0 && <div style={{color:'#666'}}>No sample rows.</div>}
                  {(t.sample||[]).map((r,ri)=> (
                    <pre key={ri} style={{background:'#f8f8f8',padding:6,borderRadius:4,overflow:'auto'}}>{JSON.stringify(r)}</pre>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Modal>
      )}
    </div>
  )
}
