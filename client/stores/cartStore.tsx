'use client';

import React, { createContext, useContext, useState, useCallback, useMemo, useEffect } from 'react';
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

// Helper function to get storage key
const getCartStorageKey = (shopSlug: string): string => {
  return `shop-kit-cart-${shopSlug}`;
};

// Helper functions for localStorage
const loadCartFromStorage = (shopSlug: string): CartItem[] => {
  if (typeof window === 'undefined') return [];
  try {
    const storageKey = getCartStorageKey(shopSlug);
    const stored = localStorage.getItem(storageKey);
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    console.error('Failed to load cart from localStorage:', error);
    return [];
  }
};

const saveCartToStorage = (items: CartItem[], shopSlug: string) => {
  if (typeof window === 'undefined') return;
  try {
    const storageKey = getCartStorageKey(shopSlug);
    localStorage.setItem(storageKey, JSON.stringify(items));
  } catch (error) {
    console.error('Failed to save cart to localStorage:', error);
  }
};

export function CartProvider({ 
  children, 
  shopSlug 
}: { 
  children: React.ReactNode;
  shopSlug: string;
}) {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  // Load cart from localStorage on mount
  useEffect(() => {
    const savedItems = loadCartFromStorage(shopSlug);
    setItems(savedItems);
    setIsInitialized(true);
  }, [shopSlug]);

  // Save cart to localStorage whenever items change (after initialization)
  useEffect(() => {
    if (isInitialized) {
      saveCartToStorage(items, shopSlug);
    }
  }, [items, isInitialized, shopSlug]);

  const addToCart = useCallback((item: Omit<CartItem, 'quantity'>) => {
    setItems((prev) => {
      const existing = prev.find((i) => i.id === item.id);
      const newItems = existing
        ? prev.map((i) =>
            i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
          )
        : [...prev, { ...item, quantity: 1 }];
      return newItems;
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

