'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { Product } from '@/types/product';

interface ProductItemProps {
  product: Product;
}

export default function ProductItem({ product }: ProductItemProps) {
  const [colorMode, setColorMode] = useState(false);

  useEffect(() => {
    // Check for color-mode attribute on html element
    const htmlElement = document.documentElement;
    const colorModeValue = htmlElement.getAttribute('data-color-mode');
    setColorMode(colorModeValue === 'true');

    // Watch for changes to the attribute
    const observer = new MutationObserver(() => {
      const value = htmlElement.getAttribute('data-color-mode');
      setColorMode(value === 'true');
    });

    observer.observe(htmlElement, {
      attributes: true,
      attributeFilter: ['data-color-mode'],
    });

    return () => observer.disconnect();
  }, []);

  return (
    <Link href={`/shop/products/${product.id}`}
      className={`flex flex-col group cursor-pointer transition-all duration-300 ${
        colorMode
          ? 'hover:bg-secondary hover:border-2 hover:border-accent radius-theme p-4 border-2 border-transparent'
          : 'hover:border-2 hover:border-base-300 radius-theme p-4 border-2 border-transparent'
      }`}
    >
      <div className="relative w-full aspect-square mb-4 overflow-hidden radius-theme bg-base-200">
        <Image
          src={product.images[0]}
          alt={product.name}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, 33vw"
        />
      </div>
      <h3 className={`text-base-content font-medium text-base mb-1 tracking-wide ${colorMode ? 'group-hover:text-secondary-content' : ''}`}>
        {product.name}
      </h3>
      <p className={`text-base-content/60 text-sm ${colorMode ? 'group-hover:text-secondary-content' : ''}`}>
        ${product.price.toFixed(2)}
      </p>
    </Link>
  );
}



