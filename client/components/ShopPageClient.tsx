'use client';

import { CartProvider } from '../stores/cartStore';
import { ProductPageProvider } from '../stores/productPageStore';

export default function ShopPageClient({ 
  children, 
  shopSlug 
}: { 
  children: React.ReactNode;
  shopSlug: string;
}) {
  return (
    <CartProvider shopSlug={shopSlug}>
        <ProductPageProvider>
          {children}
        </ProductPageProvider>
    </CartProvider>
  );
}

