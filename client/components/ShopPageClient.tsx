'use client';

import { ProductProvider } from '../stores/productStore';
import { CartProvider } from '../stores/cartStore';
import ProductDetails from './ProductDetails';

export default function ShopPageClient({ 
  children, 
  shopSlug 
}: { 
  children: React.ReactNode;
  shopSlug: string;
}) {
  return (
    <CartProvider shopSlug={shopSlug}>
      <ProductProvider>
        {children}
        <ProductDetails />
      </ProductProvider>
    </CartProvider>
  );
}

