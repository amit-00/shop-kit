import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getProductById } from '@/lib/utils';
import ProductImageCarousel from '@/components/ProductImageCarousel';
import ProductQuantitySelector from '@/components/ProductQuantitySelector';
import ProductActions from '@/components/ProductActions';

interface ProductPageProps {
  params: Promise<{ [key: string]: string | string[] | undefined }>;
}

export async function generateMetadata({
  params,
}: ProductPageProps): Promise<Metadata> {
  const resolvedParams = await params;
  const productId = resolvedParams.product as string;
  const product = getProductById(productId);

  if (!product) {
    return {
      title: 'Product Not Found',
    };
  }

  const title = `${product.name} | Shop`;
  const description = product.description || `Shop ${product.name} - $${product.price.toFixed(2)}`;
  const image = product.images && product.images.length > 0 ? product.images[0] : '';

  return {
    title,
    description,
    openGraph: {
      title,
      description,
      images: image ? [{ url: image }] : [],
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: image ? [image] : [],
    },
  };
}

export default async function ProductPage({ params }: ProductPageProps) {
  const resolvedParams = await params;
  const productId = resolvedParams.product as string;
  const product = getProductById(productId);

  if (!product) {
    notFound();
  }

  // Normalize images for structured data
  const images = product.images && product.images.length > 0 ? product.images : [];
  const firstImage = images[0] || '';

  // Generate structured data (JSON-LD)
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: images,
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'USD',
      availability: 'https://schema.org/InStock',
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />
      <section className="min-h-[600px] bg-base-100 py-16">
        <div className="max-w-7xl mx-auto px-8 md:px-4">
          <div className="flex flex-col md:flex-row gap-8 md:gap-12">
            {/* Image Section */}
            <ProductImageCarousel images={images} productName={product.name} />

            {/* Product Info Section */}
            <div className="w-full md:w-1/2 flex flex-col">
              {/* Product Title */}
              <h1 className="text-3xl md:text-4xl font-bold text-base-content uppercase tracking-tight mb-4">
                {product.name}
              </h1>

              {/* Price */}
              <p className="text-2xl md:text-3xl font-semibold text-base-content mb-6">
                ${product.price.toFixed(2)}
              </p>

              {/* Description */}
              {product.description && (
                <div className="mb-8">
                  <p className="text-base-content/80 text-base leading-relaxed">
                    {product.description}
                  </p>
                </div>
              )}

              {/* Quantity Selector */}
              <ProductQuantitySelector />

              {/* Buttons */}
              <ProductActions
                productId={product.id}
                productName={product.name}
                productPrice={product.price}
                productImage={firstImage}
              />
            </div>
          </div>
        </div>
      </section>
    </>
  );
}