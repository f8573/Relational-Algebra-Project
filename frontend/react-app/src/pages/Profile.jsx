import React, { useEffect, useState } from 'react'
import api, { auth } from '../lib/api'

export default function Profile(){
  const [user, setUser] = useState(null)
  const [name, setName] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [msg, setMsg] = useState('')

  useEffect(()=>{
    const load = async ()=>{
      const res = await api.getUser()
      if (res.ok && res.data && res.data.user){
        setUser(res.data.user)
        setName(res.data.user.name || '')
      }
    }
    load()
  },[])

  const saveProfile = async ()=>{
    setLoading(true); setMsg('')
    try{
      const res = await auth.updateUser({ name })
      if (res.ok) setMsg('Profile saved')
      else setMsg('Save failed')
    }catch(e){ setMsg('Network error') }
    finally{ setLoading(false) }
  }

  const changePassword = async ()=>{
    if (!newPassword) return setMsg('Enter a new password')
    setLoading(true); setMsg('')
    try{
      const res = await auth.changePassword(newPassword)
      if (res.ok) setMsg('Password changed')
      else setMsg('Change failed')
    }catch(e){ setMsg('Network error') }
    finally{ setLoading(false); setNewPassword('') }
  }

  if (!user) return <div>Loading...</div>

  return (
    <div style={{padding:16}}>
      <h2>Profile</h2>
      <div style={{marginBottom:12}}>
        <label>Email</label>
        <div>{user.email}</div>
      </div>
      <div style={{marginBottom:12}}>
        <label>Name</label>
        <input value={name} onChange={e=>setName(e.target.value)} />
        <div style={{marginTop:8}}>
          <button onClick={saveProfile} disabled={loading}>Save</button>
        </div>
      </div>
      <div style={{marginTop:16}}>
        <h3>Change Password</h3>
        <input type="password" placeholder="New password" value={newPassword} onChange={e=>setNewPassword(e.target.value)} />
        <div style={{marginTop:8}}>
          <button onClick={changePassword} disabled={loading}>Change password</button>
        </div>
      </div>
      {msg && <div style={{marginTop:12,color:'#666'}}>{msg}</div>}
    </div>
  )
}
