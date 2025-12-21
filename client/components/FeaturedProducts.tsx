'use client';

import { useRef, useState, useEffect } from 'react';
import { Product } from '@/types/product';
import ProductItem from './ProductItem';

interface FeaturedProductsProps {
  products?: Product[];
  name?: string;
}

function ProductSkeleton() {
  return (
    <div className="flex flex-col shrink-0 min-w-[280px]">
      <div className="relative w-full aspect-square mb-4 overflow-hidden rounded-lg bg-base-200 animate-pulse" />
      <div className="h-5 bg-base-200 rounded mb-1 animate-pulse w-3/4" />
      <div className="h-4 bg-base-200 rounded animate-pulse w-1/2" />
    </div>
  );
}

export default function FeaturedProducts({ products, name = 'Featured' }: FeaturedProductsProps) {
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(false);

  const checkScrollPosition = () => {
    const container = scrollContainerRef.current;
    if (!container) return;

    setCanScrollLeft(container.scrollLeft > 0);
    setCanScrollRight(
      container.scrollLeft + container.clientWidth < container.scrollWidth
    );
  };

  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    // Check initial scroll state
    checkScrollPosition();

    // Listen to scroll events
    container.addEventListener('scroll', checkScrollPosition);

    // Also check on resize
    const handleResize = () => {
      checkScrollPosition();
    };
    window.addEventListener('resize', handleResize);

    return () => {
      container.removeEventListener('scroll', checkScrollPosition);
      window.removeEventListener('resize', handleResize);
    };
  }, [products]);

  const scrollLeft = () => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const scrollAmount = container.clientWidth;
    container.scrollBy({
      left: -scrollAmount,
      behavior: 'smooth',
    });
  };

  const scrollRight = () => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const scrollAmount = container.clientWidth;
    container.scrollBy({
      left: scrollAmount,
      behavior: 'smooth',
    });
  };

  // Show skeleton UI while loading (products is undefined)
  if (products === undefined) {
    return (
      <section className="min-h-[400px] bg-base-100 px-4 py-16 overflow-x-clip">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-base-content uppercase tracking-tight mb-12">
            {name}
          </h2>
          <div className="overflow-x-hidden">
            <div className="flex flex-row gap-8 overflow-x-auto hide-scrollbar">
              {[...Array(4)].map((_, index) => (
                <ProductSkeleton key={index} />
              ))}
            </div>
          </div>
        </div>
      </section>
    );
  }

  // Don't render if no products
  if (products.length === 0) {
    return null;
  }

  return (
    <section className="min-h-[400px] bg-base-100 px-4 py-16 overflow-x-clip">
      <div className="max-w-6xl mx-auto relative">
        <h2 className="text-4xl md:text-5xl font-semibold text-base-content uppercase tracking-tight mb-12">
          {name}
        </h2>
        <div
          ref={scrollContainerRef}
          className="flex flex-row gap-8 overflow-x-auto hide-scrollbar"
          style={{ 
            marginRight: 'calc(-50vw + 50%)',
            paddingRight: 'calc(50vw - 50%)'
          }}
        >
          {products.map((product) => (
            <div key={product.id} className="shrink-0 min-w-[280px]">
              <ProductItem product={product} />
            </div>
          ))}
        </div>
        <div className="flex gap-2 mt-4">
          <button
            onClick={scrollLeft}
            disabled={!canScrollLeft}
            className="btn btn-ghost btn-sm"
          >
            ←
          </button>
          <button
            onClick={scrollRight}
            disabled={!canScrollRight}
            className="btn btn-ghost btn-sm"
          >
            →
          </button>
        </div>
      </div>
    </section>
  );
}

