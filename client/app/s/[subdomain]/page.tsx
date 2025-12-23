import { getShopConfig } from '@/lib/utils';
import Header from '@/components/Header';
import Shop from '@/components/Shop';
import Cart from '@/components/Cart';
import { mockCatalogs, mockFAQs } from '@/lib/mockData';
import Hero from '@/components/Hero';
import FeaturedProducts from '@/components/FeaturedProducts';
import FAQ from '@/components/FAQ';
import ShopPageClient from '@/components/ShopPageClient';

export const dynamic = 'force-dynamic';

export default async function ShopPage({ params }: { params: Promise<{ [key: string]: string | string[] | undefined }> }) {
  const subdomain = (await params).subdomain;
  const config = await getShopConfig(subdomain as string);

  return (
    <>
      <Cart />
      <Header name={config.name} />
      <main>
        <Hero />
        <FeaturedProducts products={mockCatalogs['featured']?.products} name="Featured" />
        <FeaturedProducts products={mockCatalogs['featured']?.products.slice(0, 4)} name="Popular" />
        <Shop catalogs={mockCatalogs} />
        <FAQ faqs={mockFAQs} />
      </main>
    </>
  );
}