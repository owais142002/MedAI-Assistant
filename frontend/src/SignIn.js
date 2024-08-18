import React, { useState } from 'react';
import api from './api';
import { useNavigate, Link } from 'react-router-dom';
import Loader from './Loader'; // Assuming you have a Loader component

const SignIn = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignIn = async () => {
    if (!username || !password) {
      setMessage('Username and password are required');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/medbot/validate-user/', { username, password });
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user_id', response.data.user_id);
      navigate('/chat');
    } catch (error) {
      setMessage(error.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h2 className="text-2xl mb-4">Sign In</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="px-4 py-2 mb-2 border rounded-md w-64"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="px-4 py-2 mb-2 border rounded-md w-64"
      />
      <button
        onClick={handleSignIn}
        className="px-4 py-2 bg-blue-500 text-white rounded-md w-64"
        disabled={loading}
      >
        {loading ? <Loader /> : 'Sign In'}
      </button>
      {message && <p className="mt-4">{message}</p>}
      <p className="mt-4">
        Don't have an account? <Link to="/signup" className="text-blue-500">Sign Up</Link>
      </p>
    </div>
  );
};

export default SignIn;