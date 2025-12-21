'use client';

import { useState, useEffect } from 'react';
import CartBadge from './CartBadge';

export default function Header({ name }: { name: string }) {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Check initial scroll position

    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`sticky top-2 md:top-4 z-30 max-w-6xl mx-auto bg-base-100/50 backdrop-blur-md py-4 rounded-box transition-all duration-300 ease-in-out ${
        isScrolled ? 'border border-base-300 shadow-sm' : 'border-transparent'
      }`}
    >
      <div className="px-8 md:px-4 flex items-center justify-between">
        <div className="font-semibold text-2xl text-base-content uppercase tracking-wide">
          MINIMAL
        </div>
        <div className="flex gap-4 items-center">
          <CartBadge />
        </div>
      </div>
    </header>
  );
}

