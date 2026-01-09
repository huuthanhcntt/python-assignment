import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AxiosError } from 'axios';
import { authApi } from '../../api/auth';
import { useAuthStore } from '../../store/authStore';
import './AdminLogin.css';

export function AdminLogin() {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);
  const setUser = useAuthStore((state) => state.setUser);

  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        // Login
        const tokenData = await authApi.login({
          username: formData.username,
          password: formData.password,
        });

        // Save token first (so the interceptor can use it for subsequent requests)
        login(tokenData.access_token);

        // Get user info (now the interceptor will include the token)
        const user = await authApi.getMe();

        // Update user info in store
        setUser(user);

        // Redirect to admin dashboard
        navigate('/admin/dashboard');
      } else {
        // Register
        await authApi.register({
          username: formData.username,
          email: formData.email,
          password: formData.password,
        });

        // After registration, automatically login
        const tokenData = await authApi.login({
          username: formData.username,
          password: formData.password,
        });

        // Save token first
        login(tokenData.access_token);

        // Get user info
        const user = await authApi.getMe();

        // Update user info
        setUser(user);

        navigate('/admin/dashboard');
      }
    } catch (err) {
      if (err instanceof AxiosError) {
        setError(err.response?.data?.detail || 'Authentication failed');
      } else {
        setError('Authentication failed');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-login-container">
      <div className="admin-login-card">
        <h2>{isLogin ? 'Admin Login' : 'Admin Register'}</h2>
        <p className="admin-login-subtitle">
          {isLogin ? 'Sign in to manage movies' : 'Create an admin account'}
        </p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              required
              placeholder="Enter your username"
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
                placeholder="Enter your email"
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
              placeholder="Enter your password"
            />
          </div>

          <button type="submit" disabled={loading} className="submit-button">
            {loading ? 'Processing...' : isLogin ? 'Login' : 'Register'}
          </button>
        </form>

        <div className="toggle-form">
          <button onClick={() => {
            setIsLogin(!isLogin);
            setError('');
          }}>
            {isLogin ? "Don't have an account? Register" : 'Already have an account? Login'}
          </button>
        </div>
      </div>
    </div>
  );
}
