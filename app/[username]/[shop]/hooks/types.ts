export type TCartItem = {
  id: number
  name: string
  price: number
  quantity: number
  image: string
}

export type TProduct = {
  id: number
  name: string
  price: number
  image: string
  description: string
}

export type TCartState = {
  items: TCartItem[];
};

export type TCartAction =
  | { type: 'ADD_ITEM'; payload: TCartItem }
  | { type: 'REMOVE_ITEM'; payload: { id: number } }
  | { type: 'UPDATE_QUANTITY'; payload: { id: number; quantity: number } }
  | { type: 'CLEAR_CART' };