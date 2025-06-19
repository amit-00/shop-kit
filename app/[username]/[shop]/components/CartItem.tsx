import { Button } from "@/components/ui/button";
import { Minus, Plus, X } from "lucide-react";
import { TCartItem } from "../hooks/types";
import { useCart } from "../hooks";

function CartItem({
    id,
    name,
    price,
    quantity,
    image
} : TCartItem ) {
    const cart = useCart();
    return (
        <div key={id} className="flex items-center space-x-4 bg-gray-100 p-4 rounded-lg">
            <img
                src={image || "/placeholder.svg"}
                alt={name}
                className="w-16 h-16 object-cover rounded"
            />
            <div className="flex-1">
                <h3 className="font-medium text-sm">{name}</h3>
                <p className="text-gray-600 text-sm">${price.toFixed(2)}</p>
                <div className="flex items-center space-x-2 mt-2">
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => cart.updateQuantity(id, quantity - 1)}
                    >
                        <Minus className="h-3 w-3" />
                    </Button>
                    <span className="text-sm font-medium">{quantity}</span>
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => cart.updateQuantity(id, quantity + 1)}
                    >
                        <Plus className="h-3 w-3" />
                    </Button>
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => cart.removeItem(id)}
                        className="ml-auto"
                    >
                        <X className="h-4 w-4" />
                    </Button>
                </div>
            </div>
        </div>
    )
}

export default CartItem;