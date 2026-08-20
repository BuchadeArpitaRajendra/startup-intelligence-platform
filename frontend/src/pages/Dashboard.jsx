import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [startups, setStartups] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    axios.get('http://localhost:8000/api/auth/me', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setUser(res.data)).catch(() => {
      localStorage.removeItem('token');
      navigate('/login');
    });

    axios.get('http://localhost:8000/api/startups', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setStartups(res.data));
  }, [navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">👋 Welcome, {user?.full_name || 'User'}!</h1>
          <Link to="/create-startup">
            <button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-500 text-white rounded-xl font-semibold shadow-lg hover:shadow-purple-500/50 transition-all">
              + Create New Startup
            </button>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {startups.length > 0 ? (
            startups.map((s) => (
              <div key={s.id} className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all border border-gray-100">
                <h3 className="text-xl font-bold text-gray-800">{s.name}</h3>
                <p className="text-purple-600 text-sm font-medium">{s.industry || 'General'}</p>
                <p className="text-gray-500 text-sm mt-2 line-clamp-2">{s.problem_statement || 'No description provided.'}</p>
                <div className="mt-4 flex justify-between items-center">
                  <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-semibold">{s.status || 'Active'}</span>
                  <button className="text-purple-600 text-sm font-medium hover:underline">View Details →</button>
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-full bg-white p-10 rounded-2xl shadow-lg text-center border border-gray-100">
              <p className="text-gray-500 text-lg">You haven't created a startup yet.</p>
              <Link to="/create-startup" className="text-purple-600 font-semibold hover:underline mt-2 inline-block">
                Start your first one now!
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}