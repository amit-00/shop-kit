'use client';

import { useCart } from '../stores/cartStore';

export default function CartBadge() {
  const { itemCount, openCart } = useCart();
  const count = itemCount;

  const displayCount = count > 9 ? '9+' : count.toString();
  const showBadge = count > 0;
  const showDot = count > 9;

  return (
    <button
      className="bg-transparent border-none cursor-pointer p-2 relative flex items-center justify-center"
      aria-label="Shopping cart"
      onClick={openCart}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        className="w-5 h-5 text-base-content"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
        ></path>
      </svg>
      {showBadge && (
        <>
          {showDot && (
            <span className="absolute top-1 right-1 w-2 h-2 bg-secondary rounded-full"></span>
          )}
          <span className="absolute -top-1 -right-1 min-w-5 h-5 px-1 bg-secondary text-secondary-content text-xs font-bold rounded-full flex items-center justify-center">
            {displayCount}
          </span>
        </>
      )}
    </button>
  );
}

