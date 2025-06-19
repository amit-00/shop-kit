"use client"

import { TProduct } from "../hooks/types";
import Product from "./Product";

function Shop({
    products
}: { products: TProduct[] }) {
    return (
        <section className="py-8 sm:py-12">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-8">Our Products</h2>

                {products.length === 0 ? (
                    <div className="text-center py-12">
                    <p className="text-gray-500">No products found matching your search.</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {products.map((product) => (
                        <Product key={product.id} product={product} />
                    ))}
                    </div>
                )}
            </div>
        </section>
    )
}

export default Shop;