import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface MovieFilters {
  limit?: number;
  genre?: string;
  year?: number;
}

interface MovieState {
  // State
  searchTerm: string;
  filters: MovieFilters;
  selectedTenant: string;

  // Actions
  setSearchTerm: (term: string) => void;
  setFilters: (filters: MovieFilters) => void;
  setSelectedTenant: (tenant: string) => void;
  clearFilters: () => void;
}

export const useMovieStore = create<MovieState>()(
  devtools(
    (set) => ({
      // Initial state
      searchTerm: '',
      filters: { limit: 20 },
      selectedTenant: localStorage.getItem('tenant') || 'default',

      // Actions
      setSearchTerm: (term) =>
        set({ searchTerm: term }, false, 'setSearchTerm'),

      setFilters: (filters) =>
        set({ filters }, false, 'setFilters'),

      setSelectedTenant: (tenant) => {
        localStorage.setItem('tenant', tenant);
        set({ selectedTenant: tenant }, false, 'setSelectedTenant');
      },

      clearFilters: () =>
        set(
          { searchTerm: '', filters: { limit: 20 } },
          false,
          'clearFilters'
        ),
    }),
    { name: 'MovieStore' }
  )
);
