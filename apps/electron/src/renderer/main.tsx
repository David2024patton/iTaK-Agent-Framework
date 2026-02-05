import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';
import { Dashboard } from './Dashboard';
import './styles.css';

// Initialize iTaK Dashboard
const targetNode = document.querySelector('#app-root');
if (targetNode === null) {
  throw new Error('Cannot mount: #app-root element missing');
}

createRoot(targetNode).render(
  <React.StrictMode>
    <Router>
      <Dashboard />
    </Router>
  </React.StrictMode>
);
