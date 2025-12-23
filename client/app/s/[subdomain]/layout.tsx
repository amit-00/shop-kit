import type { Metadata } from "next";
import "./shop.css";
import { getShopConfig } from "@/lib/utils";
import ShopPageClient from "@/components/ShopPageClient";

export const metadata: Metadata = {
  title: "Shop",
  description: "Shop",
};

export default async function RootLayout({
  children,
  params,
}: Readonly<{
  children: React.ReactNode;
  params: Promise<{ [key: string]: string | string[] | undefined }>;
}>) {
  
  const subdomain = (await params).subdomain;
  const config = await getShopConfig(subdomain as string);

  return (
    <div lang="en" data-theme={config.theme} className="antialiased bg-base-100">
      <ShopPageClient shopSlug={config.name}>
        {children}
      </ShopPageClient>
    </div>
  );
}
