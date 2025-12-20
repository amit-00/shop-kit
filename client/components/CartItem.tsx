'use client';

import { useCart } from '../stores/cartStore';
import type { CartItem as CartItemType } from '../types/cart';

interface CartItemProps {
  item: CartItemType;
}

export default function CartItem({ item }: CartItemProps) {
  const { removeFromCart, updateQuantity } = useCart();

  const handleRemove = () => {
    removeFromCart(item.id);
  };

  const handleDecrease = () => {
    updateQuantity(item.id, item.quantity - 1);
  };

  const handleIncrease = () => {
    updateQuantity(item.id, item.quantity + 1);
  };

  return (
    <div
      className="cart-item flex gap-4 py-4 border-b border-base-300"
      data-item-id={item.id}
    >
      <div className="shrink-0">
        <img
          src={item.image}
          alt={item.title}
          className="w-20 h-20 object-cover rounded border border-base-300"
        />
      </div>
      <div className="flex-1 flex flex-col gap-2">
        <div className="flex items-start justify-between">
          <h3 className="text-base-content font-medium text-sm">{item.title}</h3>
          <button
            className="remove-item-btn bg-transparent border-none cursor-pointer p-1 hover:opacity-70 transition-opacity"
            aria-label="Remove item"
            onClick={handleRemove}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="w-4 h-4 text-base-content"
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
        <div className="text-base-content/60 text-sm">${item.price.toFixed(2)}</div>
        <div className="flex items-center gap-2">
          <button
            className="decrease-qty-btn btn btn-ghost btn-sm h-8 w-8 min-h-0 p-0"
            aria-label="Decrease quantity"
            onClick={handleDecrease}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="w-4 h-4"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M20 12H4"
              ></path>
            </svg>
          </button>
          <span className="quantity text-base-content text-sm min-w-8 text-center">
            {item.quantity}
          </span>
          <button
            className="increase-qty-btn btn btn-ghost btn-sm h-8 w-8 min-h-0 p-0"
            aria-label="Increase quantity"
            onClick={handleIncrease}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="w-4 h-4"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 4v16m8-8H4"
              ></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

