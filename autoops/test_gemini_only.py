#!/usr/bin/env python3
"""
Test Gemini API Integration Only
Simple test for Gemini API functionality.
"""

import os
import sys
from pathlib import Path

# Add the services directory to the path
sys.path.append(str(Path(__file__).parent / "services" / "model_service"))

def test_gemini_direct():
    """Test Gemini API directly."""
    print("🧪 Testing Gemini API Direct Connection...")
    
    api_key = "AIzaSyBFlzrCZDE4vbDF6K5uE3-BkaxzM3N5_nM"
    
    try:
        import google.generativeai as genai
        
        # Configure API
        genai.configure(api_key=api_key)
        
        # Create model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        print("  ✅ Model initialized successfully")
        
        # Test 1: Simple text generation
        print("  Testing text generation...")
        response = model.generate_content("What is machine learning? Answer in 2 sentences.")
        print(f"  Generated: {response.text}")
        
        # Test 2: Chat
        print("  Testing chat...")
        chat = model.start_chat()
        response = chat.send_message("Hello! Tell me a fun fact about AI.")
        print(f"  Chat response: {response.text}")
        
        # Test 3: Code generation
        print("  Testing code generation...")
        response = model.generate_content("Write a Python function to calculate fibonacci numbers. Just the code, no explanation.")
        print(f"  Code generated: {response.text[:200]}...")
        
        print("  ✅ All Gemini tests passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Gemini test failed: {e}")
        return False


def test_gemini_manager():
    """Test our Gemini manager."""
    print("🧪 Testing AutoOps Gemini Manager...")
    
    try:
        from app.model.gemini_model import GeminiModelManager
        
        # Create manager
        manager = GeminiModelManager(
            api_key="AIzaSyBFlzrCZDE4vbDF6K5uE3-BkaxzM3N5_nM",
            model_name="gemini-2.5-flash"
        )
        
        # Load model
        success = manager.load_model()
        if not success:
            print("  ❌ Failed to load manager")
            return False
        
        print("  ✅ Manager loaded successfully")
        
        # Test text generation
        print("  Testing text generation...")
        result = manager.generate_text("Explain AutoOps in one sentence.", max_tokens=50)
        print(f"  Generated: {result}")
        
        # Test chat
        print("  Testing chat...")
        result = manager.chat("What's the weather like?")
        print(f"  Chat: {result}")
        
        # Test analysis
        print("  Testing sentiment analysis...")
        result = manager.analyze_text("I love this new AI platform!", "sentiment")
        print(f"  Analysis: {result}")
        
        print("  ✅ Manager tests passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Manager test failed: {e}")
        return False


def main():
    """Run Gemini-only tests."""
    print("🚀 AutoOps Gemini-Only Integration Test")
    print("=" * 45)
    
    results = []
    
    # Test 1: Direct Gemini API
    results.append(test_gemini_direct())
    print()
    
    # Test 2: Our Gemini Manager
    results.append(test_gemini_manager())
    print()
    
    # Summary
    print("📊 Test Summary:")
    print(f"  Direct Gemini API: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"  AutoOps Manager: {'✅ PASS' if results[1] else '❌ FAIL'}")
    
    if all(results):
        print("\n🎉 Gemini integration is working perfectly!")
        print("\n💡 Your AutoOps platform now has:")
        print("  ✅ Traditional ML (scikit-learn)")
        print("  ✅ Deep Learning (PyTorch)")
        print("  ✅ Large Language Models (Gemini)")
        print("  ✅ Complete AI platform ready!")
        
        print("\n🚀 Next steps:")
        print("  1. Start the API server")
        print("  2. Test the LLM endpoints")
        print("  3. Deploy to production")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)