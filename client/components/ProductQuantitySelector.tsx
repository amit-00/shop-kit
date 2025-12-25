'use client';

import { useProductPage } from '@/stores/productPageStore';

export default function ProductQuantitySelector() {
  const { quantity, setQuantity } = useProductPage();

  const handleQuantityChange = (newQuantity: number) => {
    if (newQuantity < 1) return;
    setQuantity(newQuantity);
  };

  const incrementQuantity = () => {
    setQuantity(quantity + 1);
  };

  const decrementQuantity = () => {
    setQuantity(quantity > 1 ? quantity - 1 : 1);
  };

  return (
    <div className="mb-6">
      <label className="block text-sm font-medium text-base-content/80 mb-2 uppercase tracking-wide">
        Quantity
      </label>
      <div className="flex items-center gap-2">
        <button
          onClick={decrementQuantity}
          className="btn btn-ghost btn-sm border border-base-300 hover:border-base-content/20"
          aria-label="Decrease quantity"
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
            />
          </svg>
        </button>
        <input
          inputMode='numeric'
          value={quantity}
          onChange={(e) => handleQuantityChange(parseInt(e.target.value) || 1)}
          className="input input-bordered w-20 text-center border-base-300 bg-base-200 focus:border-base-content/20 focus:outline-none"
        />
        <button
          onClick={incrementQuantity}
          className="btn btn-ghost btn-sm border border-base-300 hover:border-base-content/20"
          aria-label="Increase quantity"
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
            />
          </svg>
        </button>
      </div>
    </div>
  );
}

