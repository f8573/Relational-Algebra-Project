import React, { useState } from 'react'
import '../styles/login.css'

export default function Login({ onLoginSuccess }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [remember, setRemember] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, remember })
      })

      const data = await response.json()

      if (!response.ok) {
        setError(data.message || 'Login failed')
        return
      }

      // Login successful
      if (data.token && data.user) {
        // Persist token according to "remember" preference
        try {
          if (remember) {
            localStorage.setItem('authToken', data.token)
            localStorage.setItem('user', JSON.stringify(data.user))
          } else {
            sessionStorage.setItem('authToken', data.token)
            sessionStorage.setItem('user', JSON.stringify(data.user))
          }
        } catch (e) {
          // Fallback: always use localStorage if sessionStorage unavailable
          localStorage.setItem('authToken', data.token)
          localStorage.setItem('user', JSON.stringify(data.user))
        }
        // Debug: log token fingerprint (not full token) to help trace auth issues
        try { console.debug('Login success, token fingerprint:', (data.token || '').substring(0,8) + '...') } catch (e) {}
        onLoginSuccess(data.user, data.token)
      }
    } catch (err) {
      setError('Network error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Relational Algebra LMS</h1>
        <p className="subtitle">Sign in to your account</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoFocus
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',gap:8}}>
            <label style={{display:'flex',alignItems:'center',gap:8,fontSize:14}}>
              <input type="checkbox" checked={remember} onChange={(e)=>setRemember(e.target.checked)} disabled={loading} />
              Remember me for 30 days
            </label>
            <button type="submit" disabled={loading} className="login-button">
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </div>
        </form>

        <div style={{marginTop:12}}>
          <a href="/register">Create an account</a>
        </div>

        <div className="demo-credentials">
          <p>Demo credentials:</p>
          <ul>
            <li><strong>Student:</strong> student@university.edu / student-password-789</li>
            <li><strong>Instructor:</strong> instructor@university.edu / instructor-password-456</li>
            <li><strong>Admin:</strong> admin@university.edu / admin-password-123</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
