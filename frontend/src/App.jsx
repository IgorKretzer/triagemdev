import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { BarChart3, Home, Moon, Sun, Brain } from 'lucide-react'
import HomePage from './pages/HomePage'
import './styles/index.css'

function App() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'dark';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <Router>
      <div className="app">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <h1 className="header-title">IA Triagem Sponte</h1>
            <nav className="header-nav">
              <Link to="/" className="nav-link">
                <Brain size={20} />
                Triagem
              </Link>
              <button onClick={toggleTheme} className="theme-toggle" title={`Mudar para modo ${theme === 'dark' ? 'claro' : 'escuro'}`}>
                {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
              </button>
            </nav>
          </div>
        </header>

        {/* Main Content */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
