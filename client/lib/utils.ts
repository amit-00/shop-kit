import { ShopConfig } from "@/types/tenant";

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

export const protocol =
  process.env.NODE_ENV === 'production' ? 'https' : 'http';
export const rootDomain =
  process.env.NEXT_PUBLIC_ROOT_DOMAIN || 'localhost:3000';