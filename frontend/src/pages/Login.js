import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth } from '../api';
import './Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await auth.login({ username, password });
      localStorage.setItem('token', response.data.access_token);
      navigate('/admin');
    } catch (error) {
      alert('Invalid credentials');
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>Admin Login</h1>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn-login">
            Login
          </button>
        </form>
        <button onClick={() => navigate('/')} className="btn-back-login">
          Back to Home
        </button>
      </div>
    </div>
  );
}

export default Login;
