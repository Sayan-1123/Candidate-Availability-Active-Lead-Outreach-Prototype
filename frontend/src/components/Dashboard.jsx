import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getDashboardStats, getCandidates } from '../services/api';
import { Users, Send, MessageSquare, CheckCircle, Clock, Calendar } from 'lucide-react';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [candidates, setCandidates] = useState([]);

  const fetchData = async () => {
    try {
      const statsData = await getDashboardStats();
      const candidatesData = await getCandidates();
      setStats(statsData);
      setCandidates(candidatesData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const getStatusBadge = (status) => {
    const colors = {
      READY_FOR_OUTREACH: 'bg-gray-100 text-gray-800',
      NUDGE_SENT: 'bg-blue-100 text-blue-800',
      REPLY_RECEIVED: 'bg-yellow-100 text-yellow-800',
      READY_TO_SCHEDULE: 'bg-green-100 text-green-800',
      INTERVIEW_SCHEDULED: 'bg-purple-100 text-purple-800',
      FOLLOW_UP_REQUIRED: 'bg-orange-100 text-orange-800',
      CLOSED: 'bg-red-100 text-red-800',
    };
    return <span className={`px-2 py-1 rounded-full text-xs font-semibold ${colors[status] || 'bg-gray-100'}`}>{status.replace(/_/g, ' ')}</span>;
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Overview</h2>
      
      {stats && (
        <div className="grid grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 flex items-center">
            <div className="p-3 rounded-full bg-blue-100 text-blue-600 mr-4"><Users size={24} /></div>
            <div>
              <p className="text-sm text-gray-500 font-medium">Total Candidates</p>
              <p className="text-2xl font-bold text-gray-800">{stats.total}</p>
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 flex items-center">
            <div className="p-3 rounded-full bg-indigo-100 text-indigo-600 mr-4"><Send size={24} /></div>
            <div>
              <p className="text-sm text-gray-500 font-medium">Nudges Sent</p>
              <p className="text-2xl font-bold text-gray-800">{stats.nudges_sent}</p>
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 flex items-center">
            <div className="p-3 rounded-full bg-green-100 text-green-600 mr-4"><Calendar size={24} /></div>
            <div>
              <p className="text-sm text-gray-500 font-medium">Interviews Scheduled</p>
              <p className="text-2xl font-bold text-gray-800">{stats.interviews_scheduled}</p>
            </div>
          </div>
        </div>
      )}

      <h3 className="text-xl font-bold mb-4 text-gray-800">Candidates</h3>
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-200">
              <th className="p-4 text-sm font-semibold text-gray-600">Candidate</th>
              <th className="p-4 text-sm font-semibold text-gray-600">Role</th>
              <th className="p-4 text-sm font-semibold text-gray-600">Score</th>
              <th className="p-4 text-sm font-semibold text-gray-600">Status</th>
              <th className="p-4 text-sm font-semibold text-gray-600">Action</th>
            </tr>
          </thead>
          <tbody>
            {candidates.map(candidate => (
              <tr key={candidate.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="p-4">
                  <div className="font-medium text-gray-800">{candidate.name}</div>
                  <div className="text-sm text-gray-500">{candidate.current_company}</div>
                </td>
                <td className="p-4 text-sm text-gray-600">{candidate.role}</td>
                <td className="p-4 text-sm text-gray-600">{candidate.resume_score}</td>
                <td className="p-4">{getStatusBadge(candidate.status)}</td>
                <td className="p-4">
                  <Link to={`/candidate/${candidate.id}`} className="text-blue-600 hover:text-blue-800 text-sm font-medium">View Details</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
