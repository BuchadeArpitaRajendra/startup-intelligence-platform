import { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

export default function Register() {
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'founder',
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    try {
      await axios.post('http://localhost:8000/api/auth/register', {
        full_name: formData.full_name,
        email: formData.email,
        password: formData.password,
        expertise: formData.role === 'founder' ? 'Startup Founder' : 'Co-founder',
        experience_years: 0,
      });
      alert('Account created! Please log in.');
      navigate('/login');
    } catch (err) {
      alert('Registration failed: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <div className="w-full max-w-5xl bg-white rounded-3xl shadow-2xl overflow-hidden flex flex-col md:flex-row">
        
        {/* Left Side: Image (Shrunken to 5/12 width) */}
        <div className="hidden md:flex w-5/12 bg-gradient-to-br from-blue-100 to-purple-100 p-8 items-center justify-center relative overflow-hidden">
          <div className="absolute top-10 left-10 w-32 h-32 bg-blue-300 rounded-full blur-3xl opacity-30"></div>
          <div className="absolute bottom-10 right-10 w-40 h-40 bg-purple-300 rounded-full blur-3xl opacity-30"></div>
          <img 
            src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=800&auto=format&fit=crop" 
            alt="Team Collaboration" 
            className="relative z-10 rounded-2xl shadow-2xl object-cover w-full h-full max-h-[500px]"
          />
        </div>

        {/* Right Side: Form (Expanded to 7/12 width) */}
        <div className="w-full md:w-7/12 p-10 flex flex-col justify-center">
          <div className="mb-6">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-blue-500 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
                </svg>
              </div>
              <span className="text-2xl font-bold text-gray-800">StartupIQ</span>
            </div>
            <h2 className="text-3xl font-bold text-gray-800">Create Your Account</h2>
            <p className="text-gray-500 mt-1">Join StartupIQ and validate your startup ideas</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                <div className="relative">
                  <span className="absolute left-3 top-3.5 text-gray-400">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                  </span>
                  <input
                    type="text"
                    name="full_name"
                    value={formData.full_name}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none text-gray-800 placeholder-gray-400"
                    placeholder="Your full name"
                    required
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                <div className="relative">
                  <span className="absolute left-3 top-3.5 text-gray-400">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                  </span>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none text-gray-800 placeholder-gray-400"
                    placeholder="you@example.com"
                    required
                  />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                <div className="relative">
                  <span className="absolute left-3 top-3.5 text-gray-400">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                    </svg>
                  </span>
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none text-gray-800 placeholder-gray-400"
                    placeholder="Create a strong password"
                    required
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
                <div className="relative">
                  <span className="absolute left-3 top-3.5 text-gray-400">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                    </svg>
                  </span>
                  <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none text-gray-800 placeholder-gray-400"
                    placeholder="Confirm your password"
                    required
                  />
                </div>
              </div>
            </div>

            {/* Role Selector */}
            <div className="pt-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">I am a</label>
              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, role: 'founder' })}
                  className={`flex-1 border-2 p-3 rounded-xl text-center transition-all duration-200 ${
                    formData.role === 'founder' 
                    ? 'border-purple-500 bg-purple-50 text-purple-700' 
                    : 'border-gray-200 bg-gray-50 text-gray-500 hover:bg-gray-100'
                  }`}
                >
                  <div className="flex justify-center mb-1">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                  </div>
                  <div className="font-medium text-sm mt-1">Founder</div>
                  <div className="text-[10px]">I have a startup idea</div>
                </button>
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, role: 'cofounder' })}
                  className={`flex-1 border-2 p-3 rounded-xl text-center transition-all duration-200 ${
                    formData.role === 'cofounder' 
                    ? 'border-purple-500 bg-purple-50 text-purple-700' 
                    : 'border-gray-200 bg-gray-50 text-gray-500 hover:bg-gray-100'
                  }`}
                >
                  <div className="flex justify-center mb-1">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                    </svg>
                  </div>
                  <div className="font-medium text-sm mt-1">Co-Founder</div>
                  <div className="text-[10px]">I want to join a startup</div>
                </button>
              </div>
            </div>

            <div className="pt-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">Startup Name (Optional)</label>
              <div className="relative">
                <span className="absolute left-3 top-3.5 text-gray-400">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                  </svg>
                </span>
                <input
                  type="text"
                  className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none text-gray-800 placeholder-gray-400"
                  placeholder="Enter your startup name"
                />
              </div>
            </div>

            <div className="flex items-center gap-2 text-sm text-gray-600 pt-1">
              <input type="checkbox" className="rounded text-purple-600 focus:ring-purple-500" required />
              <span>I agree to the <span className="text-purple-600 hover:underline cursor-pointer font-medium">Terms of Service</span> and <span className="text-purple-600 hover:underline cursor-pointer font-medium">Privacy Policy</span></span>
            </div>

            <button 
              type="submit" 
              className="w-full py-3 bg-gradient-to-r from-purple-600 to-blue-500 text-white rounded-xl font-semibold shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50 transition-all duration-300 flex items-center justify-center gap-2"
            >
              Create Account 
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
              </svg>
            </button>
          </form>

          <div className="mt-4 text-center text-sm">
            <span className="text-gray-600">Already have an account? </span>
            <Link to="/login" className="text-purple-600 hover:text-purple-700 font-semibold">
              Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}