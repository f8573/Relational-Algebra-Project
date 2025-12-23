import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Modal from '../components/Modal'
import api, { admin } from '../lib/api'

export default function AssignmentView(){
  const { id } = useParams()
  const navigate = useNavigate()
  const [assignment, setAssignment] = useState(null)
  const [submissions, setSubmissions] = useState([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [title, setTitle] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(()=>{
    let mounted = true
    const load = async ()=>{
      setLoading(true)
      try{
        // load submissions (current user)
        const sres = await api.getAssignmentSubmissions(id)
        if (mounted && sres.ok && sres.data) setSubmissions(sres.data.submissions || [])
        // attempt to find assignment metadata by scanning course assignments
        const cres = await admin.listCourses()
        if (mounted && cres.ok && cres.data){
          for (const c of (cres.data.courses||[])){
            const ares = await admin.getCourseAssignments(c.id)
            if (ares.ok && ares.data){
              const found = (ares.data.assignments||[]).find(a=>String(a.id)===String(id))
              if (found){
                setAssignment({...found, course: c})
                setTitle(found.title || '')
                break
              }
            }
          }
        }
      }catch(e){
        console.error('Failed loading assignment', e)
      }finally{
        if (mounted) setLoading(false)
      }
    }
    load()
    return ()=>{ mounted = false }
  },[id])

  const handleSave = async ()=>{
    setSaving(true)
    try{
      const res = await admin.updateAssignment(id, { title })
      if (res.ok){
        setAssignment(a=>({...a, title}))
        setEditing(false)
      } else {
        alert('Save failed')
      }
    }catch(e){
      console.error('Save error', e)
      alert('Network error')
    }finally{ setSaving(false) }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div style={{padding:16}}>
      <button onClick={()=>navigate(-1)} style={{marginBottom:12}}>Back</button>
      <h2>{assignment ? assignment.title : `Assignment ${id}`}</h2>
      {assignment && <div style={{color:'#666',marginBottom:8}}>Course: {assignment.course?.title || '—'}</div>}
      <div style={{marginBottom:12}}>
        <button onClick={()=>setEditing(true)}>Edit Assignment</button>
      </div>

      <h3>Submissions</h3>
      <ul>
        {submissions.map(s=> (
          <li key={s.submission_id}>{s.student_id} — Score: {s.score}</li>
        ))}
      </ul>

      {editing && (
        <Modal title="Edit Assignment" onClose={()=>setEditing(false)} onSubmit={handleSave} submitting={saving} submitLabel="Save">
          <div style={{display:'flex',flexDirection:'column',gap:8}}>
            <label>Title</label>
            <input value={title} onChange={e=>setTitle(e.target.value)} />
          </div>
        </Modal>
      )}
    </div>
  )
}
