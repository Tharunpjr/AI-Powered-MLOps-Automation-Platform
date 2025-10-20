"use client";

import { useState } from "react";
import Navigation from "@/components/Navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import {
  BookOpen,
  Search,
  Code,
  Zap,
  Shield,
  Settings,
  FileText,
  Terminal,
  Menu,
  ChevronRight,
  ExternalLink,
} from "lucide-react";

export default function DocsPage() {
  const [activeSection, setActiveSection] = useState("getting-started");
  const [isMobileNavOpen, setIsMobileNavOpen] = useState(false);

  const sections = [
    {
      id: "getting-started",
      title: "Getting Started",
      icon: Zap,
      items: [
        { id: "introduction", title: "Introduction" },
        { id: "quick-start", title: "Quick Start" },
        { id: "installation", title: "Installation" },
      ],
    },
    {
      id: "api",
      title: "API Reference",
      icon: Code,
      items: [
        { id: "authentication", title: "Authentication" },
        { id: "endpoints", title: "API Endpoints" },
        { id: "rate-limits", title: "Rate Limits" },
      ],
    },
    {
      id: "models",
      title: "Model Management",
      icon: Settings,
      items: [
        { id: "deployment", title: "Deployment" },
        { id: "versioning", title: "Versioning" },
        { id: "monitoring", title: "Monitoring" },
      ],
    },
    {
      id: "security",
      title: "Security",
      icon: Shield,
      items: [
        { id: "best-practices", title: "Best Practices" },
        { id: "compliance", title: "Compliance" },
      ],
    },
  ];

  const content = {
    "getting-started": {
      title: "Getting Started with AutoOps",
      description: "Learn how to deploy your first ML model in minutes",
      content: `
# Getting Started

Welcome to AutoOps! This guide will help you deploy your first machine learning model in just a few minutes.

## Prerequisites

Before you begin, make sure you have:
- Python 3.8 or higher installed
- An AutoOps account (sign up for free)
- Your API key from the dashboard

## Quick Start

1. Install the AutoOps CLI:

\`\`\`bash
pip install autoops-cli
\`\`\`

2. Configure your API key:

\`\`\`bash
autoops config set-key YOUR_API_KEY
\`\`\`

3. Deploy your first model:

\`\`\`python
from autoops import AutoOps

# Initialize client
client = AutoOps(api_key="YOUR_API_KEY")

# Deploy model
deployment = client.deploy_model(
    model_path="model.pkl",
    name="my-first-model",
    framework="scikit-learn"
)

print(f"Model deployed: {deployment.url}")
\`\`\`

## Next Steps

- Explore the [Dashboard](/dashboard) to monitor your models
- Try the [Playground](/playground) to test different configurations
- Read the [API Reference](#api) for advanced usage
      `,
    },
    "authentication": {
      title: "Authentication",
      description: "Secure your API requests with proper authentication",
      content: `
# Authentication

AutoOps uses API keys to authenticate requests. Your API keys carry many privileges, so keep them secure!

## Getting Your API Key

1. Log in to your AutoOps dashboard
2. Navigate to Settings > API Keys
3. Click "Create New Key"
4. Copy and store your key securely

## Using API Keys

Include your API key in the Authorization header:

\`\`\`bash
curl https://api.autoops.ai/v1/models \\
  -H "Authorization: Bearer YOUR_API_KEY"
\`\`\`

## Best Practices

- **Never commit API keys** to version control
- **Use environment variables** to store keys
- **Rotate keys regularly** for enhanced security
- **Use different keys** for development and production

## Example: Python

\`\`\`python
import os
from autoops import AutoOps

# Load from environment variable
api_key = os.environ.get("AUTOOPS_API_KEY")
client = AutoOps(api_key=api_key)
\`\`\`
      `,
    },
    "deployment": {
      title: "Model Deployment",
      description: "Deploy and manage your ML models at scale",
      content: `
# Model Deployment

Deploy your machine learning models with zero downtime and automatic scaling.

## Supported Frameworks

AutoOps supports all major ML frameworks:
- scikit-learn
- TensorFlow
- PyTorch
- XGBoost
- LightGBM
- And more...

## Deployment Options

### Option 1: CLI Deployment

\`\`\`bash
autoops deploy \\
  --model model.pkl \\
  --name production-model \\
  --framework sklearn \\
  --instance-type standard
\`\`\`

### Option 2: Python SDK

\`\`\`python
from autoops import AutoOps

client = AutoOps(api_key="YOUR_API_KEY")

deployment = client.deploy_model(
    model_path="model.pkl",
    name="production-model",
    framework="sklearn",
    config={
        "min_instances": 2,
        "max_instances": 10,
        "cpu": "2",
        "memory": "4Gi"
    }
)
\`\`\`

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| min_instances | Minimum number of instances | 1 |
| max_instances | Maximum number of instances | 5 |
| cpu | CPU cores per instance | 1 |
| memory | Memory per instance | 2Gi |

## Monitoring

After deployment, monitor your model's performance in real-time through the dashboard.
      `,
    },
  };

  const currentContent = content[activeSection as keyof typeof content] || content["getting-started"];

  const SidebarContent = () => (
    <div className="space-y-6">
      <div className="px-4 lg:px-0">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input placeholder="Search docs..." className="pl-9" />
        </div>
      </div>

      <nav className="space-y-4 px-4 lg:px-0">
        {sections.map((section) => {
          const Icon = section.icon;
          return (
            <div key={section.id}>
              <div className="flex items-center gap-2 text-sm font-semibold mb-2 text-foreground">
                <Icon className="w-4 h-4" />
                {section.title}
              </div>
              <div className="ml-6 space-y-1">
                {section.items.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => {
                      setActiveSection(item.id);
                      setIsMobileNavOpen(false);
                    }}
                    className={`block w-full text-left text-sm py-2 px-3 rounded-md transition-colors ${
                      activeSection === item.id
                        ? "bg-primary/10 text-primary font-medium"
                        : "text-muted-foreground hover:text-foreground hover:bg-accent"
                    }`}
                  >
                    {item.title}
                  </button>
                ))}
              </div>
            </div>
          );
        })}
      </nav>
    </div>
  );

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <main className="pt-16 md:pt-20 pb-20 md:pb-8 px-4">
        <div className="container mx-auto max-w-7xl py-6 md:py-8">
          {/* Header */}
          <div className="mb-6 md:mb-8">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-muted rounded-xl flex items-center justify-center">
                  <BookOpen className="w-5 h-5 text-muted-foreground" />
                </div>
                <div>
                  <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">Documentation</h1>
                  <p className="text-sm md:text-base text-muted-foreground hidden sm:block">
                    Everything you need to know about AutoOps
                  </p>
                </div>
              </div>

              {/* Mobile Menu Button */}
              <Sheet open={isMobileNavOpen} onOpenChange={setIsMobileNavOpen}>
                <SheetTrigger asChild className="lg:hidden">
                  <Button variant="outline" size="icon">
                    <Menu className="w-5 h-5" />
                  </Button>
                </SheetTrigger>
                <SheetContent side="left" className="w-[280px] sm:w-[320px]">
                  <div className="mt-8">
                    <SidebarContent />
                  </div>
                </SheetContent>
              </Sheet>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Desktop Sidebar */}
            <div className="hidden lg:block lg:col-span-3">
              <div className="sticky top-24">
                <SidebarContent />
              </div>
            </div>

            {/* Main Content */}
            <div className="lg:col-span-9">
              <Card className="p-6 md:p-8 lg:p-10 bg-card/50 backdrop-blur border-border/50">
                {/* Breadcrumb */}
                <div className="flex items-center gap-2 text-sm text-muted-foreground mb-6">
                  <span>Docs</span>
                  <ChevronRight className="w-4 h-4" />
                  <span className="text-foreground font-medium">{currentContent.title}</span>
                </div>

                {/* Content Header */}
                <div className="mb-8">
                  <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold mb-3">
                    {currentContent.title}
                  </h1>
                  <p className="text-base md:text-lg text-muted-foreground">
                    {currentContent.description}
                  </p>
                </div>

                {/* Content Body */}
                <div className="prose prose-slate dark:prose-invert max-w-none">
                  <div className="space-y-6">
                    {currentContent.content.split('\n\n').map((paragraph, index) => {
                      if (paragraph.startsWith('#')) {
                        const level = paragraph.match(/^#+/)?.[0].length || 1;
                        const text = paragraph.replace(/^#+\s*/, '');
                        const HeadingTag = `h${level}` as keyof JSX.IntrinsicElements;
                        return (
                          <HeadingTag key={index} className="font-bold text-foreground">
                            {text}
                          </HeadingTag>
                        );
                      } else if (paragraph.startsWith('```')) {
                        const code = paragraph.replace(/```\w*\n?/g, '').trim();
                        return (
                          <Card key={index} className="p-4 bg-muted/50 border-border/50">
                            <pre className="text-sm overflow-x-auto">
                              <code className="text-foreground font-mono">{code}</code>
                            </pre>
                          </Card>
                        );
                      } else if (paragraph.startsWith('|')) {
                        // Simple table rendering
                        const rows = paragraph.split('\n');
                        return (
                          <div key={index} className="overflow-x-auto">
                            <table className="w-full text-sm border-collapse">
                              <tbody>
                                {rows.map((row, rowIndex) => {
                                  if (row.includes('---')) return null;
                                  const cells = row.split('|').filter(cell => cell.trim());
                                  return (
                                    <tr key={rowIndex} className={rowIndex === 0 ? 'border-b-2' : 'border-b'}>
                                      {cells.map((cell, cellIndex) => (
                                        <td key={cellIndex} className="px-4 py-2">
                                          {cell.trim()}
                                        </td>
                                      ))}
                                    </tr>
                                  );
                                })}
                              </tbody>
                            </table>
                          </div>
                        );
                      } else if (paragraph.startsWith('-')) {
                        const items = paragraph.split('\n').filter(line => line.trim());
                        return (
                          <ul key={index} className="space-y-2 list-disc list-inside">
                            {items.map((item, itemIndex) => (
                              <li key={itemIndex} className="text-muted-foreground">
                                {item.replace(/^-\s*/, '')}
                              </li>
                            ))}
                          </ul>
                        );
                      } else if (paragraph.trim()) {
                        return (
                          <p key={index} className="text-muted-foreground leading-relaxed">
                            {paragraph}
                          </p>
                        );
                      }
                      return null;
                    })}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-col sm:flex-row gap-3 mt-8 pt-8 border-t border-border">
                  <Button variant="outline" className="flex-1">
                    <Terminal className="w-4 h-4 mr-2" />
                    View Code Examples
                  </Button>
                  <Button variant="outline" className="flex-1">
                    <ExternalLink className="w-4 h-4 mr-2" />
                    API Reference
                  </Button>
                </div>
              </Card>

              {/* Help Card */}
              <Card className="mt-6 p-6 bg-muted/30 border-border backdrop-blur">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 bg-muted rounded-xl flex items-center justify-center flex-shrink-0">
                    <FileText className="w-5 h-5 text-muted-foreground" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-lg font-semibold mb-2">Need Help?</h3>
                    <p className="text-sm text-muted-foreground mb-4">
                      Can't find what you're looking for? Our support team is here to help.
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <Badge variant="secondary" className="cursor-pointer">
                        Community Forum
                      </Badge>
                      <Badge variant="secondary" className="cursor-pointer">
                        Contact Support
                      </Badge>
                      <Badge variant="secondary" className="cursor-pointer">
                        Video Tutorials
                      </Badge>
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}