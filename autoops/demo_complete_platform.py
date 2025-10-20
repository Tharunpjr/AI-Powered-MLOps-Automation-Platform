#!/usr/bin/env python3
"""
AutoOps Complete Platform Demo
Demonstrates all capabilities: Traditional ML, Deep Learning, and LLMs
"""

import os
import sys
from pathlib import Path

# Add the services directory to the path
sys.path.append(str(Path(__file__).parent / "services" / "model_service"))

def demo_traditional_ml():
    """Demo traditional ML capabilities."""
    print("🤖 Traditional ML (scikit-learn)")
    print("-" * 40)
    
    try:
        from app.model.model import ModelManager
        
        # Check if we have a trained model
        model_path = Path("models/model.pkl")
        if not model_path.exists():
            print("  ⚠️ No trained model found. Run training first:")
            print("     python pipelines/training/train.py --synthetic --out models/")
            return False
        
        # Load and test model
        manager = ModelManager(str(model_path))
        success = manager.load_model()
        
        if success:
            print("  ✅ scikit-learn model loaded")
            
            # Test prediction
            model = manager.get_model()
            import numpy as np
            test_features = np.array([[1.0, 2.0, 3.0, 4.0]])
            prediction = model.predict(test_features)[0]
            
            print(f"  📊 Prediction for [1.0, 2.0, 3.0, 4.0]: {prediction:.4f}")
            print("  ✅ Traditional ML working!")
            return True
        else:
            print("  ❌ Failed to load model")
            return False
            
    except Exception as e:
        print(f"  ❌ Traditional ML test failed: {e}")
        return False


def demo_deep_learning():
    """Demo PyTorch deep learning capabilities."""
    print("\n🧠 Deep Learning (PyTorch)")
    print("-" * 40)
    
    try:
        from app.model.pytorch_model import PyTorchModelManager
        
        # Check if we have a trained PyTorch model
        model_path = Path("models/pytorch_model.pt")
        if not model_path.exists():
            print("  ⚠️ No PyTorch model found. Run training first:")
            print("     python pipelines/training/train_pytorch.py --synthetic --out models/")
            return False
        
        # Load and test model
        manager = PyTorchModelManager(str(model_path))
        success = manager.load_model()
        
        if success:
            print("  ✅ PyTorch model loaded")
            
            # Test prediction
            import numpy as np
            test_features = np.array([[1.0, 2.0, 3.0, 4.0]])
            prediction = manager.predict(test_features)[0][0]
            
            print(f"  📊 Prediction for [1.0, 2.0, 3.0, 4.0]: {prediction:.4f}")
            print("  ✅ Deep Learning working!")
            return True
        else:
            print("  ❌ Failed to load PyTorch model")
            return False
            
    except Exception as e:
        print(f"  ❌ Deep Learning test failed: {e}")
        return False


def demo_llm():
    """Demo LLM capabilities with Gemini."""
    print("\n🧠 Large Language Models (Gemini)")
    print("-" * 40)
    
    try:
        from app.model.gemini_model import GeminiModelManager
        
        # Create and load Gemini manager
        manager = GeminiModelManager(
            api_key="AIzaSyBFlzrCZDE4vbDF6K5uE3-BkaxzM3N5_nM",
            model_name="gemini-2.5-flash"
        )
        
        success = manager.load_model()
        if not success:
            print("  ❌ Failed to load Gemini model")
            return False
        
        print("  ✅ Gemini model loaded")
        
        # Test 1: Text Generation
        print("  📝 Testing text generation...")
        response = manager.generate_text(
            "Explain what AutoOps does in one sentence.",
            max_tokens=50
        )
        print(f"     Generated: {response}")
        
        # Test 2: Sentiment Analysis
        print("  😊 Testing sentiment analysis...")
        analysis = manager.analyze_text(
            "AutoOps is an amazing MLOps platform!",
            "sentiment"
        )
        print(f"     Sentiment: {analysis['result']}")
        
        # Test 3: Question Answering
        print("  ❓ Testing question answering...")
        answer = manager.answer_question(
            "What is machine learning?",
            "Machine learning is a subset of AI that enables systems to learn from data."
        )
        print(f"     Answer: {answer[:100]}...")
        
        # Test 4: Code Generation
        print("  💻 Testing code generation...")
        code = manager.code_generation(
            "creates a simple hello world function",
            "python"
        )
        print(f"     Code: {code[:100]}...")
        
        print("  ✅ LLM capabilities working!")
        return True
        
    except Exception as e:
        print(f"  ❌ LLM test failed: {e}")
        return False


def demo_unified_interface():
    """Demo unified interface that handles all model types."""
    print("\n🔗 Unified Interface")
    print("-" * 40)
    
    try:
        from app.model.unified_predictor import UnifiedPredictor
        
        # Test unified predictor
        predictor = UnifiedPredictor()
        
        if predictor.is_model_loaded():
            print("  ✅ Unified predictor loaded")
            
            # Get model info
            info = predictor.get_model_info()
            print(f"  📋 Model type: {info['framework']}")
            print(f"  📋 Model version: {info['model_version']}")
            
            # Test prediction
            prediction = predictor.predict([1.0, 2.0, 3.0, 4.0])
            print(f"  📊 Unified prediction: {prediction:.4f}")
            
            print("  ✅ Unified interface working!")
            return True
        else:
            print("  ⚠️ No model loaded in unified predictor")
            return False
            
    except Exception as e:
        print(f"  ❌ Unified interface test failed: {e}")
        return False


def main():
    """Run complete platform demo."""
    print("🚀 AutoOps Complete AI Platform Demo")
    print("=" * 50)
    print("Demonstrating all capabilities:")
    print("• Traditional ML (scikit-learn)")
    print("• Deep Learning (PyTorch)")
    print("• Large Language Models (Gemini)")
    print("• Unified Interface")
    print("=" * 50)
    
    results = []
    
    # Demo 1: Traditional ML
    results.append(demo_traditional_ml())
    
    # Demo 2: Deep Learning
    results.append(demo_deep_learning())
    
    # Demo 3: LLMs
    results.append(demo_llm())
    
    # Demo 4: Unified Interface
    results.append(demo_unified_interface())
    
    # Summary
    print("\n📊 Platform Capabilities Summary")
    print("=" * 50)
    print(f"Traditional ML:     {'✅ WORKING' if results[0] else '❌ NEEDS SETUP'}")
    print(f"Deep Learning:      {'✅ WORKING' if results[1] else '❌ NEEDS SETUP'}")
    print(f"Large Language Models: {'✅ WORKING' if results[2] else '❌ FAILED'}")
    print(f"Unified Interface:  {'✅ WORKING' if results[3] else '❌ FAILED'}")
    
    working_count = sum(results)
    total_count = len(results)
    
    print(f"\n🎯 Platform Status: {working_count}/{total_count} capabilities working")
    
    if working_count >= 2:
        print("\n🎉 AutoOps AI Platform is operational!")
        print("\n💡 What you can do now:")
        if results[0]:
            print("  ✅ Make predictions with traditional ML models")
        if results[1]:
            print("  ✅ Use deep learning neural networks")
        if results[2]:
            print("  ✅ Chat with AI, generate text, analyze sentiment")
        if results[3]:
            print("  ✅ Use unified API for all model types")
        
        print("\n🚀 Next steps:")
        print("  1. Start the API server:")
        print("     cd services/model_service")
        print("     set GEMINI_API_KEY=AIzaSyBFlzrCZDE4vbDF6K5uE3-BkaxzM3N5_nM")
        print("     python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        print("  2. Test endpoints at http://localhost:8000/docs")
        print("  3. Deploy to production (see DEPLOYMENT_GUIDE.md)")
        
    else:
        print("\n⚠️ Platform needs setup. Run training scripts first:")
        if not results[0]:
            print("  python pipelines/training/train.py --synthetic --out models/")
        if not results[1]:
            print("  python pipelines/training/train_pytorch.py --synthetic --out models/")
    
    return working_count >= 2


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)