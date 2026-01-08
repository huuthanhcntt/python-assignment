import type { Movie } from '../types/movie';
import { MovieCard } from './MovieCard';
import './MovieList.css';

interface MovieListProps {
  movies: Movie[];
  isLoading?: boolean;
  error?: Error | null;
}

export const MovieList = ({ movies, isLoading, error }: MovieListProps) => {
  if (isLoading) {
    return (
      <div className="movie-list-state">
        <div className="loading-spinner"></div>
        <p>Loading movies...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="movie-list-state error">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <h3>Error Loading Movies</h3>
        <p>{error.message}</p>
      </div>
    );
  }

  if (!movies || movies.length === 0) {
    return (
      <div className="movie-list-state">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <rect x="2" y="7" width="20" height="15" rx="2" ry="2" />
          <polyline points="17 2 12 7 7 2" />
        </svg>
        <h3>No Movies Found</h3>
        <p>Try adjusting your search or filters</p>
      </div>
    );
  }

  return (
    <div className="movie-list">
      {movies.map((movie) => (
        <MovieCard key={movie.tmdb_id} movie={movie} />
      ))}
    </div>
  );
};
