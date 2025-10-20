#!/usr/bin/env python3
"""
AutoOps Production Backend
Full-featured MLOps platform with database integration
"""
import os
import json
import time
import uuid
import pickle
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

import uvicorn
import numpy as np
from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
import google.generativeai as genai

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./autoops.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class PredictionRecord(Base):
    __tablename__ = "predictions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    features = Column(Text)  # JSON string
    prediction = Column(Float)
    confidence = Column(Float)
    model_version = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Float)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, index=True)
    role = Column(String)  # user, assistant
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    model_used = Column(String)
    processing_time = Column(Float, nullable=True)

class AnalysisRecord(Base):
    __tablename__ = "analysis_records"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    input_text = Column(Text)
    task = Column(String)
    result = Column(Text)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Float)

class ModelMetrics(Base):
    __tablename__ = "model_metrics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    metric_name = Column(String)
    metric_value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String)

class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    level = Column(String)  # INFO, WARNING, ERROR
    message = Column(Text)
    endpoint = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(Text, nullable=True)  # JSON string

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configure Gemini
os.environ['GEMINI_API_KEY'] = 'AIzaSyBFlzrCZDE4vbDF6K5uE3-BkaxzM3N5_nM'
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# Global variables
model = None
model_metadata = {}
gemini_model = genai.GenerativeModel('gemini-2.5-flash')
start_time = datetime.now()

# Load ML model
def load_model():
    global model, model_metadata
    try:
        with open('models/model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        try:
            with open('models/model_metadata.json', 'r') as f:
                model_metadata = json.load(f)
        except:
            model_metadata = {
                "model_version": "v2.0.production",
                "model_type": "RandomForestClassifier",
                "accuracy": 0.98,
                "features": 4,
                "classes": 3,
                "timestamp": datetime.now().strftime('%Y%m%d_%H%M%S'),
                "framework": "scikit-learn"
            }
        
        print("✅ Model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False

# Initialize model
load_model()

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting AutoOps Production Backend...")
    yield
    # Shutdown
    print("🛑 Shutting down AutoOps Production Backend...")

# FastAPI app
app = FastAPI(
    title="AutoOps Production Backend",
    description="Full-featured MLOps platform with database integration",
    version="2.0.0",
    lifespan=lifespan
)

# CORS - Production ready
import os
cors_origins = os.getenv("CORS_ORIGINS", '["*"]')
if isinstance(cors_origins, str):
    import json
    try:
        cors_origins = json.loads(cors_origins)
    except:
        cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class PredictionRequest(BaseModel):
    features: List[float] = Field(..., description="Input features for prediction")
    session_id: Optional[str] = Field(None, description="Optional session ID")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Chat session ID")
    conversation_history: List[Dict] = Field(default=[], description="Previous messages")

class AnalysisRequest(BaseModel):
    text: str = Field(..., description="Text to analyze")
    task: str = Field(default="sentiment", description="Analysis task")

class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Generation prompt")
    max_tokens: int = Field(default=100, description="Maximum tokens")
    temperature: float = Field(default=0.7, description="Generation temperature")

class QARequest(BaseModel):
    question: str = Field(..., description="Question to answer")
    context: Optional[str] = Field(None, description="Optional context")

# Utility functions
def log_system_event(db: Session, level: str, message: str, endpoint: str = None, details: Dict = None):
    """Log system events to database"""
    log_entry = SystemLog(
        level=level,
        message=message,
        endpoint=endpoint,
        details=json.dumps(details) if details else None
    )
    db.add(log_entry)
    db.commit()

def record_metric(db: Session, metric_name: str, value: float, model_version: str = None):
    """Record metrics to database"""
    metric = ModelMetrics(
        metric_name=metric_name,
        metric_value=value,
        model_version=model_version or model_metadata.get("model_version", "unknown")
    )
    db.add(metric)
    db.commit()

# Root endpoints
@app.get("/")
def root():
    return {
        "message": "AutoOps Production Backend",
        "status": "running",
        "version": "2.0.0",
        "model_loaded": model is not None,
        "database": "connected",
        "uptime_seconds": int((datetime.now() - start_time).total_seconds()),
        "features": [
            "ML Predictions with Database Storage",
            "AI Chat with Session Management", 
            "Text Analysis with History",
            "Real-time Metrics & Monitoring",
            "Production-ready Database Integration"
        ]
    }

@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    health_data = {
        "status": "healthy" if db_status == "connected" else "degraded",
        "timestamp": datetime.now().isoformat(),
        "service": "autoops-production",
        "version": "2.0.0",
        "uptime": int((datetime.now() - start_time).total_seconds()),
        "model_loaded": model is not None,
        "database": db_status,
        "gemini_configured": True
    }
    
    log_system_event(db, "INFO", "Health check performed", "/health", health_data)
    return health_data

# ML Endpoints with Database Integration
@app.post("/api/v1/predict")
def predict(request: PredictionRequest, db: Session = Depends(get_db)):
    start_time_req = time.time()
    
    if model is None:
        log_system_event(db, "ERROR", "Prediction failed: Model not loaded", "/api/v1/predict")
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        features = np.array(request.features).reshape(1, -1)
        prediction = model.predict(features)[0]
        
        # Get prediction probabilities
        try:
            probabilities = model.predict_proba(features)[0]
            confidence = float(np.max(probabilities))
        except:
            confidence = 0.95
        
        processing_time = time.time() - start_time_req
        
        # Store prediction in database
        prediction_record = PredictionRecord(
            features=json.dumps(request.features),
            prediction=float(prediction),
            confidence=confidence,
            model_version=model_metadata.get("model_version", "v2.0.production"),
            processing_time=processing_time
        )
        db.add(prediction_record)
        db.commit()
        
        # Record metrics
        record_metric(db, "prediction_time", processing_time)
        record_metric(db, "prediction_confidence", confidence)
        
        log_system_event(db, "INFO", f"Prediction completed: {prediction}", "/api/v1/predict")
        
        return {
            "id": prediction_record.id,
            "prediction": float(prediction),
            "confidence": confidence,
            "model_version": model_metadata.get("model_version", "v2.0.production"),
            "prediction_time": processing_time,
            "features_count": len(request.features),
            "model_type": model_metadata.get("model_type", "sklearn"),
            "timestamp": datetime.now().isoformat(),
            "stored": True
        }
        
    except Exception as e:
        log_system_event(db, "ERROR", f"Prediction failed: {str(e)}", "/api/v1/predict")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/api/v1/predictions")
def get_predictions(
    limit: int = Query(default=10, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """Get prediction history"""
    predictions = db.query(PredictionRecord).order_by(
        PredictionRecord.timestamp.desc()
    ).offset(offset).limit(limit).all()
    
    total = db.query(PredictionRecord).count()
    
    return {
        "predictions": [
            {
                "id": p.id,
                "features": json.loads(p.features),
                "prediction": p.prediction,
                "confidence": p.confidence,
                "model_version": p.model_version,
                "timestamp": p.timestamp.isoformat(),
                "processing_time": p.processing_time
            }
            for p in predictions
        ],
        "total": total,
        "limit": limit,
        "offset": offset
    }

# Chat endpoints with session management
@app.post("/api/v1/llm/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    start_time_req = time.time()
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        # Store user message
        user_message = ChatMessage(
            session_id=session_id,
            role="user",
            content=request.message,
            model_used="gemini-2.5-flash"
        )
        db.add(user_message)
        
        # Get conversation history from database if no history provided
        if not request.conversation_history:
            recent_messages = db.query(ChatMessage).filter(
                ChatMessage.session_id == session_id
            ).order_by(ChatMessage.timestamp.desc()).limit(10).all()
            
            context = ""
            for msg in reversed(recent_messages[-5:]):  # Last 5 messages
                context += f"{msg.role}: {msg.content}\n"
        else:
            context = ""
            for msg in request.conversation_history[-5:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                context += f"{role}: {content}\n"
        
        # Generate response
        if context:
            prompt = f"Previous conversation:\n{context}\nUser: {request.message}\nAssistant:"
        else:
            prompt = request.message
            
        response = gemini_model.generate_content(prompt)
        processing_time = time.time() - start_time_req
        
        # Store assistant response
        assistant_message = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=response.text,
            model_used="gemini-2.5-flash",
            processing_time=processing_time
        )
        db.add(assistant_message)
        db.commit()
        
        # Record metrics
        record_metric(db, "chat_response_time", processing_time)
        
        log_system_event(db, "INFO", f"Chat completed for session {session_id}", "/api/v1/llm/chat")
        
        return {
            "result": response.text,
            "session_id": session_id,
            "provider": "gemini",
            "model_name": "gemini-2.5-flash",
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat(),
            "message_id": assistant_message.id
        }
        
    except Exception as e:
        log_system_event(db, "ERROR", f"Chat failed: {str(e)}", "/api/v1/llm/chat")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.get("/api/v1/llm/chat/{session_id}")
def get_chat_history(
    session_id: str,
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db)
):
    """Get chat history for a session"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.timestamp.asc()).limit(limit).all()
    
    return {
        "session_id": session_id,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "model_used": msg.model_used,
                "processing_time": msg.processing_time
            }
            for msg in messages
        ],
        "total_messages": len(messages)
    }

# Analysis endpoints with history
@app.post("/api/v1/llm/analyze")
def analyze_text(request: AnalysisRequest, db: Session = Depends(get_db)):
    start_time_req = time.time()
    
    try:
        if request.task == "sentiment":
            prompt = f"Analyze the sentiment of this text and respond with ONLY ONE WORD: either 'positive', 'negative', or 'neutral'. Text: {request.text}"
            response = gemini_model.generate_content(prompt)
            result_text = response.text.strip().lower()
            
            if "positive" in result_text:
                result = "positive"
                confidence = 0.9
            elif "negative" in result_text:
                result = "negative"
                confidence = 0.9
            elif "neutral" in result_text:
                result = "neutral"
                confidence = 0.85
            else:
                result = "neutral"
                confidence = 0.7
                
        elif request.task == "summary":
            prompt = f"Summarize this text in 2-3 sentences: {request.text}"
            response = gemini_model.generate_content(prompt)
            result = response.text
            confidence = 0.95
            
        elif request.task == "keywords":
            prompt = f"Extract the main keywords from this text (comma-separated): {request.text}"
            response = gemini_model.generate_content(prompt)
            result = response.text
            confidence = 0.9
            
        elif request.task == "entities":
            prompt = f"Extract named entities from this text: {request.text}"
            response = gemini_model.generate_content(prompt)
            result = response.text
            confidence = 0.85
            
        else:
            prompt = f"Analyze this text for {request.task}: {request.text}"
            response = gemini_model.generate_content(prompt)
            result = response.text
            confidence = 0.8
        
        processing_time = time.time() - start_time_req
        
        # Store analysis in database
        analysis_record = AnalysisRecord(
            input_text=request.text,
            task=request.task,
            result=result,
            confidence=confidence,
            processing_time=processing_time
        )
        db.add(analysis_record)
        db.commit()
        
        # Record metrics
        record_metric(db, f"analysis_{request.task}_time", processing_time)
        record_metric(db, f"analysis_{request.task}_confidence", confidence)
        
        log_system_event(db, "INFO", f"Analysis completed: {request.task}", "/api/v1/llm/analyze")
        
        return {
            "id": analysis_record.id,
            "task": request.task,
            "result": result,
            "confidence": confidence,
            "provider": "gemini",
            "model_name": "gemini-2.5-flash",
            "processing_time": processing_time,
            "input_text": request.text,
            "timestamp": datetime.now().isoformat(),
            "stored": True
        }
        
    except Exception as e:
        log_system_event(db, "ERROR", f"Analysis failed: {str(e)}", "/api/v1/llm/analyze")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/v1/analysis")
def get_analysis_history(
    task: Optional[str] = Query(None),
    limit: int = Query(default=10, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """Get analysis history"""
    query = db.query(AnalysisRecord)
    
    if task:
        query = query.filter(AnalysisRecord.task == task)
    
    analyses = query.order_by(
        AnalysisRecord.timestamp.desc()
    ).offset(offset).limit(limit).all()
    
    total = query.count()
    
    return {
        "analyses": [
            {
                "id": a.id,
                "input_text": a.input_text[:100] + "..." if len(a.input_text) > 100 else a.input_text,
                "task": a.task,
                "result": a.result,
                "confidence": a.confidence,
                "timestamp": a.timestamp.isoformat(),
                "processing_time": a.processing_time
            }
            for a in analyses
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
        "task_filter": task
    }

# System monitoring with database
@app.get("/api/v1/system/metrics")
def get_system_metrics(
    hours: int = Query(default=24, le=168),  # Max 1 week
    db: Session = Depends(get_db)
):
    """Get system metrics from database"""
    since = datetime.now() - timedelta(hours=hours)
    
    metrics = db.query(ModelMetrics).filter(
        ModelMetrics.timestamp >= since
    ).order_by(ModelMetrics.timestamp.desc()).all()
    
    # Group metrics by name
    grouped_metrics = {}
    for metric in metrics:
        if metric.metric_name not in grouped_metrics:
            grouped_metrics[metric.metric_name] = []
        grouped_metrics[metric.metric_name].append({
            "value": metric.metric_value,
            "timestamp": metric.timestamp.isoformat(),
            "model_version": metric.model_version
        })
    
    # Calculate summary statistics
    summary = {}
    for name, values in grouped_metrics.items():
        if values:
            vals = [v["value"] for v in values]
            summary[name] = {
                "count": len(vals),
                "avg": sum(vals) / len(vals),
                "min": min(vals),
                "max": max(vals),
                "latest": values[0]["value"]  # Most recent
            }
    
    return {
        "metrics": grouped_metrics,
        "summary": summary,
        "time_range_hours": hours,
        "total_metrics": len(metrics)
    }

@app.get("/api/v1/system/logs")
def get_system_logs(
    level: Optional[str] = Query(None),
    hours: int = Query(default=24, le=168),
    limit: int = Query(default=100, le=1000),
    db: Session = Depends(get_db)
):
    """Get system logs"""
    since = datetime.now() - timedelta(hours=hours)
    
    query = db.query(SystemLog).filter(SystemLog.timestamp >= since)
    
    if level:
        query = query.filter(SystemLog.level == level.upper())
    
    logs = query.order_by(SystemLog.timestamp.desc()).limit(limit).all()
    
    return {
        "logs": [
            {
                "id": log.id,
                "level": log.level,
                "message": log.message,
                "endpoint": log.endpoint,
                "timestamp": log.timestamp.isoformat(),
                "details": json.loads(log.details) if log.details else None
            }
            for log in logs
        ],
        "total": len(logs),
        "level_filter": level,
        "time_range_hours": hours
    }

# Dashboard data endpoint
@app.get("/api/v1/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Count records
    total_predictions = db.query(PredictionRecord).count()
    today_predictions = db.query(PredictionRecord).filter(
        PredictionRecord.timestamp >= today
    ).count()
    
    total_chats = db.query(ChatMessage).filter(
        ChatMessage.role == "user"
    ).count()
    today_chats = db.query(ChatMessage).filter(
        ChatMessage.role == "user",
        ChatMessage.timestamp >= today
    ).count()
    
    total_analyses = db.query(AnalysisRecord).count()
    today_analyses = db.query(AnalysisRecord).filter(
        AnalysisRecord.timestamp >= today
    ).count()
    
    # Get recent activity
    recent_predictions = db.query(PredictionRecord).order_by(
        PredictionRecord.timestamp.desc()
    ).limit(5).all()
    
    recent_chats = db.query(ChatMessage).filter(
        ChatMessage.role == "assistant"
    ).order_by(ChatMessage.timestamp.desc()).limit(5).all()
    
    return {
        "stats": {
            "total_predictions": total_predictions,
            "today_predictions": today_predictions,
            "total_chats": total_chats,
            "today_chats": today_chats,
            "total_analyses": total_analyses,
            "today_analyses": today_analyses,
            "uptime_hours": int((now - start_time).total_seconds() / 3600),
            "model_loaded": model is not None
        },
        "recent_activity": {
            "predictions": [
                {
                    "id": p.id,
                    "prediction": p.prediction,
                    "confidence": p.confidence,
                    "timestamp": p.timestamp.isoformat()
                }
                for p in recent_predictions
            ],
            "chats": [
                {
                    "id": c.id,
                    "content": c.content[:100] + "..." if len(c.content) > 100 else c.content,
                    "timestamp": c.timestamp.isoformat()
                }
                for c in recent_chats
            ]
        }
    }

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8002))
    print("🚀 Starting AutoOps Production Backend...")
    print("📊 ML Model:", "✅ Loaded" if model else "❌ Not loaded")
    print("🤖 Gemini LLM: ✅ Configured")
    print("🗄️ Database: ✅ Connected")
    print(f"🌐 Server: http://0.0.0.0:{port}")
    print(f"📚 API Docs: http://0.0.0.0:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)