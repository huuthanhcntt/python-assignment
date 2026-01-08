import { useQuery } from '@tanstack/react-query';
import { moviesApi } from '../api';
import type { GetMoviesParams } from '../api';
import type { Movie } from '../types/movie';

export const useMovies = (params?: GetMoviesParams) => {
  return useQuery<Movie[], Error>({
    queryKey: ['movies', params],
    queryFn: () => moviesApi.getMovies(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
  });
};

export const useMovie = (tmdbId: string) => {
  return useQuery<Movie, Error>({
    queryKey: ['movie', tmdbId],
    queryFn: () => moviesApi.getMovie(tmdbId),
    enabled: !!tmdbId,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useTenants = () => {
  return useQuery<string[], Error>({
    queryKey: ['tenants'],
    queryFn: () => moviesApi.getTenants(),
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};
