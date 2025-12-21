'use client';

import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';
import type { Product } from '../types/product';

interface ProductContextType {
  activeProduct: Product | null;
  setActiveProduct: (product: Product) => void;
  clearActiveProduct: () => void;
}

const ProductContext = createContext<ProductContextType | undefined>(undefined);

export function ProductProvider({ children }: { children: React.ReactNode }) {
  const [activeProduct, setActiveProductState] = useState<Product | null>(null);

  const setActiveProduct = useCallback((product: Product) => {
    setActiveProductState(product);
  }, []);

  const clearActiveProduct = useCallback(() => {
    setActiveProductState(null);
  }, []);

  const value = useMemo(
    () => ({
      activeProduct,
      setActiveProduct,
      clearActiveProduct,
    }),
    [activeProduct, setActiveProduct, clearActiveProduct]
  );

  return <ProductContext.Provider value={value}>{children}</ProductContext.Provider>;
}

export function useProduct() {
  const context = useContext(ProductContext);
  if (context === undefined) {
    throw new Error('useProduct must be used within a ProductProvider');
  }
  return context;
}

