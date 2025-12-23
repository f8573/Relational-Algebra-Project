import React, { useState, useEffect } from 'react'
import api from '../lib/api'

export default function CourseSelector({ onCourseSelect, userRole, onUnauthorized }) {
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setLoading(true)
        const res = await api.getCourses()
        if (res.unauthorized || res.status === 401) {
          // Session invalid — notify parent to clear session
          if (typeof onUnauthorized === 'function') {
            onUnauthorized()
          } else {
            localStorage.removeItem('authToken')
            localStorage.removeItem('user')
            window.location.reload()
          }
          return
        }
        if (res.ok && res.data && res.data.courses) {
          setCourses(res.data.courses)
          if (res.data.courses.length > 0) {
            onCourseSelect(res.data.courses[0])
          }
        } else {
          setError('Failed to load courses')
        }
      } catch (e) {
        setError('Error: ' + e.message)
      } finally {
        setLoading(false)
      }
    }

    fetchCourses()
  // run only on mount; `onCourseSelect` is called conditionally inside
  // and may be unstable across renders from parent props.
  }, [])

  if (loading) return <div className="course-selector">Loading courses...</div>
  if (error) return <div className="course-selector error">{error}</div>

  return (
    <div className="course-selector">
      <label htmlFor="course-select">Course:</label>
      <select 
        id="course-select"
        onChange={(e) => {
          const course = courses.find(c => c.id === parseInt(e.target.value))
          if (course) onCourseSelect(course)
        }}
      >
        {courses.map(course => (
          <option key={course.id} value={course.id}>
            {course.title} ({course.role})
          </option>
        ))}
      </select>
    </div>
  )
}
