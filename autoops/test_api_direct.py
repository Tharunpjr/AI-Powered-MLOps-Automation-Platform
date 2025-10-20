#!/usr/bin/env python3
"""
Test the API endpoints directly
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("🔍 Testing API endpoints...")
    
    # Test health
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health: {response.status_code}")
    except Exception as e:
        print(f"❌ Health: {e}")
    
    # Test prediction
    try:
        data = {"features": [5.1, 3.5, 1.4, 0.2]}
        response = requests.post(f"{base_url}/api/v1/predict", 
                               json=data, 
                               timeout=10)
        print(f"📊 Prediction Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction: {result['prediction']}")
            print(f"📝 Model Version: {result['model_version']}")
        else:
            print(f"❌ Error Response: {response.text}")
    except Exception as e:
        print(f"❌ Prediction Error: {e}")
    
    # Test different prediction
    try:
        data = {"features": [6.0, 3.0, 4.0, 1.2]}
        response = requests.post(f"{base_url}/api/v1/predict", 
                               json=data, 
                               timeout=10)
        print(f"📊 Prediction 2 Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction 2: {result['prediction']}")
        else:
            print(f"❌ Error Response 2: {response.text}")
    except Exception as e:
        print(f"❌ Prediction 2 Error: {e}")
    
    # Test chat
    try:
        data = {"message": "Hello", "conversation_history": []}
        response = requests.post(f"{base_url}/api/v1/llm/chat", 
                               json=data, 
                               timeout=15)
        print(f"💬 Chat Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat Response: {result['result'][:100]}...")
        else:
            print(f"❌ Chat Error Response: {response.text}")
    except Exception as e:
        print(f"❌ Chat Error: {e}")

if __name__ == "__main__":
    test_api()