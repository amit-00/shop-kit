"use client"

import {  ShoppingCart } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import CartItem from "./CartItem"
import { useCart } from "../hooks"
import { TCartItem } from "../hooks/types"

function Cart() {
    const cart = useCart();

    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button variant="outline" size="sm" className="absolute top-3 right-3 h-12 w-12">
                    <ShoppingCart className="h-12 w-12" />
                    {cart.getQuantity() > 0 && (
                        <Badge className="absolute -top-2 -right-2 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs">
                            {cart.getQuantity()}
                        </Badge>
                    )}
                </Button>
            </SheetTrigger>
            <SheetContent>
                <SheetHeader>
                    <SheetTitle>Shopping Cart</SheetTitle>
                </SheetHeader>
                <div className="mt-6 px-2">
                    {cart.items.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">Your cart is empty</p>
                    ) : (
                    <>
                        <div className="space-y-4">
                            {cart.items.map((item: TCartItem) => (
                                <CartItem 
                                    id={item.id}
                                    name={item.name}
                                    price={item.price}
                                    quantity={item.quantity}
                                    image={item.image}
                                />
                            ))}
                        </div>
                        <div className="mt-6 pt-6 border-t">
                            <div className="flex justify-between items-center mb-4">
                                <span className="text-lg font-semibold">Total: ${cart.getTotal().toFixed(2)}</span>
                            </div>
                            <Button className="w-full" size="lg">
                                Checkout
                            </Button>
                        </div>
                    </>
                    )}
                </div>
            </SheetContent>
        </Sheet>
    )
}

export default Cart;