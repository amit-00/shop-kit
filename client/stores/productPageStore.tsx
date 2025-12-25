'use client';

import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';

interface ProductPageContextType {
  quantity: number;
  setQuantity: (quantity: number) => void;
}

const ProductPageContext = createContext<ProductPageContextType | undefined>(undefined);

export function ProductPageProvider({ children }: { children: React.ReactNode }) {
  const [quantity, setQuantityState] = useState(1);

  const setQuantity = useCallback((newQuantity: number) => {
    if (newQuantity >= 1) {
      setQuantityState(newQuantity);
    }
  }, []);

  const value = useMemo(
    () => ({
      quantity,
      setQuantity,
    }),
    [quantity, setQuantity]
  );

  return (
    <ProductPageContext.Provider value={value}>
      {children}
    </ProductPageContext.Provider>
  );
}

export function useProductPage() {
  const context = useContext(ProductPageContext);
  if (context === undefined) {
    throw new Error('useProductPage must be used within a ProductPageProvider');
  }
  return context;
}

