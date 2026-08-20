import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function CreateStartup() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [inviteLoading, setInviteLoading] = useState(false);
  const [startupId, setStartupId] = useState(null);
  
  // Startup Data
  const [formData, setFormData] = useState({
    name: '',
    industry: '',
    problem_statement: '',
    solution: '',
    target_customers: '',
    business_model: '',
    funding_requirement: '',
    market_size: '',
    competition: '',
  });
  
  // Invitation Data
  const [inviteEmail, setInviteEmail] = useState('');
  
  const [pitchDeck, setPitchDeck] = useState(null);
  const [pitchVideo, setPitchVideo] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const token = localStorage.getItem('token');
    if (!token) return navigate('/login');

    try {
      const payload = {
        name: formData.name,
        industry: formData.industry,
        problem_statement: formData.problem_statement,
        solution: formData.solution,
        target_customers: formData.target_customers,
        business_model: formData.business_model,
        competition: formData.competition,
        funding_requirement: parseFloat(formData.funding_requirement) || 0,
        market_size: parseFloat(formData.market_size) || 0,
      };

      const startupRes = await axios.post('http://localhost:8000/api/startups/', 
        payload,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      const id = startupRes.data.id;
      setStartupId(id); // Save ID so we can invite people now

      if (pitchDeck) {
        const deckForm = new FormData();
        deckForm.append('file', pitchDeck);
        await axios.post(`http://localhost:8000/api/startups/${id}/upload-pitch-deck`, deckForm, {
          headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
        });
      }

      if (pitchVideo) {
        const videoForm = new FormData();
        videoForm.append('file', pitchVideo);
        await axios.post(`http://localhost:8000/api/startups/${id}/upload-pitch-video`, videoForm, {
          headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
        });
      }

      alert('Startup created successfully! You can now invite co-founders.');
    } catch (err) {
      console.error(err);
      alert('Failed to create startup: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

    const handleInvite = async (e) => {
    e.preventDefault();
    if (!startupId) return alert('Please create the startup first!');
    if (!inviteEmail) return alert('Please enter an email address.');

    setInviteLoading(true);
    const token = localStorage.getItem('token'); // Get the token first
    try {
      await axios.post(`http://localhost:8000/api/invitations/${startupId}`, 
        { invitee_email: inviteEmail },
        { 
          headers: { 
            Authorization: `Bearer ${token}` // 👈 THIS WAS MISSING IN THE PREVIOUS CODE
          } 
        }
      );
      alert(`Invitation sent to ${inviteEmail}!`);
      setInviteEmail('');
    } catch (err) {
      alert('Failed to send invite: ' + (err.response?.data?.detail || err.message));
    } finally {
      setInviteLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 p-8 flex justify-center">
      <div className="w-full max-w-4xl bg-white rounded-3xl shadow-2xl p-10">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-blue-500 rounded-lg flex items-center justify-center text-white font-bold">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-800">Launch Your Startup</h1>
        </div>

        {/* Main Startup Form */}
        <form onSubmit={handleSubmit} className="space-y-6 border-b border-gray-200 pb-8 mb-8">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Startup Name *</label>
              <input type="text" name="name" value={formData.name} onChange={handleChange} required
                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Industry *</label>
              <input type="text" name="industry" value={formData.industry} onChange={handleChange} required
                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none" />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Problem Statement *</label>
            <textarea name="problem_statement" rows="3" value={formData.problem_statement} onChange={handleChange} required
              className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Solution *</label>
            <textarea name="solution" rows="3" value={formData.solution} onChange={handleChange} required
              className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none" />
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Target Customers</label>
              <input type="text" name="target_customers" value={formData.target_customers} onChange={handleChange}
                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Business Model</label>
              <input type="text" name="business_model" value={formData.business_model} onChange={handleChange}
                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Funding Requirement ($)</label>
              <input type="number" name="funding_requirement" value={formData.funding_requirement} onChange={handleChange}
                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Market Size ($)</label>
              <input type="number" name="market_size" value={formData.market_size} onChange={handleChange}
                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none" />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Competition</label>
            <textarea name="competition" rows="2" value={formData.competition} onChange={handleChange}
              className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none" />
          </div>

          <div className="grid grid-cols-2 gap-6 pt-4 border-t border-gray-100">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Pitch Deck (PDF)</label>
              <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:bg-gray-50 transition cursor-pointer">
                <input type="file" accept=".pdf" onChange={(e) => setPitchDeck(e.target.files[0])} className="hidden" id="deckUpload" />
                <label htmlFor="deckUpload" className="cursor-pointer">
                  <div className="text-gray-400 text-4xl mb-2">📄</div>
                  <div className="text-sm text-gray-600">{pitchDeck ? pitchDeck.name : 'Click to upload PDF'}</div>
                </label>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Pitch Video</label>
              <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:bg-gray-50 transition cursor-pointer">
                <input type="file" accept="video/*" onChange={(e) => setPitchVideo(e.target.files[0])} className="hidden" id="videoUpload" />
                <label htmlFor="videoUpload" className="cursor-pointer">
                  <div className="text-gray-400 text-4xl mb-2">🎥</div>
                  <div className="text-sm text-gray-600">{pitchVideo ? pitchVideo.name : 'Click to upload Video'}</div>
                </label>
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4">
            <button 
              type="submit" 
              disabled={loading}
              className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-500 text-white rounded-xl font-semibold shadow-lg hover:shadow-purple-500/50 transition-all disabled:opacity-50"
            >
              {loading ? 'Creating...' : 'Create Startup →'}
            </button>
          </div>
        </form>

        {/* Invitation Section (Shown after creation) */}
        {startupId && (
          <div className="bg-purple-50 border border-purple-200 rounded-xl p-6">
            <h3 className="text-lg font-bold text-purple-800 mb-2">📨 Invite a Co-Founder</h3>
            <p className="text-sm text-purple-600 mb-4">Send an email invite to your partner so they can view and review this startup.</p>
            <form onSubmit={handleInvite} className="flex gap-4">
              <input 
                type="email" 
                value={inviteEmail} 
                onChange={(e) => setInviteEmail(e.target.value)}
                placeholder="cofounder@example.com"
                className="flex-1 px-4 py-3 bg-white border border-purple-300 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none"
                required
              />
              <button 
                type="submit" 
                disabled={inviteLoading}
                className="px-6 py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition disabled:opacity-50"
              >
                {inviteLoading ? 'Sending...' : 'Send Invite'}
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}