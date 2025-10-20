"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export default function DebugPage() {
  const [results, setResults] = useState<any>({});
  const [loading, setLoading] = useState(false);

  const testAPI = async () => {
    setLoading(true);
    const testResults: any = {};

    try {
      // Test health
      console.log("Testing health...");
      const health = await api.healthCheck();
      testResults.health = { success: true, data: health };
      console.log("Health result:", health);
    } catch (error) {
      console.error("Health error:", error);
      testResults.health = { success: false, error: error.message };
    }

    try {
      // Test prediction
      console.log("Testing prediction...");
      const prediction = await api.predict([5.1, 3.5, 1.4, 0.2]);
      testResults.prediction = { success: true, data: prediction };
      console.log("Prediction result:", prediction);
    } catch (error) {
      console.error("Prediction error:", error);
      testResults.prediction = { success: false, error: error.message };
    }

    try {
      // Test chat
      console.log("Testing chat...");
      const chat = await api.chat("Hello!", "debug-session", []);
      testResults.chat = { success: true, data: chat };
      console.log("Chat result:", chat);
    } catch (error) {
      console.error("Chat error:", error);
      testResults.chat = { success: false, error: error.message };
    }

    try {
      // Test analysis
      console.log("Testing analysis...");
      const analysis = await api.analyzeText("This is great!", "sentiment");
      testResults.analysis = { success: true, data: analysis };
      console.log("Analysis result:", analysis);
    } catch (error) {
      console.error("Analysis error:", error);
      testResults.analysis = { success: false, error: error.message };
    }

    setResults(testResults);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">API Debug Page</h1>
        
        <button
          onClick={testAPI}
          disabled={loading}
          className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 disabled:opacity-50 mb-8"
        >
          {loading ? "Testing APIs..." : "Test All APIs"}
        </button>

        <div className="space-y-6">
          {Object.entries(results).map(([key, result]: [string, any]) => (
            <div key={key} className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-xl font-semibold mb-4 capitalize">{key} Test</h2>
              {result.success ? (
                <div>
                  <p className="text-green-600 font-medium mb-2">✅ Success</p>
                  <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto">
                    {JSON.stringify(result.data, null, 2)}
                  </pre>
                </div>
              ) : (
                <div>
                  <p className="text-red-600 font-medium mb-2">❌ Failed</p>
                  <p className="text-red-600">{result.error}</p>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-8 bg-yellow-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold mb-2">Debug Info</h3>
          <p><strong>API Base URL:</strong> {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002'}</p>
          <p><strong>Current URL:</strong> {typeof window !== 'undefined' ? window.location.href : 'Server-side'}</p>
        </div>
      </div>
    </div>
  );
}