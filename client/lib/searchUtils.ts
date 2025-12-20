import { Product } from '@/types/product';

export interface ProductWithSearchText extends Product {
  searchText: string;
}

export function createSearchText(product: Product): string {
  const name = product.name.toLowerCase();
  const description = (product.description || '').toLowerCase();
  return `${name} ${description}`.trim();
}

export function searchProducts(
  products: ProductWithSearchText[],
  query: string
): ProductWithSearchText[] {
  if (!query.trim()) {
    return products;
  }

  const searchTerms = query
    .toLowerCase()
    .split(/\s+/)
    .filter((term) => term.length > 0);

  if (searchTerms.length === 0) {
    return products;
  }

  const scoredProducts = products
    .map((product) => {
      let score = 0;
      const nameLower = product.name.toLowerCase();
      const descriptionLower = (product.description || '').toLowerCase();

      // Check if all search terms are present (AND logic)
      const allTermsMatch = searchTerms.every((term) => {
        const nameMatch = nameLower.includes(term);
        const descriptionMatch = descriptionLower.includes(term);
        
        if (nameMatch) {
          score += 2; // Title matches worth 2 points
        }
        if (descriptionMatch) {
          score += 1; // Description matches worth 1 point
        }
        
        return nameMatch || descriptionMatch;
      });

      return {
        product,
        score: allTermsMatch ? score : 0,
      };
    })
    .filter((item) => item.score > 0) // Only include products that match all terms
    .sort((a, b) => b.score - a.score) // Sort by score descending
    .map((item) => item.product);

  return scoredProducts;
}


