"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, X, Cpu, Home, LayoutDashboard, Code, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false);

  const navLinks = [
    { href: "/", label: "Home", icon: Home },
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/playground", label: "Playground", icon: Code },
    { href: "/docs", label: "Docs", icon: FileText },
  ];

  return (
    <>
      {/* Desktop Navigation */}
      <nav className="hidden md:flex fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 text-xl font-bold">
            <div className="w-8 h-8 bg-muted rounded-lg flex items-center justify-center">
              <Cpu className="w-5 h-5 text-muted-foreground" />
            </div>
            AutoOps
          </Link>

          <div className="flex items-center gap-6">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm">
              Sign In
            </Button>
            <Button size="sm">
              Get Started
            </Button>
          </div>
        </div>
      </nav>

      {/* Mobile Top Navigation */}
      <nav className="md:hidden fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 h-14 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 text-lg font-bold">
            <div className="w-7 h-7 bg-muted rounded-lg flex items-center justify-center">
              <Cpu className="w-4 h-4 text-muted-foreground" />
            </div>
            AutoOps
          </Link>

          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon">
                <Menu className="w-5 h-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-[280px] sm:w-[320px]">
              <div className="flex flex-col gap-4 mt-8">
                {navLinks.map((link) => {
                  const Icon = link.icon;
                  return (
                    <Link
                      key={link.href}
                      href={link.href}
                      onClick={() => setIsOpen(false)}
                      className="flex items-center gap-3 text-base font-medium text-foreground hover:text-primary transition-colors p-3 rounded-lg hover:bg-accent"
                    >
                      <Icon className="w-5 h-5" />
                      {link.label}
                    </Link>
                  );
                })}
                <div className="flex flex-col gap-2 mt-6 pt-6 border-t border-border">
                  <Button variant="outline" className="w-full">
                    Sign In
                  </Button>
                  <Button className="w-full">
                    Get Started
                  </Button>
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </nav>

      {/* Mobile Bottom Navigation */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-lg border-t border-border">
        <div className="grid grid-cols-4 h-16">
          {navLinks.map((link) => {
            const Icon = link.icon;
            return (
              <Link
                key={link.href}
                href={link.href}
                className="flex flex-col items-center justify-center gap-1 text-muted-foreground hover:text-foreground transition-colors"
              >
                <Icon className="w-5 h-5" />
                <span className="text-xs font-medium">{link.label}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </>
  );
}