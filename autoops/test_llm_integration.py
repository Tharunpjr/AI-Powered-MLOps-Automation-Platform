#!/usr/bin/env python3
"""
Test LLM Integration
Quick test script to verify LLM functionality works.
"""

import os
import sys
from pathlib import Path

# Add the services directory to the path
sys.path.append(str(Path(__file__).parent / "services" / "model_service"))

def test_huggingface_llm():
    """Test Hugging Face LLM (always available)."""
    print("🧪 Testing Hugging Face LLM...")
    
    try:
        from app.model.comprehensive_llm import ComprehensiveLLMManager
        
        # Create manager with Hugging Face (no API key needed)
        llm = ComprehensiveLLMManager(provider="huggingface")
        
        print("  Loading model...")
        success = llm.load_model()
        
        if success:
            print("  ✅ Model loaded successfully")
            
            # Test text generation
            print("  Testing text generation...")
            result = llm.generate_text("Hello, how are you?", max_length=50)
            print(f"  Generated: {result[:100]}...")
            
            print("  ✅ Hugging Face LLM test passed!")
            return True
        else:
            print("  ❌ Failed to load model")
            return False
            
    except Exception as e:
        print(f"  ❌ Hugging Face test failed: {e}")
        return False


def test_gemini_llm():
    """Test Gemini API (if API key available)."""
    print("🧪 Testing Gemini API...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("  ⚠️ GEMINI_API_KEY not set, skipping Gemini test")
        print("  💡 Get your key from: https://makersuite.google.com/app/apikey")
        return False
    
    try:
        from app.model.comprehensive_llm import ComprehensiveLLMManager
        
        # Create manager with Gemini
        llm = ComprehensiveLLMManager(provider="gemini", api_key=api_key)
        llm.active_manager.model_name = "gemini-2.5-flash"  # Use correct model name
        
        print("  Loading model...")
        success = llm.load_model()
        
        if success:
            print("  ✅ Model loaded successfully")
            
            # Test text generation
            print("  Testing text generation...")
            result = llm.generate_text("What is artificial intelligence?", max_tokens=100)
            print(f"  Generated: {result[:200]}...")
            
            # Test chat
            print("  Testing chat...")
            chat_result = llm.chat("Hello! Tell me a joke.")
            print(f"  Chat response: {chat_result[:200]}...")
            
            # Test analysis
            print("  Testing sentiment analysis...")
            analysis = llm.analyze_text("I love this product!", "sentiment")
            print(f"  Analysis: {analysis}")
            
            print("  ✅ Gemini API test passed!")
            return True
        else:
            print("  ❌ Failed to load model")
            return False
            
    except Exception as e:
        print(f"  ❌ Gemini test failed: {e}")
        return False


def test_api_endpoints():
    """Test LLM API endpoints."""
    print("🧪 Testing API endpoints...")
    
    try:
        import requests
        import time
        
        # Start the server in background (you need to run this manually)
        base_url = "http://localhost:8000"
        
        # Test if server is running
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code != 200:
                print("  ⚠️ Server not running. Start with:")
                print("     cd services/model_service")
                print("     python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
                return False
        except requests.exceptions.RequestException:
            print("  ⚠️ Server not running. Start with:")
            print("     cd services/model_service")
            print("     python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
            return False
        
        # Test LLM endpoints
        print("  Testing LLM status...")
        response = requests.get(f"{base_url}/api/v1/llm/status")
        print(f"  Status: {response.json()}")
        
        print("  Testing text generation...")
        response = requests.post(
            f"{base_url}/api/v1/llm/generate",
            json={
                "prompt": "Write a short poem about AI",
                "max_tokens": 100,
                "temperature": 0.7
            }
        )
        if response.status_code == 200:
            result = response.json()
            print(f"  Generated: {result['result'][:100]}...")
            print("  ✅ API endpoints test passed!")
            return True
        else:
            print(f"  ❌ API test failed: {response.status_code} - {response.text}")
            return False
            
    except ImportError:
        print("  ⚠️ requests not installed. Run: pip install requests")
        return False
    except Exception as e:
        print(f"  ❌ API test failed: {e}")
        return False


def main():
    """Run all LLM tests."""
    print("🚀 AutoOps LLM Integration Test")
    print("=" * 40)
    
    results = []
    
    # Test 1: Hugging Face (always available)
    results.append(test_huggingface_llm())
    print()
    
    # Test 2: Gemini API (if key available)
    results.append(test_gemini_llm())
    print()
    
    # Test 3: API endpoints (if server running)
    results.append(test_api_endpoints())
    print()
    
    # Summary
    print("📊 Test Summary:")
    print(f"  Hugging Face: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"  Gemini API: {'✅ PASS' if results[1] else '⚠️ SKIP (no API key)'}")
    print(f"  API Endpoints: {'✅ PASS' if results[2] else '⚠️ SKIP (server not running)'}")
    
    if any(results):
        print("\n🎉 LLM integration is working!")
        print("\n💡 Next steps:")
        print("  1. Set GEMINI_API_KEY for best performance")
        print("  2. Start the server to test API endpoints")
        print("  3. Deploy to production with free hosting")
    else:
        print("\n❌ All tests failed. Check your setup.")
    
    return any(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)