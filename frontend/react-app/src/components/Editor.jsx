import React, { useRef } from 'react'
import MathEditor from './MathEditor'

export default function Editor({ onRun, course, registerSetContent, onSubmit }){
  return (
    <div>
      <div style={{marginTop:12}}>
        <MathEditor onRun={onRun} onSubmit={onSubmit} course={course} registerSetContent={registerSetContent} />
      </div>
    </div>
  )
}
