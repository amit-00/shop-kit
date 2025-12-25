'use client';

import { createContext, useContext, useState, useCallback, useMemo } from 'react';

interface SearchContextType {
  searchQuery: string;
  isSearchOpen: boolean;
  openSearch: () => void;
  closeSearch: () => void;
  setSearchQuery: (query: string) => void;
}

const SearchContext = createContext<SearchContextType | undefined>(undefined);

export function SearchProvider({ children }: { children: React.ReactNode }) {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [isSearchOpen, setIsSearchOpen] = useState<boolean>(false);

  const openSearch = useCallback(() => {
    setIsSearchOpen(true);
  }, []);

  const closeSearch = useCallback(() => {
    setIsSearchOpen(false);
  }, []);

  const value = useMemo(() => ({
    searchQuery,
    isSearchOpen,
    openSearch,
    closeSearch,
    setSearchQuery,
  }), [searchQuery, isSearchOpen, openSearch, closeSearch, setSearchQuery]);

  return <SearchContext.Provider value={value}>{children}</SearchContext.Provider>;
}

export function useSearch() {
  const context = useContext(SearchContext);
  if (context === undefined) {
    throw new Error('useSearch must be used within a SearchProvider');
  }
  return context;
}