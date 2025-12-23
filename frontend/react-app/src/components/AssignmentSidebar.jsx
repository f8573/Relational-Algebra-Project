import React, { useEffect, useState } from 'react'
import api from '../lib/api'

export default function AssignmentSidebar({ course, selectedAssignment, onSelect }){
  const [assignments, setAssignments] = useState([])
  const [loading, setLoading] = useState(false)
  const [showGrades, setShowGrades] = useState(false)

  useEffect(()=>{
    let mounted = true
    if (!course) { setAssignments([]); return }
    const load = async ()=>{
      setLoading(true)
      try{
        const res = await api.getCourseAssignmentsPublic(course.id)
        if (!mounted) return
        if (res.ok && res.data) setAssignments(res.data.assignments || [])
        else setAssignments([])
      }catch(e){
        console.error('Failed loading assignments', e)
        if (mounted) setAssignments([])
      }finally{ if (mounted) setLoading(false) }
    }
    load()
    const handler = ()=>{ load() }
    window.addEventListener('assignments:refresh', handler)
    return ()=>{ mounted = false; window.removeEventListener('assignments:refresh', handler) }
  },[course])

  if (!course) return null

  return (
    <div style={{width:260,marginRight:12}} className="left">
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between'}}>
        <h3 style={{marginTop:0}}>Assignments</h3>
        <button onClick={()=>setShowGrades(g=>!g)} style={{fontSize:12,padding:'4px 8px'}}>{showGrades ? 'Hide Grades' : 'Grades'}</button>
      </div>
      {showGrades && (
        <div style={{marginBottom:8,padding:8,background:'#fff',border:'1px solid #eee',borderRadius:6}}>
          <strong style={{display:'block',marginBottom:6}}>Grades</strong>
          {loading && <div>Loading...</div>}
          {!loading && assignments.length===0 && <div style={{color:'#666'}}>No assignments</div>}
          {!loading && assignments.map(a => (
            <div key={a.id} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'6px 0',borderBottom:'1px dashed #f6f6f6'}}>
              <div style={{flex:1,overflow:'hidden',whiteSpace:'nowrap',textOverflow:'ellipsis'}}>{a.title}</div>
              <div style={{marginLeft:8,textAlign:'right'}}>
                {a.user_points != null || a.user_grade != null || a.percent != null ? (
                  <div style={{fontWeight:700}}>
                    {a.user_points != null ? `${a.user_points}/${a.total_points||'-'}` : (a.user_grade || (a.percent != null ? `${Math.round(a.percent)}%` : '-'))}
                  </div>
                ) : (
                  <div style={{color:'#999',fontSize:12}}>—</div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
      {loading && <div>Loading...</div>}
      {!loading && (
        <ul style={{listStyle:'none',padding:0,margin:0,display:'flex',flexDirection:'column',gap:8}}>
          {assignments.map(a => (
            <li key={a.id}>
              <button onClick={()=>onSelect(a)} style={{width:'100%',textAlign:'left',padding:8,borderRadius:6,background: selectedAssignment?.id===a.id ? '#eef' : '#fafafa',border:'1px solid #eee',display:'flex',justifyContent:'space-between',alignItems:'center'}}>
                <div style={{flex:1,textAlign:'left'}}>
                  <div style={{fontWeight:600}}>{a.title}</div>
                  <div style={{fontSize:12,color:'#666'}}>{(a.question_count||0)} questions</div>
                </div>
                <div style={{marginLeft:8,textAlign:'right'}}>
                  {a.user_grade != null || a.percent != null ? (
                    <div style={{fontWeight:700}}>{a.user_grade || `${Math.round(a.percent||0)}%`}</div>
                  ) : (
                    <div style={{color:'#999',fontSize:12}}>—</div>
                  )}
                </div>
              </button>
            </li>
          ))}
          {assignments.length===0 && <li style={{color:'#666'}}>No assignments</li>}
        </ul>
      )}
    </div>
  )
}
