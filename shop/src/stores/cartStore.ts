import { atom, computed } from 'nanostores';
import type { CartItem, Cart } from '../types/cart';

const STORAGE_KEY = 'shop-cart';

// Main cart store - Record<string, CartItem>
export const cartStore = atom<Cart>({});

// Cart UI state
export const isCartOpen = atom<boolean>(false);

// Computed stores
export const cartItemsArray = computed(cartStore, (cart) => Object.values(cart));

export const cartItemCount = computed(cartItemsArray, (items) =>
  items.reduce((total, item) => total + item.quantity, 0)
);

export const cartTotal = computed(cartItemsArray, (items) =>
  items.reduce((total, item) => total + item.price * item.quantity, 0)
);

// Initialize store from localStorage
function hydrateStore() {
  if (typeof window === 'undefined') return;
  
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const cart = JSON.parse(stored) as Cart;
      cartStore.set(cart);
    }
  } catch (error) {
    console.error('Error reading cart from localStorage:', error);
  }
}

// Sync store to localStorage
function syncToStorage(cart: Cart) {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
  } catch (error) {
    console.error('Error saving cart to localStorage:', error);
  }
}

// Track if we've hydrated to prevent overwriting localStorage during initial load
let isHydrated = false;

// Subscribe to cart changes and sync to localStorage (only after hydration)
cartStore.subscribe((cart) => {
  if (isHydrated) {
    syncToStorage(cart);
  }
});

// Hydrate on mount (client-side only) - do this after setting up subscription
if (typeof window !== 'undefined') {
  hydrateStore();
  isHydrated = true;
}

// Actions
export function addToCart(item: Omit<CartItem, 'quantity'> | CartItem): void {
  const cart = cartStore.get();
  const quantityToAdd = 'quantity' in item ? item.quantity : 1;
  
  if (cart[item.id]) {
    // Item exists, update quantity
    cart[item.id].quantity += quantityToAdd;
  } else {
    // New item, add to cart
    cart[item.id] = {
      ...item,
      quantity: quantityToAdd
    };
  }
  
  cartStore.set({ ...cart });
}

export function removeFromCart(itemId: string): void {
  const cart = cartStore.get();
  const item = cart[itemId];
  
  if (item) {
    const newCart = { ...cart };
    delete newCart[itemId];
    cartStore.set(newCart);
  }
}

export function updateQuantity(itemId: string, quantity: number): void {
  if (quantity <= 0) {
    removeFromCart(itemId);
    return;
  }
  
  const cart = cartStore.get();
  
  if (cart[itemId]) {
    const newCart = { ...cart };
    newCart[itemId] = {
      ...cart[itemId],
      quantity
    };
    cartStore.set(newCart);
  }
}

export function clearCart(): void {
  cartStore.set({});
}

// Cart UI actions
export function openCart(): void {
  isCartOpen.set(true);
}

export function closeCart(): void {
  isCartOpen.set(false);
}

