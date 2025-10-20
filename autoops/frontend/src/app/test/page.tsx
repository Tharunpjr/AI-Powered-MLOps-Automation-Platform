"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export default function TestPage() {
  const [results, setResults] = useState<any>({});
  const [loading, setLoading] = useState<any>({});

  const testMLPrediction = async () => {
    setLoading(prev => ({ ...prev, ml: true }));
    try {
      const result1 = await api.predict([1, 1, 1, 1]);
      const result2 = await api.predict([5, 5, 5, 5]);
      const result3 = await api.predict([-1, -1, -1, -1]);
      
      setResults(prev => ({
        ...prev,
        ml: {
          test1: result1,
          test2: result2,
          test3: result3
        }
      }));
    } catch (error) {
      setResults(prev => ({ ...prev, ml: { error: error.message } }));
    } finally {
      setLoading(prev => ({ ...prev, ml: false }));
    }
  };

  const testChat = async () => {
    setLoading(prev => ({ ...prev, chat: true }));
    try {
      const result = await api.chat("Hello, how are you?");
      setResults(prev => ({ ...prev, chat: result }));
    } catch (error) {
      setResults(prev => ({ ...prev, chat: { error: error.message } }));
    } finally {
      setLoading(prev => ({ ...prev, chat: false }));
    }
  };

  const testSentiment = async () => {
    setLoading(prev => ({ ...prev, sentiment: true }));
    try {
      const result1 = await api.analyzeText("This is amazing!", "sentiment");
      const result2 = await api.analyzeText("I hate this", "sentiment");
      const result3 = await api.analyzeText("It's okay", "sentiment");
      
      setResults(prev => ({
        ...prev,
        sentiment: {
          positive: result1,
          negative: result2,
          neutral: result3
        }
      }));
    } catch (error) {
      setResults(prev => ({ ...prev, sentiment: { error: error.message } }));
    } finally {
      setLoading(prev => ({ ...prev, sentiment: false }));
    }
  };

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">API Test Page</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* ML Prediction Test */}
          <div className="border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">ML Prediction Test</h2>
            <button
              onClick={testMLPrediction}
              disabled={loading.ml}
              className="bg-blue-500 text-white px-4 py-2 rounded mb-4 disabled:opacity-50"
            >
              {loading.ml ? "Testing..." : "Test ML Predictions"}
            </button>
            
            {results.ml && (
              <div className="text-sm">
                <pre className="bg-gray-100 p-2 rounded overflow-auto">
                  {JSON.stringify(results.ml, null, 2)}
                </pre>
              </div>
            )}
          </div>

          {/* Chat Test */}
          <div className="border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Chat Test</h2>
            <button
              onClick={testChat}
              disabled={loading.chat}
              className="bg-green-500 text-white px-4 py-2 rounded mb-4 disabled:opacity-50"
            >
              {loading.chat ? "Testing..." : "Test Chat"}
            </button>
            
            {results.chat && (
              <div className="text-sm">
                <pre className="bg-gray-100 p-2 rounded overflow-auto">
                  {JSON.stringify(results.chat, null, 2)}
                </pre>
              </div>
            )}
          </div>

          {/* Sentiment Test */}
          <div className="border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Sentiment Test</h2>
            <button
              onClick={testSentiment}
              disabled={loading.sentiment}
              className="bg-purple-500 text-white px-4 py-2 rounded mb-4 disabled:opacity-50"
            >
              {loading.sentiment ? "Testing..." : "Test Sentiment"}
            </button>
            
            {results.sentiment && (
              <div className="text-sm">
                <pre className="bg-gray-100 p-2 rounded overflow-auto">
                  {JSON.stringify(results.sentiment, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>

        <div className="mt-8">
          <h2 className="text-xl font-semibold mb-4">Backend Status</h2>
          <div className="text-sm">
            <p>Backend URL: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}</p>
            <p>Environment: {process.env.NODE_ENV}</p>
          </div>
        </div>
      </div>
    </div>
  );
}