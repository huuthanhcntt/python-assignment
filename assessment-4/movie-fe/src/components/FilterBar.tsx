import { useMovieStore } from '../store';
import './FilterBar.css';

export const FilterBar = () => {
  const filters = useMovieStore((state) => state.filters);
  const setFilters = useMovieStore((state) => state.setFilters);
  const clearFilters = useMovieStore((state) => state.clearFilters);

  const handleLimitChange = (limit: number) => {
    setFilters({ ...filters, limit });
  };

  const handleYearChange = (year: string) => {
    setFilters({
      ...filters,
      year: year ? parseInt(year) : undefined,
    });
  };

  const handleClearFilters = () => {
    clearFilters();
  };

  const hasActiveFilters = filters.year || filters.limit !== 20;

  return (
    <div className="filter-bar">
      <div className="filter-group">
        <label htmlFor="limit-select">Show:</label>
        <select
          id="limit-select"
          value={filters.limit || 20}
          onChange={(e) => handleLimitChange(Number(e.target.value))}
          className="filter-select"
        >
          <option value={10}>10 movies</option>
          <option value={20}>20 movies</option>
          <option value={50}>50 movies</option>
          <option value={100}>100 movies</option>
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="year-input">Year:</label>
        <input
          id="year-input"
          type="number"
          placeholder="Filter by year..."
          value={filters.year || ''}
          onChange={(e) => handleYearChange(e.target.value)}
          className="filter-input"
          min="1900"
          max={new Date().getFullYear()}
        />
      </div>

      {hasActiveFilters && (
        <button onClick={handleClearFilters} className="clear-filters-button">
          Clear Filters
        </button>
      )}
    </div>
  );
};
