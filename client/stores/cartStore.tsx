'use client';

import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';
import type { CartItem } from '../types/cart';

interface CartContextType {
  items: CartItem[];
  isOpen: boolean;
  itemCount: number;
  total: number;
  addToCart: (item: Omit<CartItem, 'quantity'>) => void;
  removeFromCart: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  openCart: () => void;
  closeCart: () => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  const addToCart = useCallback((item: Omit<CartItem, 'quantity'>) => {
    setItems((prev) => {
      const existing = prev.find((i) => i.id === item.id);
      if (existing) {
        return prev.map((i) =>
          i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
        );
      }
      return [...prev, { ...item, quantity: 1 }];
    });
  }, []);

  const removeFromCart = useCallback((id: string) => {
    setItems((prev) => prev.filter((item) => item.id !== id));
  }, []);

  const updateQuantity = useCallback((id: string, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(id);
      return;
    }
    setItems((prev) =>
      prev.map((item) => (item.id === id ? { ...item, quantity } : item))
    );
  }, [removeFromCart]);

  const openCart = useCallback(() => {
    setIsOpen(true);
  }, []);

  const closeCart = useCallback(() => {
    setIsOpen(false);
  }, []);

  const itemCount = useMemo(
    () => items.reduce((sum, item) => sum + item.quantity, 0),
    [items]
  );

  const total = useMemo(
    () => items.reduce((sum, item) => sum + item.price * item.quantity, 0),
    [items]
  );

  const value = useMemo(
    () => ({
      items,
      isOpen,
      itemCount,
      total,
      addToCart,
      removeFromCart,
      updateQuantity,
      openCart,
      closeCart,
    }),
    [items, isOpen, itemCount, total, addToCart, removeFromCart, updateQuantity, openCart, closeCart]
  );

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
}

// Export individual values for compatibility with existing component imports
export const cartItemsArray = {
  get: () => {
    throw new Error('cartItemsArray.get() is not available. Use useCart() hook instead.');
  },
  subscribe: () => {
    throw new Error('cartItemsArray.subscribe() is not available. Use useCart() hook instead.');
  },
};

export const cartTotal = {
  get: () => {
    throw new Error('cartTotal.get() is not available. Use useCart() hook instead.');
  },
  subscribe: () => {
    throw new Error('cartTotal.subscribe() is not available. Use useCart() hook instead.');
  },
};

export const isCartOpen = {
  get: () => {
    throw new Error('isCartOpen.get() is not available. Use useCart() hook instead.');
  },
  subscribe: () => {
    throw new Error('isCartOpen.subscribe() is not available. Use useCart() hook instead.');
  },
};

export const cartItemCount = {
  get: () => {
    throw new Error('cartItemCount.get() is not available. Use useCart() hook instead.');
  },
  subscribe: () => {
    throw new Error('cartItemCount.subscribe() is not available. Use useCart() hook instead.');
  },
};

