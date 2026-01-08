import { apiClient } from './client';
import type { Movie, Category } from '../types/movie';

export interface GetMoviesParams {
  limit?: number;
  genre?: string;
  year?: number;
}

export const moviesApi = {
  // Get movies with optional filters
  getMovies: async (params?: GetMoviesParams): Promise<Movie[]> => {
    const response = await apiClient.get<Movie[]>('/movies', { params });
    return response.data;
  },

  // Get single movie by TMDB ID
  getMovie: async (tmdbId: string): Promise<Movie> => {
    const response = await apiClient.get<Movie>(`/movies/${tmdbId}`);
    return response.data;
  },

  // Get list of tenants
  getTenants: async (): Promise<string[]> => {
    const response = await apiClient.get<string[]>('/tenants');
    return response.data;
  },

  // Get categories hierarchy
  getCategories: async (maxLevel?: number): Promise<Category[]> => {
    const params = maxLevel !== undefined ? { max_level: maxLevel } : {};
    const response = await apiClient.get<Category[]>('/categories', { params });
    return response.data;
  },
};
