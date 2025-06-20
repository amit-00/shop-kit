function Footer() {
    return (
        <footer id="contact" className="bg-background border-t">
            <div className="max-w-7xl mx-auto px-4 py-16">
            <div className="grid md:grid-cols-4 gap-8">
                <div className="space-y-4">
                    <div className="flex items-center space-x-2">
                        <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
                            <span className="text-primary-foreground font-bold text-lg">S</span>
                        </div>
                        <span className="font-bold text-xl">Shop Kit</span>
                    </div>
                    <p className="text-muted-foreground">Empowering businesses with smart automation and analytics.</p>
                </div>
                <div>
                    <h3 className="font-semibold mb-4">Product</h3>
                    <div className="space-y-2 text-muted-foreground">
                        <div>Features</div>
                        <div>Pricing</div>
                        <div>API</div>
                        <div>Integrations</div>
                    </div>
                </div>
                <div>
                    <h3 className="font-semibold mb-4">Company</h3>
                    <div className="space-y-2 text-muted-foreground">
                        <div>About</div>
                        <div>Blog</div>
                        <div>Careers</div>
                        <div>Contact</div>
                    </div>
                </div>
                <div>
                    <h3 className="font-semibold mb-4">Support</h3>
                    <div className="space-y-2 text-muted-foreground">
                        <div>Help Center</div>
                        <div>Documentation</div>
                        <div>Status</div>
                        <div>Security</div>
                    </div>
                </div>
            </div>
                <div className="border-t mt-12 pt-8 text-center text-muted-foreground">
                    <p>&copy; 2024 Shop Kit. All rights reserved.</p>
                </div>
            </div>
        </footer>
    )
}

export default Footer;