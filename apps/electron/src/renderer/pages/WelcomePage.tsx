import React from 'react';

export function WelcomePage() {
  return (
    <div>
      <div className="card">
        <h2 className="card-header">Welcome to iTaK Agent Framework</h2>
        <div>
          <p style={{ marginBottom: '1rem', color: 'var(--itak-text-secondary)' }}>
            iTaK (Intelligent Task Automation Kernel) is a powerful multi-agent automation framework
            with self-healing capabilities and a 10-layer architecture.
          </p>
          
          <h3 style={{ 
            fontSize: '1.1rem', 
            marginTop: '1.5rem', 
            marginBottom: '0.75rem',
            color: 'var(--itak-accent-bright)'
          }}>
            Key Features
          </h3>
          <ul style={{ 
            marginLeft: '1.5rem', 
            color: 'var(--itak-text-secondary)',
            lineHeight: '1.8'
          }}>
            <li>🔧 Self-Healing - Automatically detects and recovers from failures</li>
            <li>🧠 Persistent Memory - Remembers past solutions via ChromaDB</li>
            <li>🐳 Safe Execution - Runs untrusted code in Docker sandboxes</li>
            <li>🌐 Remote Access - Access your local AI from anywhere</li>
            <li>🏠 Local-First - Optimized for Ollama and local LLMs</li>
          </ul>
          
          <h3 style={{ 
            fontSize: '1.1rem', 
            marginTop: '1.5rem', 
            marginBottom: '0.75rem',
            color: 'var(--itak-accent-bright)'
          }}>
            Getting Started
          </h3>
          <p style={{ color: 'var(--itak-text-secondary)', marginBottom: '0.5rem' }}>
            Use the navigation menu to:
          </p>
          <ul style={{ 
            marginLeft: '1.5rem', 
            color: 'var(--itak-text-secondary)',
            lineHeight: '1.8'
          }}>
            <li><strong>Status</strong> - View the current state of your iTaK agent</li>
            <li><strong>Logs</strong> - Monitor real-time output and activity</li>
            <li><strong>Controls</strong> - Start, stop, and manage your agent</li>
          </ul>
        </div>
      </div>
      
      <div className="card">
        <h2 className="card-header">Quick Actions</h2>
        <div className="flex gap-md">
          <button className="btn btn-primary">
            📚 View Documentation
          </button>
          <button className="btn btn-primary">
            🚀 Launch Agent
          </button>
          <button className="btn btn-primary">
            ⚙️ Configure Settings
          </button>
        </div>
      </div>
    </div>
  );
}
