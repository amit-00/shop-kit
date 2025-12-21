'use client';

import { useEffect } from 'react';
import Image from 'next/image';
import { useProduct } from '../stores/productStore';
import { useCart } from '../stores/cartStore';

export default function ProductDetails() {
  const { activeProduct, clearActiveProduct } = useProduct();
  const { addToCart } = useCart();

  const isOpen = activeProduct !== null;

  // Prevent body scroll when modal is open
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
        clearActiveProduct();
      }
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, clearActiveProduct]);

  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      clearActiveProduct();
    }
  };

  const handleAddToCart = () => {
    if (activeProduct) {
      addToCart({
        id: activeProduct.id,
        title: activeProduct.name,
        price: activeProduct.price,
        image: activeProduct.image,
      });
      clearActiveProduct();
    }
  };

  // Use empty values when no active product
  const productName = activeProduct?.name || '';
  const productPrice = activeProduct?.price ?? 0;
  const productImage = activeProduct?.image || '';
  const productDescription = activeProduct?.description || '';
  const productAlt = activeProduct?.name || 'Product';

  return (
    <>
      <div
        className={`fixed inset-0 bg-base-content/50 z-40 transition-opacity duration-300 ${
          isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={handleBackdropClick}
        aria-hidden={!isOpen}
      ></div>
      <div
        role="dialog"
        aria-modal="true"
        aria-hidden={!isOpen}
        aria-label="Product details"
        className={`fixed inset-0 z-50 flex items-center justify-center p-4 transition-opacity duration-300 ${
          isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={handleBackdropClick}
      >
        <div
          className={`bg-base-100 rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto transition-all duration-300 ${
            isOpen
              ? 'opacity-100 scale-100 translate-y-0'
              : 'opacity-0 scale-95 translate-y-4 pointer-events-none'
          }`}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex flex-col md:flex-row">
            {/* Product Image */}
            <div className="relative w-full md:w-1/2 aspect-square md:aspect-auto md:h-[600px] bg-base-200">
              {productImage && (
                <Image
                  src={productImage}
                  alt={productAlt}
                  fill
                  className="object-cover rounded-t-lg md:rounded-l-lg md:rounded-t-none"
                  sizes="(max-width: 768px) 100vw, 50vw"
                />
              )}
            </div>

            {/* Product Info */}
            <div className="w-full md:w-1/2 p-6 md:p-8 flex flex-col">
              {/* Close Button */}
              <button
                className="self-end bg-transparent border-none cursor-pointer p-2 hover:opacity-70 transition-opacity mb-4"
                aria-label="Close product details"
                onClick={clearActiveProduct}
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

              {/* Product Name */}
              <h2 className="text-3xl md:text-4xl font-bold text-base-content uppercase tracking-tight mb-4">
                {productName}
              </h2>

              {/* Price */}
              <p className="text-2xl md:text-3xl font-semibold text-base-content mb-6">
                {productPrice > 0 ? `$${productPrice.toFixed(2)}` : ''}
              </p>

              {/* Description */}
              {productDescription && (
                <div className="mb-8 flex-1">
                  <p className="text-base-content/80 text-base leading-relaxed">
                    {productDescription}
                  </p>
                </div>
              )}

              {/* Buy Now Button */}
              {activeProduct && (
                <button
                  className="btn btn-primary w-full btn-lg group mt-auto mb-4"
                >
                  Buy Now
                  <span className="text-xl arrow-hover">→</span>
                </button>
              )}

              {/* Add to Cart Button */}
              {activeProduct && (
                <button
                  className="btn btn-neutral w-full btn-lg group"
                  onClick={handleAddToCart}
                >
                  Add to Cart
                  <span className="text-xl arrow-hover">→</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

