import { useState, useEffect, ChangeEvent } from 'react';
import { useDebounce } from '../hooks';
import './SearchBar.css';

interface SearchBarProps {
  onSearch: (searchTerm: string) => void;
  placeholder?: string;
  debounceDelay?: number;
}

export const SearchBar = ({
  onSearch,
  placeholder = 'Search movies...',
  debounceDelay = 500
}: SearchBarProps) => {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, debounceDelay);

  // Effect to call onSearch when debounced value changes
  useEffect(() => {
    onSearch(debouncedSearchTerm);
  }, [debouncedSearchTerm, onSearch]);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleClear = () => {
    setSearchTerm('');
    onSearch('');
  };

  return (
    <div className="search-bar">
      <div className="search-input-wrapper">
        <svg
          className="search-icon"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.35-4.35" />
        </svg>
        <input
          type="text"
          className="search-input"
          placeholder={placeholder}
          value={searchTerm}
          onChange={handleChange}
          autoComplete="off"
        />
        {searchTerm && (
          <button
            className="clear-button"
            onClick={handleClear}
            aria-label="Clear search"
            type="button"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        )}
      </div>
      {searchTerm && searchTerm !== debouncedSearchTerm && (
        <div className="search-status">Searching...</div>
      )}
    </div>
  );
};
