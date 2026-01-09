import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AxiosError } from 'axios';
import { useAuthStore } from '../../store/authStore';
import { moviesApi } from '../../api/movies';
import './AdminDashboard.css';

export function AdminDashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const [selectedTenant, setSelectedTenant] = useState('trending');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      // Validate file type
      if (!selectedFile.name.endsWith('.csv')) {
        setMessage({ type: 'error', text: 'Please select a CSV file' });
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setMessage(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedTenant) {
      setMessage({ type: 'error', text: 'Please select a tenant' });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const result = await moviesApi.reloadMovies(selectedTenant, file || undefined);
      setMessage({
        type: 'success',
        text: `Successfully loaded ${result.loaded} movies for tenant "${result.tenant}"`,
      });
      setFile(null);
      // Reset file input
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (err) {
      if (err instanceof AxiosError) {
        setMessage({
          type: 'error',
          text: err.response?.data?.detail || 'Failed to upload movies',
        });
      } else {
        setMessage({
          type: 'error',
          text: 'Failed to upload movies',
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
  };

  return (
    <div className="admin-dashboard">
      <header className="admin-header">
        <div className="header-content">
          <h1>Admin Dashboard</h1>
          <div className="user-info">
            <span>Welcome, {user?.username}</span>
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="admin-main">
        <div className="dashboard-card">
          <h2>Movie Management</h2>
          <p className="card-subtitle">Upload or reload movies from CSV files</p>

          {message && (
            <div className={`message ${message.type}`}>
              {message.text}
            </div>
          )}

          <div className="upload-section">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="tenant">Select Tenant</label>
                <select
                  id="tenant"
                  value={selectedTenant}
                  onChange={(e) => setSelectedTenant(e.target.value)}
                  className="tenant-select"
                >
                  <option value="movies">Movies</option>
                  <option value="tv_serials">TV Serials</option>
                  <option value="trending">Trending</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="file-input">CSV File (Optional)</label>
                <input
                  id="file-input"
                  type="file"
                  accept=".csv"
                  onChange={handleFileChange}
                  className="file-input"
                />
                {file && (
                  <div className="file-info">
                    Selected: {file.name} ({(file.size / 1024).toFixed(2)} KB)
                  </div>
                )}
              </div>
            </div>

            <div className="upload-info">
              <p>
                <strong>Note:</strong> {file ?
                  'Upload a custom CSV file with movie data.' :
                  'Click upload to reload default data for the selected tenant.'}
              </p>
            </div>

            <button
              onClick={handleUpload}
              disabled={loading}
              className="upload-button"
            >
              {loading ? 'Uploading...' : file ? 'Upload CSV' : 'Reload Default Data'}
            </button>
          </div>

          <div className="action-buttons">
            <button
              onClick={() => navigate('/')}
              className="secondary-button"
            >
              View Movies Site
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
