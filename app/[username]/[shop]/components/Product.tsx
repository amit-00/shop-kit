"use client"
import { useState } from "react"
import { useCart } from "../hooks"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { TProduct } from "../hooks/types"
import { Button } from "@/components/ui/button"

function Product({ 
    product
} : { product: TProduct }) {
    const [quantity, setQuantity] = useState(1)
    const cart = useCart()

    const handleAddToCart = () => {
        cart.addItem(product, quantity)
        setQuantity(1) // Reset quantity after adding to cart
    }

    return (
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <img src={product.image || "/placeholder.svg"} alt={product.name} className="w-full h-64 object-cover" />
            <div className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{product.name}</h3>
                <p className="text-gray-600 text-sm mb-4">{product.description}</p>
                    <div className="flex items-center justify-between mb-4">
                        <span className="text-2xl font-bold text-gray-900">${product.price.toFixed(2)}</span>
                    </div>

                <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-2">
                        <label htmlFor={`quantity-${product.id}`} className="text-sm font-medium text-gray-700">
                            Qty:
                        </label>
                        <Select value={quantity.toString()} onValueChange={(value) => setQuantity(Number.parseInt(value))}>
                            <SelectTrigger className="w-20">
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                                <SelectItem key={num} value={num.toString()}>
                                    {num}
                                </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>

                    <Button onClick={handleAddToCart} className="flex-1">
                        Add to Cart
                    </Button>
                </div>
            </div>
        </div>
    )
}

export default Product;