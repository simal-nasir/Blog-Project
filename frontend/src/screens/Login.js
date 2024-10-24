import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
        const response = await axios.post('http://localhost:8000/auth/jwt/create/', {
            email,
            password,
        });
        const { access } = response.data;
        localStorage.setItem('access_token', access);
        navigate('/home'); 
        // Redirect or do something after login
    } catch (error) {
        console.error('Login error:', error);
        // Handle error (e.g., show a message to the user)
    }
};

  return (
    <div className="container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email</label>
          <input
            type="email"
            className="form-control"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Login</button>
      </form>

      {/* Sign Up link */}
      <p className="mt-3">
        Don't have an account?{' '}
        <button className="btn btn-link" onClick={() => navigate('/register')}>
          Sign Up
        </button>
      </p>
    </div>
  );
};

export default Login;