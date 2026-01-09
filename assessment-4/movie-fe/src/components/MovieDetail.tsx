import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { moviesApi } from '../api/movies';
import { useTenant } from '../contexts/TenantContext';
import { Layout } from './Layout';
import './MovieDetail.css';

export const MovieDetail = () => {
  const { tenant: urlTenant, tmdbId } = useParams<{ tenant: string; tmdbId: string }>();
  const { tenant } = useTenant();
  const navigate = useNavigate();
  const tenantSlug = urlTenant || 'trending';

  const { data: movie, isLoading, error } = useQuery({
    queryKey: ['movie', tmdbId],
    queryFn: () => moviesApi.getMovie(tmdbId!),
    enabled: !!tmdbId,
  });

  // Fetch related movies from the same tenant
  const { data: relatedMovies } = useQuery({
    queryKey: ['movies', tenant, 'related'],
    queryFn: () => moviesApi.getMovies({ limit: 8 }),
    enabled: !!movie,
  });

  if (isLoading) {
    return (
      <Layout>
        <div className="movie-detail-loading">Loading movie details...</div>
      </Layout>
    );
  }

  if (error || !movie) {
    return (
      <Layout>
        <div className="movie-detail-error">
          <h2>Movie not found</h2>
          <button onClick={() => navigate(`/${tenant}`)}>Back to Movies</button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="movie-detail">
        {/* Backdrop Header */}
        <div
          className="movie-detail-backdrop"
          style={{
            backgroundImage: movie.backdrop_url
              ? `url(${movie.backdrop_url})`
              : undefined
          }}
        >
          <div className="movie-detail-backdrop-overlay" />
        </div>

        {/* Content */}
        <div className="movie-detail-content">
          <button
            className="movie-detail-back-btn"
            onClick={() => navigate(`/${tenantSlug}`)}
          >
            ← Back
          </button>

          <div className="movie-detail-main">
            {/* Poster */}
            <div className="movie-detail-poster-wrapper">
              {movie.poster_url ? (
                <img
                  src={movie.poster_url}
                  alt={movie.movie_name}
                  className="movie-detail-poster"
                />
              ) : (
                <div className="movie-detail-poster-placeholder">
                  <span>No Image</span>
                </div>
              )}
            </div>

            {/* Info */}
            <div className="movie-detail-info">
              <h1 className="movie-detail-title">{movie.movie_name}</h1>

              {movie.original_title && movie.original_title !== movie.movie_name && (
                <p className="movie-detail-original-title">{movie.original_title}</p>
              )}

              <div className="movie-detail-meta">
                {movie.year && (
                  <span className="movie-detail-year">{movie.year}</span>
                )}
                {movie.runtime && (
                  <>
                    <span className="movie-detail-separator">•</span>
                    <span className="movie-detail-runtime">{movie.runtime}</span>
                  </>
                )}
                {movie.genre && (
                  <>
                    <span className="movie-detail-separator">•</span>
                    <span className="movie-detail-genre">{movie.genre}</span>
                  </>
                )}
              </div>

              <div className="movie-detail-rating">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  className="movie-detail-star"
                >
                  <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
                </svg>
                <span className="movie-detail-rating-value">{movie.rating.toFixed(1)}</span>
                <span className="movie-detail-rating-max">/10</span>
              </div>

              {movie.overview && (
                <div className="movie-detail-overview">
                  <h2>Overview</h2>
                  <p>{movie.overview}</p>
                </div>
              )}

              {/* Action Buttons */}
              <div className="movie-detail-actions">
                <button
                  onClick={() => window.open(movie.movie_link, '_blank')}
                  disabled={!movie.movie_link}
                  className="movie-detail-action-btn movie-detail-action-trailer"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                  Trailer
                </button>
                <button className="movie-detail-action-btn movie-detail-action-share">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path>
                    <polyline points="16 6 12 2 8 6"></polyline>
                    <line x1="12" y1="2" x2="12" y2="15"></line>
                  </svg>
                  Share
                </button>
                {movie.fshare_link && (
                  <button
                    onClick={() => window.open(movie.fshare_link, '_blank')}
                    className="movie-detail-action-btn movie-detail-action-download"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                      <polyline points="7 10 12 15 17 10"></polyline>
                      <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    Download
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* Related Movies Section */}
          {relatedMovies && relatedMovies.length > 0 && (
            <div className="movie-detail-related">
              <h2 className="movie-detail-related-title">Related Movies</h2>
              <div className="movie-detail-related-grid">
                {relatedMovies.slice(0, 4).filter(m => m.tmdb_id !== tmdbId).map((relatedMovie) => (
                  <Link
                    key={relatedMovie.tmdb_id}
                    to={`/${tenantSlug}/movie/${relatedMovie.tmdb_id}`}
                    className="movie-detail-related-card"
                  >
                    {relatedMovie.poster_url ? (
                      <img
                        src={relatedMovie.poster_url}
                        alt={relatedMovie.movie_name}
                        className="movie-detail-related-poster"
                      />
                    ) : (
                      <div className="movie-detail-related-poster-placeholder">
                        <span>No Image</span>
                      </div>
                    )}
                    <div className="movie-detail-related-info">
                      <h3>{relatedMovie.movie_name}</h3>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};
