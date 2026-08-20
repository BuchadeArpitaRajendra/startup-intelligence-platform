import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function Invitations() {
  const [invites, setInvites] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchInvites();
  }, []);

  const fetchInvites = async () => {
    const token = localStorage.getItem('token');
    if (!token) return navigate('/login');

    try {
      const res = await axios.get('http://localhost:8000/api/invitations/pending', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setInvites(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (token, action) => {
    const userToken = localStorage.getItem('token');
    try {
      await axios.post(`http://localhost:8000/api/invitations/${token}/${action}`, {}, {
        headers: { Authorization: `Bearer ${userToken}` }
      });
      alert(`Invitation ${action === 'accept' ? 'accepted' : 'rejected'} successfully!`);
      fetchInvites(); // Refresh the list
    } catch (err) {
      alert('Failed: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">📨 Co-Founder Invitations</h1>
        
        {loading ? (
          <p className="text-gray-500">Loading...</p>
        ) : invites.length === 0 ? (
          <div className="bg-white p-10 rounded-2xl shadow-lg text-center border border-gray-100">
            <p className="text-gray-500 text-lg">You have no pending invitations.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {invites.map((invite) => (
              <div key={invite.id} className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100 flex justify-between items-center">
                <div>
                  <h3 className="font-bold text-gray-800 text-lg">Startup #{invite.startup_id}</h3>
                  <p className="text-gray-500 text-sm">Invited by Founder ID: {invite.inviter_id}</p>
                  <p className="text-xs text-gray-400 mt-1">Expires: {new Date(invite.expires_at).toLocaleDateString()}</p>
                </div>
                <div className="flex gap-3">
                  <button 
                    onClick={() => handleAction(invite.token, 'accept')}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
                  >
                    Accept
                  </button>
                  <button 
                    onClick={() => handleAction(invite.token, 'reject')}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
                  >
                    Reject
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}