import { useState } from 'react';
import { Layout, SearchBar, MovieList, ErrorBoundary } from './components';
import { useMovies } from './hooks';
import './App.css';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const filters = { limit: 20 };

  const { data: movies, isLoading, error } = useMovies(filters);

  // Filter movies based on search term (client-side filtering)
  const filteredMovies = movies?.filter((movie) => {
    if (!searchTerm) return true;
    const lowerSearch = searchTerm.toLowerCase();
    return (
      movie.movie_name.toLowerCase().includes(lowerSearch) ||
      movie.original_title.toLowerCase().includes(lowerSearch) ||
      movie.genre.toLowerCase().includes(lowerSearch)
    );
  });

  const handleSearch = (term: string) => {
    setSearchTerm(term);
  };

  return (
    <ErrorBoundary>
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

          <MovieList
            movies={filteredMovies || []}
            isLoading={isLoading}
            error={error}
          />
        </div>
      </Layout>
    </ErrorBoundary>
  );
}

export default App;
