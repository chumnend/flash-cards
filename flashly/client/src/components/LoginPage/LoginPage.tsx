import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import * as api from '../../helpers/api';
import { useAuthContext } from '../../helpers/context';

import './LoginPage.css';

const LoginPage = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [formData, setFormData] = useState<{[key: string]: string}>({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<{[key: string]: string}>({});
  const { handleLogin } = useAuthContext();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const {name, value} = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  }

  const validateForm = (): boolean => {
    const newErrors: {[key: string]: string} = {};

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    }

    if (!formData.password.trim()) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      const data = await api.login(formData.email, formData.password);

      if (data.user && data.token) {
        handleLogin(data.user.id, data.user.username, data.user.email, data.token);
        navigate("/feed");
      } else {
        throw new Error('Registration succeeded but user data is missing.');
      }

      setFormData({
        email: '',
        password: '',
      });
    } catch (error) {
      console.error('Login failed:', error);
      const errorMessage = error instanceof Error ? error.message : 'Registration failed. Please try again.';
      setErrors(prev => ({
        ...prev,
        'form': errorMessage,
      }));
    } finally {
      setIsLoading(false);
    }
  }


  return (
    <div className="login-page">
      <div className='login-container'>
        <h1>Login</h1>
        <p>Please log in to access your flashcards.</p>

        <form className='login-form' onSubmit={handleSubmit}>
          {errors.form && (
            <div className='form-error'>
              <span className="error-message">{errors.form}</span>
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'error' : ''}
              placeholder="Enter your email address"
            />
            {errors.email && <span className="error-message">{errors.email}</span>}
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className={errors.password ? 'error' : ''}
              placeholder="Create a password"
            />
            {errors.password && <span className="error-message">{errors.password}</span>}
          </div>

          <button 
            type="submit" 
            className="submit-button"
            disabled={isLoading}
          >
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className='register-link'>
          <p>Don't have an account? <Link to="/register">Register here</Link></p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;


