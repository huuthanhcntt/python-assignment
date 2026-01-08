import { Layout, SearchBar, FilterBar, MovieList, ErrorBoundary } from './components';
import { useMovies } from './hooks';
import { useMovieStore } from './store';
import './App.css';

function App() {
  // Get state and actions from Zustand store
  const searchTerm = useMovieStore((state) => state.searchTerm);
  const filters = useMovieStore((state) => state.filters);
  const setSearchTerm = useMovieStore((state) => state.setSearchTerm);

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

          <FilterBar />

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
