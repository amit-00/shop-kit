import { getShopConfig } from '@/lib/utils';
import { mockCatalogs, mockFAQs } from '@/lib/mockData';
import Hero from '@/components/Hero';
import FeaturedProducts from '@/components/FeaturedProducts';
import FAQ from '@/components/FAQ';

export const dynamic = 'force-dynamic';

export default async function HomePage() {

  return (
    <>
      <main>
        <Hero />
        <FeaturedProducts products={mockCatalogs['featured']?.products} name="Featured" />
        <FeaturedProducts products={mockCatalogs['featured']?.products.slice(0, 4)} name="Popular" />
        <FAQ faqs={mockFAQs} />
      </main>
    </>
  );
}