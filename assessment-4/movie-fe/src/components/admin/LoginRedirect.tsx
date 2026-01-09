import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { AdminLogin } from './AdminLogin';

export function LoginRedirect() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  // If already authenticated, redirect to dashboard
  if (isAuthenticated) {
    return <Navigate to="/admin/dashboard" replace />;
  }

  // Otherwise, show login page
  return <AdminLogin />;
}
