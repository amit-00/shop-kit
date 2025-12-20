'use client';

import { Product } from '@/types/product';
import ProductItem from './ProductItem';

interface FeaturedProductsProps {
  products?: Product[];
  name?: string;
}

function ProductSkeleton() {
  return (
    <div className="flex flex-col">
      <div className="relative w-full aspect-square mb-4 overflow-hidden rounded-lg bg-base-200 animate-pulse" />
      <div className="h-5 bg-base-200 rounded mb-1 animate-pulse w-3/4" />
      <div className="h-4 bg-base-200 rounded animate-pulse w-1/2" />
    </div>
  );
}

export default function FeaturedProducts({ products, name = 'Featured' }: FeaturedProductsProps) {
  // Show skeleton UI while loading (products is undefined)
  if (products === undefined) {
    return (
      <section className="min-h-[400px] bg-base-100 px-4 py-16">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-base-content uppercase tracking-tight mb-12">
            {name}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[...Array(4)].map((_, index) => (
              <ProductSkeleton key={index} />
            ))}
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
    <section className="min-h-[400px] bg-base-100 px-4 py-16">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-semibold text-base-content uppercase tracking-tight mb-12">
          {name}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {products.map((product) => (
            <ProductItem key={product.id} product={product} />
          ))}
        </div>
      </div>
    </section>
  );
}

