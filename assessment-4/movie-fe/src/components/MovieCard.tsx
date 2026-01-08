import type { Movie } from '../types/movie';
import './MovieCard.css';

interface MovieCardProps {
  movie: Movie;
}

export const MovieCard = ({ movie }: MovieCardProps) => {
  return (
    <div className="movie-card">
      <div className="movie-poster-wrapper">
        {movie.poster_url ? (
          <img
            src={movie.poster_url}
            alt={movie.movie_name}
            className="movie-poster"
            loading="lazy"
          />
        ) : (
          <div className="movie-poster-placeholder">
            <span>No Image</span>
          </div>
        )}
        <div className="movie-rating">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
          </svg>
          {movie.rating.toFixed(1)}
        </div>
      </div>
      <div className="movie-info">
        <h3 className="movie-title">{movie.movie_name}</h3>
        <p className="movie-original-title">{movie.original_title}</p>
        <div className="movie-meta">
          <span className="movie-year">{movie.year || 'N/A'}</span>
          {movie.runtime && (
            <>
              <span className="movie-meta-separator">•</span>
              <span className="movie-runtime">{movie.runtime}</span>
            </>
          )}
        </div>
        <p className="movie-overview">{movie.overview}</p>
      </div>
    </div>
  );
};
