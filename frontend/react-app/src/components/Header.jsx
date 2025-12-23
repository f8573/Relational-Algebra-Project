import React from 'react'

export default function Header(){
  return (
    <header className="ra-header" style={{padding:20,background:'linear-gradient(45deg,#510C76,#8348AD)',color:'#fff',borderRadius:8}}>
      <h1 style={{margin:0,fontWeight:300}}>Relational Algebra Calculator</h1>
      <p style={{margin:0,opacity:0.9}}>Create relational algebra queries to be evaluated</p>
    </header>
  )
}
