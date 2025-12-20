'use client';

import { useState, useEffect, useMemo } from 'react';
import { Catalog } from '@/types/catalog';
import ProductItem from './ProductItem';
import { createSearchText, searchProducts, ProductWithSearchText } from '@/lib/searchUtils';

interface ShopProps {
  catalogs: Record<string, Catalog>;
}

export default function Shop({ catalogs }: ShopProps) {
  const catalogIds = useMemo(() => Object.keys(catalogs), [catalogs]);
  const [selectedCatalogId, setSelectedCatalogId] = useState<string>(
    catalogIds[0] || ''
  );
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [debouncedQuery, setDebouncedQuery] = useState<string>('');
  const [sortBy, setSortBy] = useState<'none' | 'price-high' | 'price-low'>('none');

  // Update selected catalog ID if catalogs change
  useEffect(() => {
    if (catalogIds.length > 0 && !catalogs[selectedCatalogId]) {
      setSelectedCatalogId(catalogIds[0]);
    }
  }, [catalogIds, selectedCatalogId, catalogs]);

  // Debounce search query
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(searchQuery);
    }, 300);

    return () => {
      clearTimeout(timer);
    };
  }, [searchQuery]);

  const selectedCatalog = catalogs[selectedCatalogId];
  
  // Add searchText property to products for searching
  const productsWithSearchText: ProductWithSearchText[] = useMemo(() => {
    if (!selectedCatalog) return [];
    return selectedCatalog.products.map((product) => ({
      ...product,
      searchText: createSearchText(product),
    }));
  }, [selectedCatalog]);

  const filteredProducts = useMemo(() => {
    const searched = searchProducts(productsWithSearchText, debouncedQuery);
    // Sort by price only if a filter is selected
    if (sortBy === 'none') {
      return searched;
    }
    const sorted = [...searched].sort((a, b) => {
      if (sortBy === 'price-high') {
        return b.price - a.price;
      } else {
        return a.price - b.price;
      }
    });
    return sorted;
  }, [productsWithSearchText, debouncedQuery, sortBy]);

  return (
    <section className="min-h-[600px] bg-base-100 px-4 py-16">
      <div className="max-w-6xl mx-auto">
        {/* Catalog Selector and Search Bar */}
        <h2 className="text-4xl md:text-5xl font-semibold text-base-content uppercase tracking-tight mb-12">
          Shop
        </h2>
        <div className="mb-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-center gap-4 w-full md:w-auto">
            {/* Catalog Selector */}
            <div className="dropdown dropdown-end">
              <div
                tabIndex={0}
                role="button"
                className="btn btn-ghost border border-base-300 bg-base-300 hover:border-base-content/20 min-w-[200px] justify-between"
              >
                <span className="text-base-content/80 text-sm uppercase tracking-wide">
                  {selectedCatalog?.name || 'Select Catalog'}
                </span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  className="w-4 h-4 text-base-content/60"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </div>
              <ul
                tabIndex={0}
                className="dropdown-content menu bg-base-100 border border-base-300 shadow-lg rounded-lg w-[200px] mt-2 z-10"
              >
                {catalogIds.map((catalogId) => {
                  const catalog = catalogs[catalogId];
                  return (
                    <li key={catalogId}>
                      <button
                        className={`text-sm uppercase tracking-wide ${
                          selectedCatalogId === catalogId
                            ? 'bg-base-200 text-base-content'
                            : 'text-base-content/60 hover:text-base-content hover:bg-base-200'
                        }`}
                        onClick={() => {
                          setSelectedCatalogId(catalogId);
                          setSearchQuery(''); // Clear search when switching catalogs
                        }}
                      >
                        {catalog.name}
                      </button>
                    </li>
                  );
                })}
              </ul>
            </div>
            {/* Search Bar */}
            <div className="flex-1 md:flex-initial">
              <input
                type="text"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input input-bordered w-full md:w-64 border-base-300 bg-base-200 focus:border-base-content/20 focus:outline-none"
              />
            </div>
          </div>
          {/* Filter */}
          <div className="dropdown dropdown-end">
            <div
              tabIndex={0}
              role="button"
              className="btn btn-ghost border border-base-300 bg-base-300 hover:border-base-content/20 min-w-[200px] justify-between"
            >
              <span className="text-base-content/80 text-sm uppercase tracking-wide">
                Filter
              </span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="w-4 h-4 text-base-content/60"
              >
                <rect x="4" y="7" width="16" height="2" rx="1" fill="currentColor" />
                <rect x="6" y="12" width="12" height="2" rx="1" fill="currentColor" />
                <rect x="8" y="17" width="8" height="2" rx="1" fill="currentColor" />
              </svg>
            </div>
            <ul
              tabIndex={0}
              className="dropdown-content menu bg-base-100 border border-base-300 shadow-lg rounded-lg w-[200px] mt-2 z-10"
            >
              <li>
                <button
                  className={`text-sm uppercase tracking-wide ${
                    sortBy === 'none'
                      ? 'bg-base-200 text-base-content'
                      : 'text-base-content/60 hover:text-base-content hover:bg-base-200'
                  }`}
                  onClick={() => setSortBy('none')}
                >
                  None
                </button>
              </li>
              <li>
                <button
                  className={`text-sm uppercase tracking-wide ${
                    sortBy === 'price-high'
                      ? 'bg-base-200 text-base-content'
                      : 'text-base-content/60 hover:text-base-content hover:bg-base-200'
                  }`}
                  onClick={() => setSortBy('price-high')}
                >
                  Price High
                </button>
              </li>
              <li>
                <button
                  className={`text-sm uppercase tracking-wide ${
                    sortBy === 'price-low'
                      ? 'bg-base-200 text-base-content'
                      : 'text-base-content/60 hover:text-base-content hover:bg-base-200'
                  }`}
                  onClick={() => setSortBy('price-low')}
                >
                  Price Low
                </button>
              </li>
            </ul>
          </div>
        </div>

        {/* Products Grid */}
        {filteredProducts.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {filteredProducts.map((product) => (
              <ProductItem key={product.id} product={product} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-base-content/60">
              {debouncedQuery
                ? 'No products found matching your search.'
                : 'No products available in this catalog.'}
            </p>
          </div>
        )}
      </div>
    </section>
  );
}

