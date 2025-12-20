import { useStore } from '@nanostores/react';
import { useEffect } from 'react';
import { cartItemsArray, cartTotal, isCartOpen, closeCart } from '../stores/cartStore';
import CartItem from './CartItem';

export default function Cart() {
  const items = useStore(cartItemsArray);
  const total = useStore(cartTotal);
  const isOpen = useStore(isCartOpen);

  // Safe scroll-lock: remember previous value and restore on close/unmount
  useEffect(() => {
    const prev = document.body.style.overflow;
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.body.style.overflow = prev;
    };
  }, [isOpen]);

  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        closeCart();
      }
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen]);

  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      closeCart();
    }
  };

  return (
    <>
      <div
        id="cart-backdrop"
        className={`cart-backdrop fixed inset-0 bg-base-content/50 z-40 transition-opacity ${
          isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={handleBackdropClick}
      ></div>
      <div
        id="cart-sidebar"
        role="dialog"
        aria-modal="true"
        aria-hidden={!isOpen}
        aria-label="Shopping cart"
        className={`cart-sidebar fixed right-0 top-0 h-full w-full md:w-96 bg-base-100 z-50 shadow-lg transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-base-300">
            <h2 className="text-xl font-bold text-base-content uppercase tracking-wide">
              Cart
            </h2>
            <button
              id="cart-close-btn"
              className="bg-transparent border-none cursor-pointer p-2 hover:opacity-70 transition-opacity"
              aria-label="Close cart"
              onClick={closeCart}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="w-6 h-6 text-base-content"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M6 18L18 6M6 6l12 12"
                ></path>
              </svg>
            </button>
          </div>

          {/* Cart Items Container (Scrollable) */}
          <div id="cart-items-container" className="flex-1 overflow-y-auto p-6">
            {items.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-base-content/60">Your cart is empty</p>
              </div>
            ) : (
              <div id="cart-items-list">
                {items.map((item) => (
                  <CartItem key={item.id} item={item} />
                ))}
              </div>
            )}
          </div>

          {/* Footer */}
          {items.length > 0 && (
            <div className="border-t border-base-300 p-6 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-base-content/60 text-sm uppercase tracking-wide">
                  Total
                </span>
                <span id="cart-total" className="text-xl font-bold text-base-content">
                  ${total.toFixed(2)}
                </span>
              </div>
              <button id="checkout-btn" className="btn btn-primary w-full btn-lg group">
                Checkout
                <span className="text-xl arrow-hover">→</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

