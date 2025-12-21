'use client';

import { ProductProvider } from '../stores/productStore';
import ProductDetails from './ProductDetails';

export default function ShopPageClient({ children }: { children: React.ReactNode }) {
  return (
    <ProductProvider>
      {children}
      <ProductDetails />
    </ProductProvider>
  );
}

