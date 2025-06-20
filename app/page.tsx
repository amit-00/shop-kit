import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import Navbar from "./components/Navbar";
import { ArrowRight, BarChart3, Check, Clock, Globe, Shield, Star, Users, Zap } from "lucide-react"
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import Footer from "./components/Footer";


export default function ShopKit() {

  return (
    <>
      <Navbar />
      <section className="text-center py-48 max-w-7xl mx-auto">
        <Badge variant="secondary" className="mb-4">
          🚀 New: Analytics Dashboard
        </Badge>
        <div className="text-center w-3xl mx-auto">
          <h1 className="text-6xl font-bold">Turn Your Products Into Profit – Instantly</h1>
          <div className="w-xl mx-auto my-8">
            <p className="font-light text-2xl text-gray-600">Launch a clean, mobile-ready store without the tech headache.</p>
          </div>
        </div>
        <Button asChild size="lg">
          <Link href="/">
            <ArrowRight /> Get Started for Free
          </Link>
        </Button>
      </section>

      <section className="bg-muted/50 py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl md:text-4xl font-bold text-primary">10K+</div>
              <div className="text-muted-foreground">Active Companies</div>
            </div>
            <div>
              <div className="text-3xl md:text-4xl font-bold text-primary">99.9%</div>
              <div className="text-muted-foreground">Uptime</div>
            </div>
            <div>
              <div className="text-3xl md:text-4xl font-bold text-primary">50M+</div>
              <div className="text-muted-foreground">Tasks Automated</div>
            </div>
            <div>
              <div className="text-3xl md:text-4xl font-bold text-primary">24/7</div>
              <div className="text-muted-foreground">Support</div>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Everything you need to succeed</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Powerful features designed to streamline your workflow and accelerate growth
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <Zap className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>Lightning Fast</CardTitle>
              <CardDescription>
                Process thousands of operations per second with our optimized infrastructure
              </CardDescription>
            </CardHeader>
          </Card>
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <Shield className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>Enterprise Security</CardTitle>
              <CardDescription>
                Bank-level encryption and compliance with SOC 2, GDPR, and HIPAA standards
              </CardDescription>
            </CardHeader>
          </Card>
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <BarChart3 className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>Advanced Analytics</CardTitle>
              <CardDescription>Real-time insights and custom dashboards to track your key metrics</CardDescription>
            </CardHeader>
          </Card>
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <Users className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>Team Collaboration</CardTitle>
              <CardDescription>Seamless collaboration tools with role-based permissions and workflows</CardDescription>
            </CardHeader>
          </Card>
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <Globe className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>Global Scale</CardTitle>
              <CardDescription>Deploy worldwide with our global infrastructure and CDN network</CardDescription>
            </CardHeader>
          </Card>
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <Clock className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>24/7 Support</CardTitle>
              <CardDescription>Round-the-clock expert support with dedicated success managers</CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      <section className="bg-muted/50 py-20">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Trusted by industry leaders</h2>
            <p className="text-xl text-muted-foreground">See what our customers have to say about their experience</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
                <p className="text-muted-foreground mb-4">
                  "Shop Kit transformed our operations. We've seen a 300% increase in productivity and our
                  team loves the intuitive interface."
                </p>
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <span className="font-semibold text-primary">JD</span>
                  </div>
                  <div>
                    <div className="font-semibold">John Davis</div>
                    <div className="text-sm text-muted-foreground">CEO, TechCorp</div>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
                <p className="text-muted-foreground mb-4">
                  "The automation features saved us countless hours. The ROI was evident within the first month of
                  implementation."
                </p>
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <span className="font-semibold text-primary">SM</span>
                  </div>
                  <div>
                    <div className="font-semibold">Sarah Miller</div>
                    <div className="text-sm text-muted-foreground">CTO, InnovateLab</div>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
                <p className="text-muted-foreground mb-4">
                  "Outstanding support and reliability. Shop Kit has become an integral part of our daily operations
                  across all departments."
                </p>
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <span className="font-semibold text-primary">MJ</span>
                  </div>
                  <div>
                    <div className="font-semibold">Michael Johnson</div>
                    <div className="text-sm text-muted-foreground">VP Operations, ScaleUp</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      <section id="pricing" className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Simple, transparent pricing</h2>
          <p className="text-xl text-muted-foreground">Choose the perfect plan for your team size and needs</p>
        </div>
        <div className="grid md:grid-cols-2 gap-8 max-w-3xl mx-auto">
          <Card className="border-2">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl">Starter</CardTitle>
              <CardDescription>Perfect for small teams</CardDescription>
              <div className="text-4xl font-bold mt-4">
                $29<span className="text-lg text-muted-foreground">/month</span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Up to 5 team members</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>10GB storage</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Basic analytics</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Email support</span>
                </div>
              </div>
              <Button className="w-full" variant="outline">
                Get Started
              </Button>
            </CardContent>
          </Card>

          <Card className="border-2 border-primary relative">
            <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
              <Badge className="bg-primary text-primary-foreground">Most Popular</Badge>
            </div>
            <CardHeader className="text-center">
              <CardTitle className="text-2xl">Professional</CardTitle>
              <CardDescription>Best for growing businesses</CardDescription>
              <div className="text-4xl font-bold mt-4">
                $99<span className="text-lg text-muted-foreground">/month</span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Up to 25 team members</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>100GB storage</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Advanced analytics</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>Priority support</span>
                </div>
                <div className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-green-500" />
                  <span>API access</span>
                </div>
              </div>
              <Button className="w-full">Get Started</Button>
            </CardContent>
          </Card>
        </div>
      </section>
      <Footer />
    </>
  )
}
