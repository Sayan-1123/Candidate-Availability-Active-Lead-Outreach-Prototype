import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import CandidateDetail from './components/CandidateDetail';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 flex">
        <div className="w-64 bg-white shadow-md">
          <div className="p-4 border-b">
            <h1 className="text-xl font-bold text-gray-800">RecruitAI</h1>
          </div>
          <nav className="p-4">
            <ul className="space-y-2">
              <li>
                <a href="/" className="block p-2 text-blue-600 bg-blue-50 rounded font-medium">Dashboard</a>
              </li>
              <li>
                <a href="#" className="block p-2 text-gray-600 hover:bg-gray-50 rounded">Candidates</a>
              </li>
            </ul>
          </nav>
        </div>
        <div className="flex-1 p-8 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/candidate/:id" element={<CandidateDetail />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
