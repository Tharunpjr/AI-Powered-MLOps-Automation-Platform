"use client";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Brain,
  Zap,
  Shield,
  TrendingUp,
  Users,
  Clock,
  CheckCircle,
  ArrowRight,
  Cpu,
  BarChart3,
  GitBranch,
  Boxes,
} from "lucide-react";
import Link from "next/link";

export default function LandingPage() {
  const features = [
    {
      icon: Brain,
      title: "AI-Powered Insights",
      description: "Leverage advanced AI models to optimize your ML pipeline and get actionable insights.",
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Deploy and monitor models in seconds with our optimized infrastructure.",
    },
    {
      icon: Shield,
      title: "Enterprise Security",
      description: "Bank-grade security with SOC2 compliance and end-to-end encryption.",
    },
    {
      icon: GitBranch,
      title: "Version Control",
      description: "Track every model version with built-in experiment tracking and rollback.",
    },
    {
      icon: BarChart3,
      title: "Real-time Analytics",
      description: "Monitor model performance with comprehensive dashboards and alerts.",
    },
    {
      icon: Boxes,
      title: "Model Registry",
      description: "Centralized model management with automatic versioning and metadata.",
    },
  ];

  const stats = [
    { value: "10M+", label: "Predictions Daily" },
    { value: "99.9%", label: "Uptime SLA" },
    { value: "500+", label: "Enterprise Clients" },
    { value: "<50ms", label: "Average Latency" },
  ];

  const benefits = [
    "Automated model deployment and monitoring",
    "Real-time performance tracking",
    "A/B testing and experimentation",
    "Custom alerts and notifications",
    "Team collaboration tools",
    "API-first architecture",
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="pt-20 md:pt-32 pb-16 md:pb-24 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center space-y-6 md:space-y-8">
            <Badge className="bg-muted text-muted-foreground border-border">
              <Cpu className="w-3 h-3 mr-1" />
              AI-Powered MLOps Platform
            </Badge>
            
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight">
              <span className="block">Deploy ML Models</span>
              <span className="block bg-gradient-to-r from-purple-500 to-blue-600 bg-clip-text text-transparent">
                At Lightning Speed
              </span>
            </h1>
            
            <p className="text-lg sm:text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              The complete MLOps platform for teams that want to ship faster. 
              Monitor, deploy, and scale ML models with confidence.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Button 
                size="lg" 
                className="w-full sm:w-auto text-base md:text-lg h-12 md:h-14 px-6 md:px-8"
                asChild
              >
                <Link href="/dashboard">
                  Start Free Trial
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="w-full sm:w-auto text-base md:text-lg h-12 md:h-14 px-6 md:px-8"
                asChild
              >
                <Link href="/docs">
                  View Documentation
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 md:py-16 px-4 border-y border-border bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center space-y-2">
                <div className="text-3xl md:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-purple-500 to-blue-600 bg-clip-text text-transparent">
                  {stat.value}
                </div>
                <div className="text-sm md:text-base text-muted-foreground">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 md:py-24 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center space-y-4 mb-12 md:mb-16">
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold">
              Everything You Need
            </h2>
            <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto">
              Powerful features to streamline your ML operations
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card 
                  key={index} 
                  className="p-6 md:p-8 hover:shadow-lg transition-all hover:scale-105 bg-card/50 backdrop-blur border-border/50"
                >
                  <div className="w-12 h-12 bg-muted rounded-xl flex items-center justify-center mb-4">
                    <Icon className="w-6 h-6 text-muted-foreground" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {feature.description}
                  </p>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-16 md:py-24 px-4 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold">
                Why Choose AutoOps?
              </h2>
              <p className="text-lg md:text-xl text-muted-foreground">
                Built for modern ML teams who demand reliability, speed, and scalability.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <span className="text-sm md:text-base">{benefit}</span>
                  </div>
                ))}
              </div>
              <Button 
                size="lg" 
                className="w-full sm:w-auto mt-6"
                asChild
              >
                <Link href="/playground">
                  Try Playground
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
              </Button>
            </div>
            
            <div className="relative">
              <Card className="p-8 md:p-10 bg-muted/30 border-border backdrop-blur">
                <div className="space-y-6">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-muted rounded-full flex items-center justify-center">
                      <TrendingUp className="w-6 h-6 text-muted-foreground" />
                    </div>
                    <div>
                      <div className="text-2xl font-bold">87% Faster</div>
                      <div className="text-sm text-muted-foreground">Model Deployment</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-muted rounded-full flex items-center justify-center">
                      <Users className="w-6 h-6 text-muted-foreground" />
                    </div>
                    <div>
                      <div className="text-2xl font-bold">50K+ Users</div>
                      <div className="text-sm text-muted-foreground">Trusted Worldwide</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-muted rounded-full flex items-center justify-center">
                      <Clock className="w-6 h-6 text-muted-foreground" />
                    </div>
                    <div>
                      <div className="text-2xl font-bold">24/7 Support</div>
                      <div className="text-sm text-muted-foreground">Always Here to Help</div>
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 md:py-24 px-4">
        <div className="container mx-auto max-w-4xl">
          <Card className="p-8 md:p-12 lg:p-16 bg-gradient-to-br from-purple-500 to-blue-600 border-0 text-white text-center">
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 md:mb-6">
              Ready to Transform Your ML Workflow?
            </h2>
            <p className="text-lg md:text-xl text-white/90 mb-6 md:mb-8 max-w-2xl mx-auto">
              Join thousands of teams using AutoOps to deploy and monitor ML models at scale.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button 
                size="lg" 
                variant="secondary" 
                className="w-full sm:w-auto text-base md:text-lg h-12 md:h-14 px-6 md:px-8"
                asChild
              >
                <Link href="/dashboard">
                  Start Free Trial
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="w-full sm:w-auto text-base md:text-lg h-12 md:h-14 px-6 md:px-8 bg-white/10 hover:bg-white/20 text-white border-white/30"
                asChild
              >
                <Link href="/docs">
                  Contact Sales
                </Link>
              </Button>
            </div>
          </Card>
        </div>
      </section>
    </div>
  );
}