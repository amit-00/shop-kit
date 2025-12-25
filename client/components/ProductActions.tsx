'use client';

import { useCart } from '@/stores/cartStore';
import { useProductPage } from '@/stores/productPageStore';

interface ProductActionsProps {
  productId: string;
  productName: string;
  productPrice: number;
  productImage: string;
}

export default function ProductActions({
  productId,
  productName,
  productPrice,
  productImage,
}: ProductActionsProps) {
  const { addToCart, updateQuantity, items } = useCart();
  const { quantity } = useProductPage();

  const handleAddToCart = () => {
    if (!productImage) return;

    const existingItem = items.find((item) => item.id === productId);

    if (existingItem) {
      // Item already exists, update quantity by adding the desired quantity
      updateQuantity(productId, existingItem.quantity + quantity);
    } else {
      // Item doesn't exist, add it first
      addToCart({
        id: productId,
        title: productName,
        price: productPrice,
        image: productImage,
      });

      // Then update to the desired quantity if more than 1
      if (quantity > 1) {
        // Use setTimeout to ensure the item is added first
        setTimeout(() => {
          updateQuantity(productId, quantity);
        }, 0);
      }
    }
  };

  return (
    <div className="flex flex-col gap-4 mt-auto">
      {/* Buy Now Button */}
      <button className="btn btn-primary w-full btn-lg group">
        Buy Now
        <span className="text-xl arrow-hover">→</span>
      </button>

      {/* Add to Cart Button */}
      <button
        className="btn btn-neutral w-full btn-lg group"
        onClick={handleAddToCart}
      >
        Add to Cart
        <span className="text-xl arrow-hover">→</span>
      </button>
    </div>
  );
}

