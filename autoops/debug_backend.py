#!/usr/bin/env python3
"""
Debug script to test the backend directly
"""

import sys
import os
sys.path.append('services/model_service')

from app.model.unified_predictor import UnifiedPredictor

def test_model_loading():
    print("🔍 Testing model loading...")
    
    try:
        # Test UnifiedPredictor
        predictor = UnifiedPredictor()
        print(f"✅ UnifiedPredictor created")
        
        # Check if model is loaded
        if predictor.is_model_loaded():
            print(f"✅ Model is loaded")
            
            # Get model info
            info = predictor.get_model_info()
            print(f"📊 Model Info:")
            for key, value in info.items():
                print(f"  {key}: {value}")
            
            # Test prediction
            test_features = [5.1, 3.5, 1.4, 0.2]
            print(f"\n🧪 Testing prediction with features: {test_features}")
            
            prediction = predictor.predict(test_features)
            print(f"✅ Prediction: {prediction}")
            
            # Test with different features
            test_features2 = [6.0, 3.0, 4.0, 1.2]
            print(f"\n🧪 Testing prediction with features: {test_features2}")
            
            prediction2 = predictor.predict(test_features2)
            print(f"✅ Prediction: {prediction2}")
            
            if prediction != prediction2:
                print("✅ Model gives different predictions for different inputs!")
            else:
                print("❌ Model gives same prediction for different inputs")
                
        else:
            print("❌ Model is not loaded")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_model_loading()