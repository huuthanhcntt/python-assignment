import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import {
  Layout,
  SearchBar,
  FilterBar,
  MovieList,
  ErrorBoundary,
  AdminDashboard,
  ProtectedRoute,
  LoginRedirect
} from './components';
import { useMovies } from './hooks';
import { useMovieStore } from './store';
import { TenantProvider, useTenant } from './contexts/TenantContext';
import './App.css';

function MovieBrowser() {
  // Get current tenant from context
  const { tenant } = useTenant();

  // Get state and actions from Zustand store
  const searchTerm = useMovieStore((state) => state.searchTerm);
  const filters = useMovieStore((state) => state.filters);
  const setSearchTerm = useMovieStore((state) => state.setSearchTerm);

  // Pass search term to API - server-side filtering
  const { data: movies, isLoading, error } = useMovies({
    ...filters,
    search: searchTerm || undefined,
  });

  const handleSearch = (term: string) => {
    setSearchTerm(term);
  };

  // Format tenant name: replace underscores with spaces and capitalize each word
  const formattedTenant = tenant
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');

  return (
    <Layout>
      <div className="app-container">
        <h2>Browse Movies - {formattedTenant}</h2>
        <p className="app-subtitle">
          Search and explore our collection of movies
        </p>

        <SearchBar
          onSearch={handleSearch}
          placeholder="Search by title, original title, or genre..."
          debounceDelay={300}
        />

        <FilterBar />

        <MovieList
          movies={movies || []}
          isLoading={isLoading}
          error={error}
        />
      </div>
    </Layout>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Routes>
          {/* Redirect root to default tenant */}
          <Route path="/" element={<Navigate to="/trending" replace />} />

          {/* Tenant-based movie browsing route */}
          <Route
            path="/:tenant"
            element={
              <TenantProvider>
                <MovieBrowser />
              </TenantProvider>
            }
          />

          {/* Admin routes */}
          <Route path="/admin/login" element={<LoginRedirect />} />
          <Route
            path="/admin/dashboard"
            element={
              <ProtectedRoute>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />

          {/* Redirect /admin and /admin/* to dashboard */}
          <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
          <Route path="/admin/*" element={<Navigate to="/admin/dashboard" replace />} />

          {/* Redirect unknown routes to trending */}
          <Route path="*" element={<Navigate to="/trending" replace />} />
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
