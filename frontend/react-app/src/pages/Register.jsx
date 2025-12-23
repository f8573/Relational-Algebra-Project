import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api, { auth } from '../lib/api'

export default function Register(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e)=>{
    e.preventDefault()
    setError('')
    setLoading(true)
    try{
      const res = await auth.register({ email, password, name })
      if (!res.ok){
        setError(res.data?.message || 'Register failed')
        return
      }
      // Try logging in immediately
      const loginRes = await api.login(email, password)
      if (loginRes.ok && loginRes.data && loginRes.data.token){
        localStorage.setItem('authToken', loginRes.data.token)
        localStorage.setItem('user', JSON.stringify(loginRes.data.user))
        navigate('/')
      } else {
        // fallback to home
        navigate('/')
      }
    }catch(e){
      setError('Network error: '+e.message)
    }finally{ setLoading(false) }
  }

  return (
    <div style={{padding:24}}>
      <h2>Register</h2>
      {error && <div style={{color:'red'}}>{error}</div>}
      <form onSubmit={handleSubmit} style={{display:'flex',flexDirection:'column',gap:8,maxWidth:420}}>
        <label>Email</label>
        <input type="email" value={email} onChange={e=>setEmail(e.target.value)} required />
        <label>Name</label>
        <input value={name} onChange={e=>setName(e.target.value)} />
        <label>Password</label>
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} required />
        <div>
          <button type="submit" disabled={loading}>{loading? 'Registering...':'Register'}</button>
        </div>
      </form>
    </div>
  )
}
