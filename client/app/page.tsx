import FeaturedProducts from "@/components/FeaturedProducts";
import { mockCatalogs } from "@/lib/mockData";

export default function Home() {
  const featuredProducts = mockCatalogs['featured']?.products || [];
  
  return (
    <div className="">
      <FeaturedProducts products={featuredProducts} name="Featured" />
    </div>
  );
}
