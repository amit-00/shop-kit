'use client';

import { useState } from 'react';
import CartBadge from './CartBadge';

export default function Header({ name }: { name: string }) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen((prev) => !prev);
  };

  return (
    <>
      <header className="border-t border-b border-base-300 bg-base-100 py-4">
        <div className="max-w-6xl mx-auto px-8 flex items-center justify-between md:px-4">
          <div className="font-semibold text-2xl text-base-content uppercase tracking-wide">
            MINIMAL
          </div>
          <nav className="hidden md:flex gap-8 items-center">
            <a
              href="/shop"
              className="text-base-content/60 hover:text-base-content transition-colors text-sm font-semibold no-underline"
            >
              Shop
            </a>
            <a
              href="/collections"
              className="text-base-content/60 hover:text-base-content transition-colors text-sm font-semibold no-underline"
            >
              Collections
            </a>
            <a
              href="/about"
              className="text-base-content/60 hover:text-base-content transition-colors text-sm font-semibold no-underline"
            >
              About
            </a>
          </nav>
          <div className="flex gap-4 items-center">
            <CartBadge />
            <button
              id="mobile-menu-button"
              className="md:hidden bg-transparent border-none cursor-pointer p-2 flex items-center justify-center"
              aria-label="Menu"
              aria-expanded={isMobileMenuOpen}
              onClick={toggleMobileMenu}
            >
              {isMobileMenuOpen ? (
                <svg
                  id="close-icon"
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
              ) : (
                <svg
                  id="menu-icon"
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
                    d="M4 6h16M4 12h16M4 18h16"
                  ></path>
                </svg>
              )}
            </button>
          </div>
        </div>
      </header>
      {isMobileMenuOpen && (
        <nav
          id="mobile-menu"
          className="md:hidden border-t border-base-300 bg-base-100 py-4"
        >
          <div className="max-w-6xl mx-auto px-8 md:px-4 flex flex-col gap-4">
            <a
              href="/shop"
              className="text-base-content/60 hover:text-base-content transition-colors text-sm no-underline"
            >
              Shop
            </a>
            <a
              href="/collections"
              className="text-base-content/60 hover:text-base-content transition-colors text-sm no-underline"
            >
              Collections
            </a>
            <a
              href="/about"
              className="text-base-content/60 hover:text-base-content transition-colors text-sm no-underline"
            >
              About
            </a>
          </div>
        </nav>
      )}
    </>
  );
}

