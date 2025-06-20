import { Facebook, Twitter, Instagram } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link";
import Image from "next/image";

interface SocialLinks {
    twitter: string;
    instagram: string;
    facebook: string;
}

interface LandingComponent {
    logoUrl: string, 
    shopName: string, 
    description: string, 
    socialLinks: SocialLinks
}

function Landing(
    {
        logoUrl, 
        shopName, 
        description, 
        socialLinks 
    }: LandingComponent) {
    return (
        <section className="bg-white py-8 sm:py-12">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                <div className="flex justify-center mb-8 rounded">
                    <Image 
                        src={logoUrl} 
                        alt="Shop Logo"
                        height={100}
                        width={100}
                    />
                </div>
                <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">{shopName}</h2>
                <p className="text-lg text-gray-600 mb-6 max-w-2xl mx-auto">
                    {description}
                </p>

                {/* Social Links */}
                <div className="flex justify-center space-x-4 mb-8">
                    
                    <Button asChild variant="outline" size="sm">
                        <Facebook className="h-4 w-4 mr-2" />
                        <Link href={socialLinks.facebook}>Facebook</Link>
                    </Button>
                    
                    <Button asChild variant="outline" size="sm">
                        <Twitter className="h-4 w-4 mr-2" />
                        <Link href={socialLinks.twitter}>Twitter</Link>
                    </Button>
                    
                    <Button asChild variant="outline" size="sm">
                        <Instagram className="h-4 w-4 mr-2" />
                        <Link href={socialLinks.instagram}>Instagram</Link>
                    </Button>
                </div>
            </div>
        </section>
    )
}

export default Landing;