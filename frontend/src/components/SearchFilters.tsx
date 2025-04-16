import React, { useState } from 'react';
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline';

interface SearchFiltersProps {
  onFiltersChange: (filters: {
    search?: string;
    file_type?: string;
    size_range?: string;
    date_range?: number;
  }) => void;
}

export const SearchFilters: React.FC<SearchFiltersProps> = ({ onFiltersChange }) => {
  const [search, setSearch] = useState('');
  const [fileType, setFileType] = useState('');
  const [sizeRange, setSizeRange] = useState('');
  const [dateRange, setDateRange] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  const sizeRanges = [
    { label: 'All Sizes', value: '' },
    { label: 'Small (<100KB)', value: '0,102400' },          // 0 to 100KB
    { label: 'Medium (100KB-200KB)', value: '102400,204800' }, // 100KB to 200KB
    { label: 'Large (200KB-500KB)', value: '204800,512000' },  // 200KB to 500KB
    { label: 'Very Large (>500KB)', value: '512000,999999999' } // More than 500KB
  ];

  const predefinedDateRanges = [
    { label: 'All Time', value: '' },
    { label: 'Last 24 Hours', value: '1' },
    { label: 'Last 7 Days', value: '7' },
    { label: 'Last 30 Days', value: '30' },
    { label: 'Last 90 Days', value: '90' }
  ];

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearch(value);
    applyFilters({ search: value });
  };

  const applyFilters = (additionalFilters = {}) => {
    const filters: any = { ...additionalFilters };
    
    if (search && !('search' in additionalFilters)) {
      filters.search = search;
    }
    
    if (fileType.trim()) {
      filters.file_type = fileType.trim();
    }
    
    if (sizeRange) {
      filters.size_range = sizeRange;
    }
    
    if (dateRange !== '') {
      const days = parseInt(dateRange);
      if (!isNaN(days) && days > 0) {
        filters.date_range = days;
      }
    }

    onFiltersChange(filters);
  };

  const handleApplyFilters = (e?: React.FormEvent) => {
    e?.preventDefault();
    applyFilters();
  };

  const handleResetFilters = () => {
    setFileType('');
    setSizeRange('');
    setDateRange('');
    setSearch('');
    onFiltersChange({});
  };

  return (
    <div className="p-6">
      <form onSubmit={handleApplyFilters} className="space-y-4">
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <div className="relative rounded-md shadow-sm">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={search}
                onChange={handleSearch}
                placeholder="Search files..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
            </div>
          </div>
          <button
            type="button"
            onClick={() => setShowFilters(!showFilters)}
            className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <FunnelIcon className="h-4 w-4 mr-1" />
            Filters
          </button>
        </div>

        {showFilters && (
          <div className="mt-4 p-4 bg-gray-50 rounded-md">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              {/* File Type Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700">File Type</label>
                <input
                  type="text"
                  value={fileType}
                  onChange={(e) => setFileType(e.target.value)}
                  placeholder="e.g., image/jpeg, application/pdf"
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              </div>

              {/* Size Range Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700">File Size</label>
                <select
                  value={sizeRange}
                  onChange={(e) => setSizeRange(e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
                  {sizeRanges.map((range) => (
                    <option key={range.value} value={range.value}>
                      {range.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Upload Date Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700">Upload Date</label>
                <select
                  value={dateRange}
                  onChange={(e) => setDateRange(e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
                  {predefinedDateRanges.map((range) => (
                    <option key={range.value} value={range.value}>
                      {range.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="mt-4 flex justify-end space-x-3">
              <button
                type="button"
                onClick={handleResetFilters}
                className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Reset
              </button>
              <button
                type="submit"
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Apply Filters
              </button>
            </div>
          </div>
        )}
      </form>
    </div>
  );
}; 