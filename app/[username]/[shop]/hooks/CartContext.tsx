'use client';

import {
  createContext,
  useReducer,
  useContext,
  ReactNode,
} from 'react';
import { cartReducer } from './cartReducer';
import { TCartState, TCartAction } from './types';

const CartContext = createContext<{
  state: TCartState;
  dispatch: React.Dispatch<TCartAction>;
} | null>(null);

const initialCart: TCartState = { items: [] };

export function CartProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, initialCart);

  return (
    <CartContext.Provider value={{ state, dispatch }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCartContext() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error('useCartContext must be used inside <CartProvider>');
  return ctx;
}
