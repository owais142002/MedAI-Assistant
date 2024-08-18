import React, { useState } from 'react';
import api from './api';

const SignUp = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSignUp = async () => {
    try {
      const response = await api.post('/medbot/signup/', { username, password });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || 'An error occurred');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h2 className="text-2xl mb-4">Sign Up</h2>
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
        onClick={handleSignUp}
        className="px-4 py-2 bg-blue-500 text-white rounded-md w-64"
      >
        Sign Up
      </button>
      {message && <p className="mt-4">{message}</p>}
    </div>
  );
};

export default SignUp;