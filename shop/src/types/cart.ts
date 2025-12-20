export interface CartItem {
  id: string;
  title: string;
  image: string;
  price: number;
  quantity: number;
}

export type Cart = Record<string, CartItem>;

