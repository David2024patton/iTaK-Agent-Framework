import React from 'react';
import { Routes, Route, NavLink } from 'react-router-dom';
import { WelcomePage } from './pages/WelcomePage';
import { StatusPage } from './pages/StatusPage';
import { LogsPage } from './pages/LogsPage';
import { ControlsPage } from './pages/ControlsPage';

export function Dashboard() {
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1 className="dashboard-title">
          <span>🤖</span>
          <span>iTaK Agent Dashboard</span>
        </h1>
        <div className="flex items-center gap-md">
          <span className="status-badge running">
            <span className="status-indicator active"></span>
            Ready
          </span>
        </div>
      </header>
      
      <div className="dashboard-main">
        <nav className="sidebar-navigation">
          <NavLink to="/" end className="nav-link">
            <span>🏠</span>
            <span>Welcome</span>
          </NavLink>
          <NavLink to="/status" className="nav-link">
            <span>📊</span>
            <span>Status</span>
          </NavLink>
          <NavLink to="/logs" className="nav-link">
            <span>📝</span>
            <span>Logs</span>
          </NavLink>
          <NavLink to="/controls" className="nav-link">
            <span>🎮</span>
            <span>Controls</span>
          </NavLink>
        </nav>
        
        <main className="content-area">
          <Routes>
            <Route path="/" element={<WelcomePage />} />
            <Route path="/status" element={<StatusPage />} />
            <Route path="/logs" element={<LogsPage />} />
            <Route path="/controls" element={<ControlsPage />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}
