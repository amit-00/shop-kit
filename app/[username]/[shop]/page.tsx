import Cart from "./components/Cart";
import Landing from "./components/Landing";
import Shop from "./components/Shop";
import { CartProvider } from "./hooks/CartContext";
// import { notFound } from 'next/navigation';
// import { Metadata } from 'next';

const mockProducts = [
  {
    id: 1,
    name: "Classic White T-Shirt",
    price: 29.99,
    image: "/placeholder.svg?height=300&width=300",
    description: "Comfortable cotton t-shirt perfect for everyday wear",
  },
  {
    id: 2,
    name: "Denim Jeans",
    price: 79.99,
    image: "/placeholder.svg?height=300&width=300",
    description: "Premium denim jeans with a modern fit",
  },
  {
    id: 3,
    name: "Sneakers",
    price: 129.99,
    image: "/placeholder.svg?height=300&width=300",
    description: "Comfortable and stylish sneakers for all occasions",
  },
  {
    id: 4,
    name: "Hoodie",
    price: 59.99,
    image: "/placeholder.svg?height=300&width=300",
    description: "Cozy hoodie perfect for cooler weather",
  },
  {
    id: 5,
    name: "Baseball Cap",
    price: 24.99,
    image: "/placeholder.svg?height=300&width=300",
    description: "Classic baseball cap with adjustable strap",
  },
  {
    id: 6,
    name: "Backpack",
    price: 89.99,
    image: "/placeholder.svg?height=300&width=300",
    description: "Durable backpack with multiple compartments",
  },
]

// export async function generateMetadata({
//   params,
// }: {
//   params: { username: string; shop: string };
// }): Promise<Metadata> {
//   const shop = await getShopByUsernameAndSlug(params.username, params.shop);
//   if (!shop) return { title: 'Shop Not Found' };

//   return {
//     title: shop.name,
//     description: shop.description,
//     openGraph: {
//       images: [shop.logoUrl],
//     },
//   };
// }

export default async function ShopPage({
    params
} : {
    params: { username: string; shop: string }
}) {
    const { shop } = await params;
    return (
        <div className="min-h-screen bg-gray-50">
            <Landing
                shopName={shop}
                description="This is a basic shop description"
                logoUrl="/globe.svg"
                socialLinks={{ facebook: "#", twitter: "#", instagram: "#" }}
            />
            <CartProvider>
                <Cart />
                <Shop products={mockProducts} />
            </CartProvider>
        </div>
    )
}