import { Catalog } from '@/types/catalog';

const catalogsArray: Catalog[] = [
  {
    id: 'featured',
    name: 'Featured',
    products: [
      {
        id: '1',
        name: 'Minimalist Watch',
        price: 299.99,
        image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&h=800&fit=crop',
        description: 'Elegant timepiece with clean lines and premium materials. Perfect for everyday wear.',
      },
      {
        id: '2',
        name: 'Modern Desk Lamp',
        price: 149.99,
        image: 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&h=800&fit=crop',
        description: 'Sleek adjustable lamp with LED technology. Ideal for home office or study space.',
      },
      {
        id: '3',
        name: 'Wireless Headphones',
        price: 199.99,
        image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=800&fit=crop',
        description: 'Premium noise-cancelling headphones with exceptional sound quality and comfort.',
      },
      {
        id: '4',
        name: 'Leather Backpack',
        price: 249.99,
        image: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&h=800&fit=crop',
        description: 'Handcrafted genuine leather backpack with multiple compartments. Durable and stylish.',
      },
      {
        id: '5',
        name: 'Ceramic Vase',
        price: 79.99,
        image: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=800&fit=crop',
        description: 'Beautiful hand-glazed ceramic vase perfect for displaying fresh flowers or as standalone decor.',
      },
      {
        id: '6',
        name: 'Wooden Speaker',
        price: 179.99,
        image: 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&h=800&fit=crop',
        description: 'Natural wood Bluetooth speaker with rich, warm sound. Eco-friendly and elegant design.',
      },
    ],
  },
  {
    id: 'new-arrivals',
    name: 'New Arrivals',
    products: [
      {
        id: '7',
        name: 'Smart Notebook',
        price: 39.99,
        image: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&h=800&fit=crop',
        description: 'Reusable notebook that syncs with your digital devices. Write, scan, and organize seamlessly.',
      },
      {
        id: '8',
        name: 'Minimalist Chair',
        price: 399.99,
        image: 'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=800&h=800&fit=crop',
        description: 'Ergonomic design chair with premium materials. Comfortable for long work sessions.',
      },
      {
        id: '9',
        name: 'Glass Water Bottle',
        price: 29.99,
        image: 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=800&h=800&fit=crop',
        description: 'BPA-free glass bottle with silicone sleeve for protection. Keep your drinks pure and fresh.',
      },
      {
        id: '10',
        name: 'Bamboo Cutting Board',
        price: 49.99,
        image: 'https://images.unsplash.com/photo-1556910096-6f5e72db6803?w=800&h=800&fit=crop',
        description: 'Sustainable bamboo cutting board with juice groove. Antibacterial and easy to clean.',
      },
      {
        id: '11',
        name: 'Metal Plant Stand',
        price: 89.99,
        image: 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&h=800&fit=crop',
        description: 'Modern metal stand to elevate your plants. Sleek design that complements any interior.',
      },
      {
        id: '12',
        name: 'Cotton Throw Pillow',
        price: 34.99,
        image: 'https://images.unsplash.com/photo-1584100936595-3c404ed18c0c?w=800&h=800&fit=crop',
        description: 'Soft organic cotton pillow cover. Adds comfort and style to your living space.',
      },
    ],
  },
  {
    id: 'best-sellers',
    name: 'Best Sellers',
    products: [
      {
        id: '13',
        name: 'Minimalist Wallet',
        price: 59.99,
        image: 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&h=800&fit=crop',
        description: 'Slim leather wallet with RFID blocking. Holds cards and cash without bulk.',
      },
      {
        id: '14',
        name: 'Desk Organizer',
        price: 69.99,
        image: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&h=800&fit=crop',
        description: 'Multi-compartment organizer to keep your desk tidy. Perfect for office supplies.',
      },
      {
        id: '15',
        name: 'Reading Glasses',
        price: 99.99,
        image: 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=800&h=800&fit=crop',
        description: 'Stylish reading glasses with blue light filtering. Comfortable frames for extended use.',
      },
      {
        id: '16',
        name: 'Candle Set',
        price: 44.99,
        image: 'https://images.unsplash.com/photo-1602874805363-c4000e0e1a5a?w=800&h=800&fit=crop',
        description: 'Set of three soy candles with natural scents. Long-lasting and eco-friendly.',
      },
      {
        id: '17',
        name: 'Stone Coaster Set',
        price: 24.99,
        image: 'https://images.unsplash.com/photo-1571781926291-c4776fd1fb89?w=800&h=800&fit=crop',
        description: 'Natural stone coasters that protect surfaces. Set of four with elegant design.',
      },
      {
        id: '18',
        name: 'Minimalist Clock',
        price: 129.99,
        image: 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=800&fit=crop',
        description: 'Quiet wall clock with clean design. Battery-operated with precise timekeeping.',
      },
    ],
  },
];

// Convert array to map/object with catalog id as key
export const mockCatalogs: Record<string, Catalog> = catalogsArray.reduce(
  (acc, catalog) => {
    acc[catalog.id] = catalog;
    return acc;
  },
  {} as Record<string, Catalog>
);

