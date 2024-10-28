import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(''); // Reset error before each attempt

    try {
      // Authenticate and get access token
      const response = await axios.post('http://localhost:8000/auth/jwt/create/', {
        email,
        password,
      });
      const { access } = response.data;

      // Store token in localStorage
      localStorage.setItem('access_token', access);

      // Fetch user details to check for superuser status
      const userResponse = await axios.get('http://localhost:8000/auth/users/', {
        headers: {
          Authorization: `JWT ${access}`,
        },
      });

      // Redirect based on superuser status
      if (userResponse.data.is_superuser) {
        navigate('/admin');
      } else {
        navigate('/home');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('Invalid email or password. Please try again.');
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
        {error && <div className="alert alert-danger">{error}</div>}
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