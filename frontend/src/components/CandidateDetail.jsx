import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getCandidate, getTimeline, sendOutreach, simulateReply, scheduleInterview } from '../services/api';

const CandidateDetail = () => {
  const { id } = useParams();
  const [candidate, setCandidate] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [replyText, setReplyText] = useState('');
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    try {
      const c = await getCandidate(id);
      const t = await getTimeline(id);
      setCandidate(c);
      setTimeline(t);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, [id]);

  const handleOutreach = async () => {
    setLoading(true);
    await sendOutreach(id);
    await loadData();
    setLoading(false);
  };

  const handleReply = async () => {
    if (!replyText) return;
    setLoading(true);
    await simulateReply(id, replyText);
    setReplyText('');
    await loadData();
    setLoading(false);
  };

  const handleSchedule = async () => {
    setLoading(true);
    await scheduleInterview(id);
    await loadData();
    setLoading(false);
  };

  if (!candidate) return <div>Loading...</div>;

  return (
    <div className="max-w-5xl mx-auto flex gap-6">
      <div className="w-2/3">
        <Link to="/" className="text-blue-600 mb-4 inline-block">&larr; Back to Dashboard</Link>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="text-2xl font-bold text-gray-800">{candidate.name}</h2>
              <p className="text-gray-600">{candidate.role} at {candidate.current_company}</p>
            </div>
            <span className="px-3 py-1 rounded-full text-sm font-semibold bg-blue-100 text-blue-800">
              {candidate.status}
            </span>
          </div>
          
          <div className="grid grid-cols-2 gap-4 mt-6">
            <div>
              <p className="text-sm text-gray-500">Email</p>
              <p className="font-medium">{candidate.email}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Skills</p>
              <p className="font-medium">{candidate.skills}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-bold mb-4">Actions</h3>
          
          {candidate.status === 'READY_FOR_OUTREACH' && (
            <button 
              onClick={handleOutreach}
              disabled={loading}
              className="bg-blue-600 text-white px-4 py-2 rounded font-medium hover:bg-blue-700 disabled:opacity-50"
            >
              Start Outreach
            </button>
          )}

          {candidate.status === 'NUDGE_SENT' && (
            <div className="mt-4 border-t pt-4">
              <h4 className="font-medium mb-2">Simulate Candidate Reply</h4>
              <textarea 
                className="w-full border rounded p-2 mb-2"
                rows="3"
                value={replyText}
                onChange={e => setReplyText(e.target.value)}
                placeholder="e.g. Yes I am interested. I have 15 days notice and am free next Tuesday afternoon."
              />
              <button 
                onClick={handleReply}
                disabled={loading}
                className="bg-green-600 text-white px-4 py-2 rounded font-medium hover:bg-green-700 disabled:opacity-50"
              >
                Send Reply & Analyze
              </button>
            </div>
          )}
          
          {candidate.status === 'READY_TO_SCHEDULE' && (
            <button 
              onClick={handleSchedule}
              disabled={loading}
              className="bg-purple-600 text-white px-4 py-2 rounded font-medium hover:bg-purple-700 disabled:opacity-50"
            >
              Auto Schedule Interview
            </button>
          )}
        </div>
      </div>
      
      <div className="w-1/3">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 sticky top-4">
          <h3 className="text-lg font-bold mb-4">Activity Timeline</h3>
          <div className="space-y-4">
            {timeline.map((event, idx) => (
              <div key={idx} className="border-l-2 border-gray-200 pl-4 pb-2">
                <p className="text-xs text-gray-500">{new Date(event.created_at).toLocaleString()}</p>
                <p className="text-sm font-semibold text-gray-800">{event.action}</p>
                <p className="text-sm text-gray-600 mt-1">{event.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CandidateDetail;
