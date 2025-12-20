import { headers } from 'next/headers';
import { notFound } from 'next/navigation';
import { getTenantConfig } from '@/lib/utils';
import Header from '@/components/Header';
import Shop from '@/components/Shop';
import Cart from '@/components/Cart';
import { mockCatalogs } from '@/lib/mockData';
import Hero from '@/components/Hero';
import FeaturedProducts from '@/components/FeaturedProducts';

export const dynamic = 'force-dynamic';

export default async function ShopPage() {
  const tenant = (await headers()).get("x-tenant-id");

  if (!tenant) notFound();

  const config = await getTenantConfig(tenant);

  return (
    <>
      <Cart />
      <Header name={config.name.toUpperCase()} />
      <main>
        <Hero />
        <FeaturedProducts products={mockCatalogs['featured']?.products.slice(0, 4)} name="Featured" />
        <FeaturedProducts products={mockCatalogs['featured']?.products.slice(0, 4)} name="Popular" />
        <Shop catalogs={mockCatalogs} />
      </main>
    </>
  );
}