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
import './App.css';

function MovieBrowser() {
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

  return (
    <Layout>
      <div className="app-container">
        <h2>Browse Movies</h2>
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
          {/* Public movie browsing route */}
          <Route path="/" element={<MovieBrowser />} />

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

          {/* Redirect unknown routes to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
