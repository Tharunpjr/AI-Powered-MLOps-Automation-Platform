"use client";

import { useState, useEffect } from "react";
import Navigation from "@/components/Navigation";
import { api } from "@/lib/api";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("overview");
  const [predictionInput, setPredictionInput] = useState([5.1, 3.5, 1.4, 0.2]);
  const [predictionResult, setPredictionResult] = useState<any>(null);
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState<any[]>([]);
  const [chatSessionId, setChatSessionId] = useState<string>("");
  const [analysisInput, setAnalysisInput] = useState("This is an amazing product!");
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [modelInfo, setModelInfo] = useState<any>(null);
  const [dashboardStats, setDashboardStats] = useState<any>(null);
  const [predictionHistory, setPredictionHistory] = useState<any[]>([]);
  const [analysisHistory, setAnalysisHistory] = useState<any[]>([]);
  const [systemMetrics, setSystemMetrics] = useState<any>(null);
  const [loading, setLoading] = useState<any>({});

  // Load dashboard data on mount
  useEffect(() => {
    loadDashboardData();
    loadModelInfo();
    loadPredictionHistory();
    loadAnalysisHistory();
    loadSystemMetrics();
    // Generate session ID for chat
    setChatSessionId(`session-${Date.now()}`);
  }, []);

  const loadDashboardData = async () => {
    setLoading(prev => ({ ...prev, stats: true }));
    try {
      const stats = await api.request('/api/v1/dashboard/stats');
      setDashboardStats(stats);
    } catch (error) {
      console.error('Failed to load dashboard stats:', error);
    } finally {
      setLoading(prev => ({ ...prev, stats: false }));
    }
  };

  const loadPredictionHistory = async () => {
    try {
      const history = await api.request('/api/v1/predictions?limit=5');
      setPredictionHistory(history.predictions || []);
    } catch (error) {
      console.error('Failed to load prediction history:', error);
    }
  };

  const loadAnalysisHistory = async () => {
    try {
      const history = await api.request('/api/v1/analysis?limit=5');
      setAnalysisHistory(history.analyses || []);
    } catch (error) {
      console.error('Failed to load analysis history:', error);
    }
  };

  const loadSystemMetrics = async () => {
    try {
      const metrics = await api.request('/api/v1/system/metrics?hours=24');
      setSystemMetrics(metrics);
    } catch (error) {
      console.error('Failed to load system metrics:', error);
    }
  };

  const loadModelInfo = async () => {
    try {
      const info = await api.getModelInfo();
      setModelInfo(info);
    } catch (error) {
      console.error('Failed to load model info:', error);
    }
  };

  const handlePredict = async () => {
    setLoading(prev => ({ ...prev, predict: true }));
    try {
      const result = await api.predict(predictionInput);
      setPredictionResult(result);
      // Refresh prediction history
      loadPredictionHistory();
      loadDashboardData(); // Update stats
    } catch (error) {
      console.error('Prediction failed:', error);
    } finally {
      setLoading(prev => ({ ...prev, predict: false }));
    }
  };

  const handleChat = async () => {
    if (!chatInput.trim()) return;
    
    setLoading(prev => ({ ...prev, chat: true }));
    const userMessage = { role: "user", content: chatInput, timestamp: new Date().toISOString() };
    setChatMessages(prev => [...prev, userMessage]);
    setChatInput("");

    try {
      const result = await api.chat(chatInput, chatSessionId, chatMessages);
      const assistantMessage = { 
        role: "assistant", 
        content: result.result, 
        timestamp: new Date().toISOString(),
        processing_time: result.processing_time
      };
      setChatMessages(prev => [...prev, assistantMessage]);
      loadDashboardData(); // Update stats
    } catch (error) {
      console.error('Chat failed:', error);
      const errorMessage = { 
        role: "assistant", 
        content: "Sorry, I encountered an error. Please try again.", 
        timestamp: new Date().toISOString() 
      };
      setChatMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(prev => ({ ...prev, chat: false }));
    }
  };

  const handleAnalysis = async () => {
    if (!analysisInput.trim()) return;
    
    setLoading(prev => ({ ...prev, analysis: true }));
    try {
      const result = await api.analyzeText(analysisInput, "sentiment");
      setAnalysisResult(result);
      // Refresh analysis history
      loadAnalysisHistory();
      loadDashboardData(); // Update stats
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(prev => ({ ...prev, analysis: false }));
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-100';
      case 'negative': return 'text-red-600 bg-red-100';
      case 'neutral': return 'text-gray-600 bg-gray-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">AutoOps Dashboard</h1>
          <p className="text-gray-600">Production MLOps platform with full database integration</p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {[
                { id: "overview", label: "Overview", icon: "📊" },
                { id: "predictions", label: "ML Predictions", icon: "🧠" },
                { id: "chat", label: "AI Chat", icon: "💬" },
                { id: "analysis", label: "Text Analysis", icon: "📝" },
                { id: "history", label: "History", icon: "📈" },
                { id: "system", label: "System", icon: "⚙️" }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? "border-blue-500 text-blue-600"
                      : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                  }`}
                >
                  {tab.icon} {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Overview Tab */}
        {activeTab === "overview" && (
          <div className="space-y-6">
            {/* Stats Cards */}
            {dashboardStats && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="flex items-center">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <span className="text-2xl">🧠</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Total Predictions</p>
                      <p className="text-2xl font-semibold text-gray-900">{dashboardStats.stats.total_predictions}</p>
                      <p className="text-sm text-green-600">+{dashboardStats.stats.today_predictions} today</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="flex items-center">
                    <div className="p-2 bg-green-100 rounded-lg">
                      <span className="text-2xl">💬</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Chat Sessions</p>
                      <p className="text-2xl font-semibold text-gray-900">{dashboardStats.stats.total_chats}</p>
                      <p className="text-sm text-green-600">+{dashboardStats.stats.today_chats} today</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="flex items-center">
                    <div className="p-2 bg-purple-100 rounded-lg">
                      <span className="text-2xl">📝</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Text Analyses</p>
                      <p className="text-2xl font-semibold text-gray-900">{dashboardStats.stats.total_analyses}</p>
                      <p className="text-sm text-green-600">+{dashboardStats.stats.today_analyses} today</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="flex items-center">
                    <div className="p-2 bg-orange-100 rounded-lg">
                      <span className="text-2xl">⏱️</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Uptime</p>
                      <p className="text-2xl font-semibold text-gray-900">{dashboardStats.stats.uptime_hours}h</p>
                      <p className="text-sm text-green-600">System healthy</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Recent Predictions</h3>
                {dashboardStats?.recent_activity?.predictions?.length > 0 ? (
                  <div className="space-y-3">
                    {dashboardStats.recent_activity.predictions.map((pred: any, index: number) => (
                      <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                        <div>
                          <p className="font-medium">Prediction: {pred.prediction}</p>
                          <p className="text-sm text-gray-600">Confidence: {(pred.confidence * 100).toFixed(1)}%</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-gray-500">{formatTimestamp(pred.timestamp)}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No recent predictions</p>
                )}
              </div>

              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Recent Chats</h3>
                {dashboardStats?.recent_activity?.chats?.length > 0 ? (
                  <div className="space-y-3">
                    {dashboardStats.recent_activity.chats.map((chat: any, index: number) => (
                      <div key={index} className="p-3 bg-gray-50 rounded">
                        <p className="text-sm">{chat.content}</p>
                        <p className="text-xs text-gray-500 mt-1">{formatTimestamp(chat.timestamp)}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No recent chats</p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* ML Predictions Tab */}
        {activeTab === "predictions" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Prediction Input */}
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Make Prediction</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Input Features (Iris Dataset)
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                      {predictionInput.map((value, index) => (
                        <input
                          key={index}
                          type="number"
                          step="0.1"
                          value={value}
                          onChange={(e) => {
                            const newInput = [...predictionInput];
                            newInput[index] = parseFloat(e.target.value) || 0;
                            setPredictionInput(newInput);
                          }}
                          className="border border-gray-300 rounded px-3 py-2"
                          placeholder={`Feature ${index + 1}`}
                        />
                      ))}
                    </div>
                  </div>
                  <button
                    onClick={handlePredict}
                    disabled={loading.predict}
                    className="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
                  >
                    {loading.predict ? "Predicting..." : "Make Prediction"}
                  </button>
                </div>

                {predictionResult && (
                  <div className="mt-4 p-4 bg-green-50 rounded-lg">
                    <h4 className="font-semibold text-green-800">Prediction Result</h4>
                    <p className="text-green-700">Class: {predictionResult.prediction}</p>
                    <p className="text-green-700">Confidence: {(predictionResult.confidence * 100).toFixed(1)}%</p>
                    <p className="text-sm text-green-600">ID: {predictionResult.id}</p>
                    <p className="text-sm text-green-600">Stored in database: ✅</p>
                  </div>
                )}
              </div>

              {/* Model Info */}
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Model Information</h3>
                {modelInfo ? (
                  <div className="space-y-2">
                    <p><span className="font-medium">Type:</span> {modelInfo.model_type}</p>
                    <p><span className="font-medium">Version:</span> {modelInfo.model_version}</p>
                    <p><span className="font-medium">Accuracy:</span> {(modelInfo.accuracy * 100).toFixed(1)}%</p>
                    <p><span className="font-medium">Features:</span> {modelInfo.features_expected}</p>
                    <p><span className="font-medium">Classes:</span> {modelInfo.classes}</p>
                    <p><span className="font-medium">Framework:</span> {modelInfo.framework}</p>
                    <p><span className="font-medium">Status:</span> 
                      <span className="ml-2 px-2 py-1 bg-green-100 text-green-800 rounded text-sm">
                        {modelInfo.is_loaded ? "Loaded" : "Not Loaded"}
                      </span>
                    </p>
                  </div>
                ) : (
                  <p className="text-gray-500">Loading model information...</p>
                )}
              </div>
            </div>

            {/* Prediction History */}
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-4">Recent Predictions</h3>
              {predictionHistory.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Features</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Prediction</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Confidence</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Timestamp</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {predictionHistory.map((pred) => (
                        <tr key={pred.id}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{pred.id.slice(0, 8)}...</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            [{pred.features.map((f: number) => f.toFixed(1)).join(', ')}]
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{pred.prediction}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{(pred.confidence * 100).toFixed(1)}%</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatTimestamp(pred.timestamp)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-gray-500">No predictions yet. Make your first prediction above!</p>
              )}
            </div>
          </div>
        )}

        {/* AI Chat Tab */}
        {activeTab === "chat" && (
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b">
              <h3 className="text-lg font-semibold">AI Chat Assistant</h3>
              <p className="text-sm text-gray-600">Session ID: {chatSessionId}</p>
            </div>
            
            <div className="h-96 overflow-y-auto p-6 space-y-4">
              {chatMessages.length === 0 && (
                <div className="text-center text-gray-500 py-8">
                  <p>Start a conversation with the AI assistant!</p>
                </div>
              )}
              
              {chatMessages.map((message, index) => (
                <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    message.role === 'user' 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-gray-100 text-gray-900'
                  }`}>
                    <p>{message.content}</p>
                    <p className="text-xs mt-1 opacity-70">
                      {formatTimestamp(message.timestamp)}
                      {message.processing_time && ` • ${message.processing_time.toFixed(2)}s`}
                    </p>
                  </div>
                </div>
              ))}
              
              {loading.chat && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
                    <p>AI is thinking...</p>
                  </div>
                </div>
              )}
            </div>
            
            <div className="p-6 border-t">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleChat()}
                  placeholder="Type your message..."
                  className="flex-1 border border-gray-300 rounded px-3 py-2"
                  disabled={loading.chat}
                />
                <button
                  onClick={handleChat}
                  disabled={loading.chat || !chatInput.trim()}
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Text Analysis Tab */}
        {activeTab === "analysis" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Analysis Input */}
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Text Analysis</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Text to Analyze
                    </label>
                    <textarea
                      value={analysisInput}
                      onChange={(e) => setAnalysisInput(e.target.value)}
                      rows={4}
                      className="w-full border border-gray-300 rounded px-3 py-2"
                      placeholder="Enter text for sentiment analysis..."
                    />
                  </div>
                  <button
                    onClick={handleAnalysis}
                    disabled={loading.analysis || !analysisInput.trim()}
                    className="w-full bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 disabled:opacity-50"
                  >
                    {loading.analysis ? "Analyzing..." : "Analyze Sentiment"}
                  </button>
                </div>

                {analysisResult && (
                  <div className="mt-4 p-4 bg-purple-50 rounded-lg">
                    <h4 className="font-semibold text-purple-800">Analysis Result</h4>
                    <div className="flex items-center mt-2">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(analysisResult.result)}`}>
                        {analysisResult.result.toUpperCase()}
                      </span>
                      <span className="ml-2 text-purple-700">
                        Confidence: {(analysisResult.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                    <p className="text-sm text-purple-600 mt-2">ID: {analysisResult.id}</p>
                    <p className="text-sm text-purple-600">Stored in database: ✅</p>
                  </div>
                )}
              </div>

              {/* Quick Analysis Examples */}
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Quick Examples</h3>
                <div className="space-y-2">
                  {[
                    "This product is absolutely amazing!",
                    "I hate waiting in long lines.",
                    "The weather is okay today.",
                    "Best purchase I've ever made!",
                    "This service is terrible."
                  ].map((example, index) => (
                    <button
                      key={index}
                      onClick={() => setAnalysisInput(example)}
                      className="w-full text-left p-2 text-sm bg-gray-50 hover:bg-gray-100 rounded"
                    >
                      "{example}"
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Analysis History */}
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-4">Recent Analyses</h3>
              {analysisHistory.length > 0 ? (
                <div className="space-y-3">
                  {analysisHistory.map((analysis) => (
                    <div key={analysis.id} className="p-4 border rounded-lg">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <p className="text-sm text-gray-900 mb-2">"{analysis.input_text}"</p>
                          <div className="flex items-center space-x-2">
                            <span className={`px-2 py-1 rounded text-xs font-medium ${getSentimentColor(analysis.result)}`}>
                              {analysis.result.toUpperCase()}
                            </span>
                            <span className="text-sm text-gray-600">
                              {(analysis.confidence * 100).toFixed(1)}% confidence
                            </span>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-gray-500">{formatTimestamp(analysis.timestamp)}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No analyses yet. Try analyzing some text above!</p>
              )}
            </div>
          </div>
        )}

        {/* History Tab */}
        {activeTab === "history" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Prediction History */}
              <div className="bg-white p-6 rounded-lg shadow">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold">Prediction History</h3>
                  <button
                    onClick={loadPredictionHistory}
                    className="text-blue-500 hover:text-blue-700 text-sm"
                  >
                    Refresh
                  </button>
                </div>
                {predictionHistory.length > 0 ? (
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {predictionHistory.map((pred) => (
                      <div key={pred.id} className="p-3 border rounded">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Class {pred.prediction}</p>
                            <p className="text-sm text-gray-600">Confidence: {(pred.confidence * 100).toFixed(1)}%</p>
                            <p className="text-xs text-gray-500">Processing: {pred.processing_time.toFixed(3)}s</p>
                          </div>
                          <div className="text-right">
                            <p className="text-xs text-gray-500">{formatTimestamp(pred.timestamp)}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No prediction history available</p>
                )}
              </div>

              {/* Analysis History */}
              <div className="bg-white p-6 rounded-lg shadow">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold">Analysis History</h3>
                  <button
                    onClick={loadAnalysisHistory}
                    className="text-blue-500 hover:text-blue-700 text-sm"
                  >
                    Refresh
                  </button>
                </div>
                {analysisHistory.length > 0 ? (
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {analysisHistory.map((analysis) => (
                      <div key={analysis.id} className="p-3 border rounded">
                        <p className="text-sm mb-2">"{analysis.input_text}"</p>
                        <div className="flex justify-between items-center">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${getSentimentColor(analysis.result)}`}>
                            {analysis.result.toUpperCase()}
                          </span>
                          <p className="text-xs text-gray-500">{formatTimestamp(analysis.timestamp)}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No analysis history available</p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* System Tab */}
        {activeTab === "system" && (
          <div className="space-y-6">
            {/* System Status */}
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-4">System Status</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl mb-2">🟢</div>
                  <p className="font-medium">Database</p>
                  <p className="text-sm text-green-600">Connected</p>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl mb-2">🧠</div>
                  <p className="font-medium">ML Model</p>
                  <p className="text-sm text-green-600">Loaded</p>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl mb-2">🤖</div>
                  <p className="font-medium">AI Assistant</p>
                  <p className="text-sm text-green-600">Online</p>
                </div>
              </div>
            </div>

            {/* System Metrics */}
            {systemMetrics && (
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Performance Metrics (24h)</h3>
                {systemMetrics.summary && Object.keys(systemMetrics.summary).length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {Object.entries(systemMetrics.summary).map(([key, value]: [string, any]) => (
                      <div key={key} className="p-4 border rounded-lg">
                        <p className="font-medium capitalize">{key.replace(/_/g, ' ')}</p>
                        <p className="text-2xl font-bold text-blue-600">{value.avg?.toFixed(3)}s</p>
                        <p className="text-sm text-gray-600">
                          {value.count} samples • Min: {value.min?.toFixed(3)}s • Max: {value.max?.toFixed(3)}s
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No metrics data available yet. Use the system to generate metrics.</p>
                )}
              </div>
            )}

            {/* Quick Actions */}
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <button
                  onClick={loadDashboardData}
                  className="p-4 border border-blue-200 rounded-lg hover:bg-blue-50 text-center"
                >
                  <div className="text-2xl mb-2">🔄</div>
                  <p className="font-medium">Refresh Stats</p>
                </button>
                <button
                  onClick={loadModelInfo}
                  className="p-4 border border-green-200 rounded-lg hover:bg-green-50 text-center"
                >
                  <div className="text-2xl mb-2">🧠</div>
                  <p className="font-medium">Check Model</p>
                </button>
                <button
                  onClick={loadSystemMetrics}
                  className="p-4 border border-purple-200 rounded-lg hover:bg-purple-50 text-center"
                >
                  <div className="text-2xl mb-2">📊</div>
                  <p className="font-medium">Load Metrics</p>
                </button>
                <button
                  onClick={() => window.open('http://localhost:8002/docs', '_blank')}
                  className="p-4 border border-orange-200 rounded-lg hover:bg-orange-50 text-center"
                >
                  <div className="text-2xl mb-2">📚</div>
                  <p className="font-medium">API Docs</p>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}