import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AdminDashboard from './AdminDashboard'
import api from '../../lib/api'

export default function AdminPage(){
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [authorized, setAuthorized] = useState(false)

  useEffect(()=>{
    let mounted = true
    const check = async ()=>{
      try{
        const res = await api.getUser()
        if (!mounted) return
        if (res.ok && res.data && res.data.user && res.data.user.is_platform_admin){
          setAuthorized(true)
        } else {
          alert('Admin access required')
          navigate('/')
        }
      }catch(e){
        console.error('Auth check failed', e)
        navigate('/')
      }finally{
        if (mounted) setLoading(false)
      }
    }
    check()
    return ()=>{ mounted = false }
  },[navigate])

  if (loading) return <div>Loading...</div>
  if (!authorized) return null

  return (
    <div className="page-root">
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:12}}>
        <h1 style={{margin:0}}>Administrator Dashboard</h1>
        <div>
          <button onClick={()=>navigate('/')} style={{padding:'8px 10px',borderRadius:6}}>Back to app</button>
        </div>
      </div>
      <AdminDashboard onClose={()=>navigate('/')} fullPage={true} />
    </div>
  )
}
