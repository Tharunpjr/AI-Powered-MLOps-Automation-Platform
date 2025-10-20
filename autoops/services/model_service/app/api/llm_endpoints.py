"""
AutoOps LLM API Endpoints
REST API endpoints for LLM capabilities (text generation, chat, analysis).
"""

import time
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.model.comprehensive_llm import ComprehensiveLLMManager, create_llm_for_task
from app.utils.telemetry import record_prediction

router = APIRouter()

# Global LLM manager instance
llm_manager = None


class TextGenerationRequest(BaseModel):
    """Request model for text generation."""
    prompt: str = Field(..., description="Input text prompt", example="Write a story about AI")
    max_tokens: int = Field(100, description="Maximum tokens to generate", example=100)
    temperature: float = Field(0.7, description="Sampling temperature (0.0-1.0)", example=0.7)


class ChatRequest(BaseModel):
    """Request model for chat."""
    message: str = Field(..., description="User message", example="Hello, how are you?")
    conversation_history: Optional[List[Dict]] = Field(None, description="Previous conversation")


class TextAnalysisRequest(BaseModel):
    """Request model for text analysis."""
    text: str = Field(..., description="Text to analyze", example="I love this product!")
    task: str = Field("sentiment", description="Analysis task", example="sentiment")


class QuestionAnsweringRequest(BaseModel):
    """Request model for question answering."""
    question: str = Field(..., description="Question to answer", example="What is AI?")
    context: Optional[str] = Field(None, description="Context for the question")


class LLMResponse(BaseModel):
    """Response model for LLM operations."""
    result: str = Field(..., description="LLM output")
    provider: str = Field(..., description="LLM provider used")
    model_name: str = Field(..., description="Model name")
    processing_time: float = Field(..., description="Processing time in seconds")


class AnalysisResponse(BaseModel):
    """Response model for text analysis."""
    task: str = Field(..., description="Analysis task performed")
    result: Any = Field(..., description="Analysis result")
    provider: str = Field(..., description="LLM provider used")
    processing_time: float = Field(..., description="Processing time in seconds")


def get_llm_manager(task: str = "chatbot") -> ComprehensiveLLMManager:
    """Dependency to get the LLM manager instance."""
    global llm_manager
    
    if llm_manager is None:
        try:
            llm_manager = create_llm_for_task(task)
            llm_manager.load_model()
        except Exception as e:
            print(f"Failed to initialize LLM manager: {e}")
            # Try fallback
            try:
                llm_manager = ComprehensiveLLMManager(provider="huggingface")
                llm_manager.load_model()
            except Exception as e2:
                print(f"Fallback also failed: {e2}")
                llm_manager = None
    
    if llm_manager is None or not llm_manager.is_model_loaded():
        raise HTTPException(
            status_code=503,
            detail="LLM service unavailable. Please check configuration."
        )
    
    return llm_manager


@router.post("/generate", response_model=LLMResponse)
async def generate_text(
    request: TextGenerationRequest,
    llm: ComprehensiveLLMManager = Depends(get_llm_manager)
) -> LLMResponse:
    """
    Generate text using LLM.
    
    Args:
        request: Text generation request
        llm: LLM manager instance
        
    Returns:
        Generated text response
    """
    start_time = time.time()
    
    try:
        # Generate text
        if llm.provider == "gemini":
            result = llm.generate_text(
                prompt=request.prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
        else:
            # Hugging Face uses different parameter names
            result = llm.generate_text(
                prompt=request.prompt,
                max_length=request.max_tokens,
                temperature=request.temperature
            )
        
        processing_time = time.time() - start_time
        
        # Record metrics
        record_prediction("llm_text_generation", processing_time)
        
        # Get model info
        model_info = llm.get_model_info()
        
        return LLMResponse(
            result=result,
            provider=model_info.get("provider", "unknown"),
            model_name=model_info.get("model_name", "unknown"),
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Text generation failed: {str(e)}"
        )


@router.post("/chat", response_model=LLMResponse)
async def chat(
    request: ChatRequest,
    llm: ComprehensiveLLMManager = Depends(get_llm_manager)
) -> LLMResponse:
    """
    Chat with the LLM.
    
    Args:
        request: Chat request
        llm: LLM manager instance
        
    Returns:
        Chat response
    """
    start_time = time.time()
    
    try:
        # Chat with LLM
        result = llm.chat(
            message=request.message,
            conversation_history=request.conversation_history
        )
        
        processing_time = time.time() - start_time
        
        # Record metrics
        record_prediction("llm_chat", processing_time)
        
        # Get model info
        model_info = llm.get_model_info()
        
        return LLMResponse(
            result=result,
            provider=model_info.get("provider", "unknown"),
            model_name=model_info.get("model_name", "unknown"),
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}"
        )


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(
    request: TextAnalysisRequest,
    llm: ComprehensiveLLMManager = Depends(get_llm_manager)
) -> AnalysisResponse:
    """
    Analyze text for various tasks.
    
    Args:
        request: Text analysis request
        llm: LLM manager instance
        
    Returns:
        Analysis results
    """
    start_time = time.time()
    
    try:
        # Analyze text
        result = llm.analyze_text(
            text=request.text,
            task=request.task
        )
        
        processing_time = time.time() - start_time
        
        # Record metrics
        record_prediction(f"llm_analysis_{request.task}", processing_time)
        
        # Get model info
        model_info = llm.get_model_info()
        
        return AnalysisResponse(
            task=request.task,
            result=result,
            provider=model_info.get("provider", "unknown"),
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Text analysis failed: {str(e)}"
        )


@router.post("/qa", response_model=LLMResponse)
async def answer_question(
    request: QuestionAnsweringRequest,
    llm: ComprehensiveLLMManager = Depends(get_llm_manager)
) -> LLMResponse:
    """
    Answer a question using the LLM.
    
    Args:
        request: Question answering request
        llm: LLM manager instance
        
    Returns:
        Answer response
    """
    start_time = time.time()
    
    try:
        # Answer question
        result = llm.answer_question(
            question=request.question,
            context=request.context
        )
        
        processing_time = time.time() - start_time
        
        # Record metrics
        record_prediction("llm_qa", processing_time)
        
        # Get model info
        model_info = llm.get_model_info()
        
        return LLMResponse(
            result=result,
            provider=model_info.get("provider", "unknown"),
            model_name=model_info.get("model_name", "unknown"),
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Question answering failed: {str(e)}"
        )


@router.get("/models")
async def list_available_models() -> Dict[str, Any]:
    """
    List available LLM models and configurations.
    
    Returns:
        Available models and their capabilities
    """
    from app.model.comprehensive_llm import LLM_CONFIGS
    
    return {
        "available_tasks": list(LLM_CONFIGS.keys()),
        "configurations": LLM_CONFIGS,
        "providers": {
            "gemini": {
                "description": "Google Gemini API - High quality, free tier available",
                "requires_api_key": True,
                "get_key_url": "https://makersuite.google.com/app/apikey"
            },
            "huggingface": {
                "description": "Hugging Face models - Free, runs locally",
                "requires_api_key": False,
                "note": "Smaller models for free deployment"
            }
        },
        "setup_instructions": {
            "gemini": "Set GEMINI_API_KEY environment variable",
            "huggingface": "No setup required, models download automatically"
        }
    }


@router.get("/status")
async def llm_status() -> Dict[str, Any]:
    """
    Get LLM service status.
    
    Returns:
        Current LLM service status
    """
    try:
        llm = get_llm_manager()
        model_info = llm.get_model_info()
        
        return {
            "status": "healthy",
            "model_loaded": llm.is_model_loaded(),
            "provider": model_info.get("provider"),
            "model_name": model_info.get("model_name"),
            "capabilities": model_info.get("capabilities", []),
            "last_check": time.time()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "model_loaded": False,
            "last_check": time.time()
        }