import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

export default function StartupDetails() {
  const { id } = useParams();
  const [startup, setStartup] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return navigate('/login');

    axios.get(`http://localhost:8000/api/startups/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setStartup(res.data))
      .catch(err => console.error(err));
  }, [id, navigate]);

  if (!startup) return <div className="p-8 text-gray-500">Loading...</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 p-8 flex justify-center">
      <div className="w-full max-w-4xl bg-white rounded-3xl shadow-2xl p-10">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800">{startup.name}</h1>
          <Link to="/dashboard" className="text-purple-600 font-medium hover:underline">← Back</Link>
        </div>
        <div className="grid grid-cols-2 gap-6">
          <div><span className="font-bold text-gray-600">Industry:</span> {startup.industry}</div>
          <div><span className="font-bold text-gray-600">Business Model:</span> {startup.business_model}</div>
        </div>
        <div className="mt-4"><span className="font-bold text-gray-600">Problem:</span> {startup.problem_statement}</div>
        <div className="mt-2"><span className="font-bold text-gray-600">Solution:</span> {startup.solution}</div>
        <div className="mt-4"><span className="font-bold text-gray-600">Funding:</span> ${startup.funding_requirement}</div>
      </div>
    </div>
  );
}