'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

import CartBadge from './CartBadge';
import SearchBar from './SearchBar';

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
      className={`sticky top-2 md:top-4 z-30 max-w-7xl mx-auto bg-base-100/50 backdrop-blur-md py-4 rounded-box transition-all duration-300 ease-in-out ${
        isScrolled ? 'shadow-sm' : ''
      }`}
    >
      <div className="px-8 md:px-4 flex items-center justify-between">
        <div className="font-semibold text-2xl text-base-content uppercase tracking-wide">
          <Link href="/">{name.toUpperCase()}</Link>
        </div>
        <div className="gap-4 items-center hidden md:flex">
          <Link href="/shop">Shop</Link>
          <SearchBar />
          <CartBadge />
        </div>
        <div className="md:hidden">
          <button className="btn btn-ghost">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-6 h-6">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
}

