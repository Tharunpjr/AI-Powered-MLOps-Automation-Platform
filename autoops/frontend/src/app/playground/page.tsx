"use client";

import { useState } from "react";
import Navigation from "@/components/Navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import {
  Play,
  Code,
  Sparkles,
  Brain,
  Image as ImageIcon,
  FileText,
  Settings,
} from "lucide-react";

export default function PlaygroundPage() {
  const [selectedModel, setSelectedModel] = useState("gpt-4");
  const [temperature, setTemperature] = useState([0.7]);
  const [maxTokens, setMaxTokens] = useState([2048]);
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");

  const models = [
    { value: "gpt-4", label: "GPT-4", type: "Text Generation" },
    { value: "claude-3", label: "Claude 3", type: "Text Generation" },
    { value: "llama-2", label: "LLaMA 2", type: "Text Generation" },
    { value: "stable-diffusion", label: "Stable Diffusion", type: "Image Generation" },
    { value: "whisper", label: "Whisper", type: "Speech Recognition" },
  ];

  const examples = [
    {
      title: "Text Summarization",
      prompt: "Summarize the following text in 3 bullet points:\n\nMachine learning operations (MLOps) is a set of practices that aims to deploy and maintain machine learning models in production reliably and efficiently...",
    },
    {
      title: "Code Generation",
      prompt: "Write a Python function that trains a simple neural network using PyTorch for binary classification.",
    },
    {
      title: "Sentiment Analysis",
      prompt: "Analyze the sentiment of this review: 'This product exceeded my expectations! The quality is outstanding and delivery was fast.'",
    },
  ];

  const handleRun = () => {
    setOutputText(`Model: ${selectedModel}\nTemperature: ${temperature[0]}\nMax Tokens: ${maxTokens[0]}\n\n[Demo Output]\nThis is a simulated response from the ${selectedModel} model. In production, this would show the actual model output based on your input and configuration.`);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <main className="pt-16 md:pt-20 pb-20 md:pb-8 px-4">
        <div className="container mx-auto max-w-7xl py-6 md:py-8">
          {/* Header */}
          <div className="mb-6 md:mb-8">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-muted rounded-xl flex items-center justify-center">
                <Code className="w-5 h-5 text-muted-foreground" />
              </div>
              <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">Playground</h1>
            </div>
            <p className="text-sm md:text-base text-muted-foreground">Experiment with AI models in real-time</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Settings Sidebar - Desktop */}
            <div className="hidden lg:block lg:col-span-3 space-y-6">
              <Card className="p-6 bg-card/50 backdrop-blur border-border/50 sticky top-24">
                <div className="flex items-center gap-2 mb-6">
                  <Settings className="w-5 h-5 text-muted-foreground" />
                  <h2 className="text-lg font-semibold">Configuration</h2>
                </div>

                <div className="space-y-6">
                  <div>
                    <label className="text-sm font-medium mb-2 block">Model</label>
                    <Select value={selectedModel} onValueChange={setSelectedModel}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {models.map((model) => (
                          <SelectItem key={model.value} value={model.value}>
                            <div className="flex flex-col">
                              <span className="font-medium">{model.label}</span>
                              <span className="text-xs text-muted-foreground">{model.type}</span>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <label className="text-sm font-medium">Temperature</label>
                      <span className="text-sm text-muted-foreground">{temperature[0]}</span>
                    </div>
                    <Slider
                      value={temperature}
                      onValueChange={setTemperature}
                      min={0}
                      max={2}
                      step={0.1}
                      className="w-full"
                    />
                    <p className="text-xs text-muted-foreground mt-1">Controls randomness in output</p>
                  </div>

                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <label className="text-sm font-medium">Max Tokens</label>
                      <span className="text-sm text-muted-foreground">{maxTokens[0]}</span>
                    </div>
                    <Slider
                      value={maxTokens}
                      onValueChange={setMaxTokens}
                      min={256}
                      max={4096}
                      step={256}
                      className="w-full"
                    />
                    <p className="text-xs text-muted-foreground mt-1">Maximum output length</p>
                  </div>

                  <div className="pt-4 border-t border-border">
                    <h3 className="text-sm font-medium mb-3">Quick Examples</h3>
                    <div className="space-y-2">
                      {examples.map((example, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          className="w-full justify-start text-left h-auto py-2"
                          onClick={() => setInputText(example.prompt)}
                        >
                          <Sparkles className="w-4 h-4 mr-2 flex-shrink-0 text-muted-foreground" />
                          <span className="text-sm truncate">{example.title}</span>
                        </Button>
                      ))}
                    </div>
                  </div>
                </div>
              </Card>
            </div>

            {/* Main Content */}
            <div className="lg:col-span-9 space-y-6">
              {/* Mobile Settings */}
              <Card className="lg:hidden p-4 bg-card/50 backdrop-blur border-border/50">
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium mb-2 block">Model</label>
                    <Select value={selectedModel} onValueChange={setSelectedModel}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {models.map((model) => (
                          <SelectItem key={model.value} value={model.value}>
                            {model.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium mb-2 block">Temperature</label>
                      <Badge variant="secondary">{temperature[0]}</Badge>
                    </div>
                    <div>
                      <label className="text-sm font-medium mb-2 block">Max Tokens</label>
                      <Badge variant="secondary">{maxTokens[0]}</Badge>
                    </div>
                  </div>
                </div>
              </Card>

              {/* Input/Output Area */}
              <Card className="p-4 md:p-6 bg-card/50 backdrop-blur border-border/50">
                <Tabs defaultValue="input" className="space-y-4">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="input" className="flex items-center gap-2">
                      <FileText className="w-4 h-4" />
                      Input
                    </TabsTrigger>
                    <TabsTrigger value="output" className="flex items-center gap-2">
                      <Brain className="w-4 h-4" />
                      Output
                    </TabsTrigger>
                  </TabsList>

                  <TabsContent value="input" className="space-y-4">
                    <Textarea
                      placeholder="Enter your prompt or input data here..."
                      className="min-h-[300px] md:min-h-[400px] resize-none font-mono text-sm"
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                    />
                    <Button
                      onClick={handleRun}
                      className="w-full"
                      size="lg"
                    >
                      <Play className="w-4 h-4 mr-2" />
                      Run Model
                    </Button>
                  </TabsContent>

                  <TabsContent value="output" className="space-y-4">
                    <div className="min-h-[300px] md:min-h-[400px] p-4 bg-background/50 rounded-lg border border-border/50 font-mono text-sm whitespace-pre-wrap">
                      {outputText || "Output will appear here after running the model..."}
                    </div>
                    {outputText && (
                      <Button variant="outline" className="w-full">
                        <Code className="w-4 h-4 mr-2" />
                        Copy Output
                      </Button>
                    )}
                  </TabsContent>
                </Tabs>
              </Card>

              {/* Quick Actions - Mobile Only */}
              <div className="lg:hidden">
                <h3 className="text-sm font-medium mb-3">Quick Examples</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {examples.map((example, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      className="justify-start text-left h-auto py-3"
                      onClick={() => setInputText(example.prompt)}
                    >
                      <Sparkles className="w-4 h-4 mr-2 flex-shrink-0 text-muted-foreground" />
                      <span className="text-sm">{example.title}</span>
                    </Button>
                  ))}
                </div>
              </div>

              {/* Model Info */}
              <Card className="p-4 md:p-6 bg-muted/30 border-border backdrop-blur">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 bg-muted rounded-xl flex items-center justify-center flex-shrink-0">
                    <Brain className="w-5 h-5 text-muted-foreground" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-lg font-semibold mb-2">About {models.find(m => m.value === selectedModel)?.label}</h3>
                    <p className="text-sm text-muted-foreground">
                      This model is optimized for {models.find(m => m.value === selectedModel)?.type.toLowerCase()} tasks. 
                      Adjust the temperature and token settings to fine-tune the output based on your needs.
                    </p>
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