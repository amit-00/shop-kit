import { ShopConfig } from "@/types/tenant";
import { Product } from "@/types/product";
import { mockCatalogs } from "./mockData";

const shops: Record<string, ShopConfig> = {
  'minimal': {
    subdomain: 'minimal',
    name: 'Minimal',
    theme: 'light',
  },
  'modern': {
    subdomain: 'modern',
    name: 'Modern',
    theme: 'dark',
  },
  'retro': {
    subdomain: 'retro',
    name: 'Retro',
    theme: 'retro',
  },
}

export async function getShopConfig(subdomain: string): Promise<ShopConfig> {
  return Promise.resolve(shops[subdomain]);
}

export function getProductById(productId: string): Product | null {
  // Search through all catalogs to find the product
  for (const catalog of Object.values(mockCatalogs)) {
    const product = catalog.products.find((p) => p.id === productId);
    if (product) {
      // Normalize product to match Product type (handle image vs images)
      const normalizedProduct: Product = {
        ...product,
        images: 'images' in product && Array.isArray(product.images)
          ? product.images
          : 'image' in product && typeof product.image === 'string'
          ? [product.image]
          : [],
      };
      return normalizedProduct;
    }
  }
  return null;
}

export const protocol =
  process.env.NODE_ENV === 'production' ? 'https' : 'http';
export const rootDomain =
  process.env.NEXT_PUBLIC_ROOT_DOMAIN || 'localhost:3000';