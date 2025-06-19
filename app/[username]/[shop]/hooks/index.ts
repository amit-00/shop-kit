import { useCartContext } from './CartContext';
import { TCartItem, TProduct } from './types';

export function useCart() {
  const { state, dispatch } = useCartContext();

  const addItem = (product: TProduct, quantity: number) => {
    const item: TCartItem = {
      id: product.id,
      name: product.name,
      price: product.price,
      quantity: quantity,
      image: product.image
    }
    dispatch({ type: 'ADD_ITEM', payload: item });
  }

  const removeItem = (id: number) =>
    dispatch({ type: 'REMOVE_ITEM', payload: { id } });

  const updateQuantity = (id: number, quantity: number) =>
    dispatch({ type: 'UPDATE_QUANTITY', payload: { id, quantity } });

  const clearCart = () => dispatch({ type: 'CLEAR_CART' });

  const getTotal = () =>
    state.items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const getQuantity = () =>
    state.items.reduce((sum, item) => sum + item.quantity, 0);

  return {
    items: state.items,
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
    getTotal,
    getQuantity,
  };
}
