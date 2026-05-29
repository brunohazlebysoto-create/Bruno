import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

// Storage polyfill — must run before any React render
if (!window.storage) {
  window.storage = {
    get: async (key) => {
      const val = localStorage.getItem(key)
      return val ? { value: val } : null
    },
    set: async (key, value) => {
      localStorage.setItem(key, value)
    },
  }
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
