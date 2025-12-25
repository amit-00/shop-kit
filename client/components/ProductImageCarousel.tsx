'use client';

import { useState } from 'react';
import Image from 'next/image';

interface ProductImageCarouselProps {
  images: string[];
  productName: string;
}

export default function ProductImageCarousel({ images, productName }: ProductImageCarouselProps) {
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);

  if (images.length === 0) {
    return null;
  }

  const mainImage = images[selectedImageIndex] || images[0] || '';

  return (
    <div className="w-full md:w-1/2">
      {/* Main Image */}
      <div className="relative w-full aspect-square mb-4 bg-base-200 rounded-lg overflow-hidden">
        {mainImage && (
          <Image
            src={mainImage}
            alt={productName}
            fill
            className="object-cover"
            sizes="(max-width: 768px) 100vw, 50vw"
            priority
          />
        )}
      </div>

      {/* Thumbnail Carousel */}
      {images.length > 1 && (
        <div className="flex gap-2 overflow-x-auto hide-scrollbar">
          {images.map((image, index) => (
            <button
              key={index}
              onClick={() => setSelectedImageIndex(index)}
              className={`relative w-20 h-20 flex-shrink-0 rounded-lg overflow-hidden border-2 transition-all ${
                selectedImageIndex === index
                  ? 'border-base-content'
                  : 'border-base-300 hover:border-base-content/50'
              }`}
              aria-label={`View image ${index + 1}`}
            >
              <Image
                src={image}
                alt={`${productName} - View ${index + 1}`}
                fill
                className="object-cover"
                sizes="80px"
              />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

