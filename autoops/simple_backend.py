#!/usr/bin/env python3
"""
Simple working backend for AutoOps
"""

import os
import pickle
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import google.generativeai as genai

# Set up Gemini
os.environ['GEMINI_API_KEY'] = 'AIzaSyBFlzrCZDE4vbDF6K5uE3-BkaxzM3N5_nM'
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

app = FastAPI(title="AutoOps Simple Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = None
try:
    with open('models/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load model: {e}")

# Gemini model
gemini_model = genai.GenerativeModel('gemini-2.5-flash')

class PredictionRequest(BaseModel):
    features: List[float]

class ChatRequest(BaseModel):
    message: str
    conversation_history: List = []

class AnalysisRequest(BaseModel):
    text: str
    task: str = "sentiment"

@app.get("/")
def root():
    return {"message": "AutoOps Simple Backend", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/api/v1/predict")
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        import numpy as np
        features = np.array(request.features).reshape(1, -1)
        prediction = model.predict(features)[0]
        
        return {
            "prediction": float(prediction),
            "model_version": "v1.0.simple",
            "prediction_time": 0.001,
            "features_count": len(request.features)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/api/v1/model/info")
def model_info():
    return {
        "model_loaded": model is not None,
        "model_type": "sklearn" if model else "none",
        "model_version": "v1.0.simple",
        "features_expected": 4,
        "is_loaded": model is not None,
        "last_updated": "2024-10-20",
        "framework": "scikit-learn"
    }

@app.post("/api/v1/llm/chat")
def chat(request: ChatRequest):
    try:
        response = gemini_model.generate_content(request.message)
        return {
            "result": response.text,
            "provider": "gemini",
            "model_name": "gemini-2.5-flash",
            "processing_time": 1.0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.post("/api/v1/llm/analyze")
def analyze(request: AnalysisRequest):
    try:
        if request.task == "sentiment":
            prompt = f"Analyze the sentiment of this text and respond with ONLY ONE WORD: either 'positive', 'negative', or 'neutral'. Text: {request.text}"
            response = gemini_model.generate_content(prompt)
            result_text = response.text.strip().lower()
            
            # Clean up response
            if "positive" in result_text:
                sentiment = "positive"
            elif "negative" in result_text:
                sentiment = "negative"
            elif "neutral" in result_text:
                sentiment = "neutral"
            else:
                sentiment = "neutral"
            
            return {
                "task": request.task,
                "result": sentiment,
                "provider": "gemini",
                "processing_time": 1.0
            }
        else:
            response = gemini_model.generate_content(f"Analyze this text for {request.task}: {request.text}")
            return {
                "task": request.task,
                "result": response.text,
                "provider": "gemini",
                "processing_time": 1.0
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)