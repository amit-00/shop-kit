import { Variant } from "./variant";

export interface Product {
  id: string;
  name: string;
  price: number;
  images: string[];
  description?: string;
  variants?: Record<string, Variant[]>;
}

