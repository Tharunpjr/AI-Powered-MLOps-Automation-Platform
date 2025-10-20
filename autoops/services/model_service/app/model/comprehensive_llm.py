"""
AutoOps Comprehensive LLM Manager
Unified interface for Gemini API, Hugging Face models, and other LLM providers.
"""

import os
from typing import Any, Dict, Optional, List, Union
from datetime import datetime

from app.model.gemini_model import GeminiModelManager
from app.model.llm_model import LLMModelManager


class ComprehensiveLLMManager:
    """
    Unified LLM manager supporting multiple providers:
    - Google Gemini API (best quality, free tier)
    - Hugging Face models (free, runs locally)
    - OpenAI API (premium, costs money)
    """
    
    def __init__(
        self, 
        provider: str = "auto",
        model_name: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize comprehensive LLM manager.
        
        Args:
            provider: LLM provider ("gemini", "huggingface", "openai", "auto")
            model_name: Specific model name (optional)
            api_key: API key for cloud providers (optional)
        """
        self.provider = provider
        self.model_name = model_name
        self.api_key = api_key
        self.active_manager = None
        self.metadata = {}
        
        # Auto-detect best available provider
        if provider == "auto":
            self.provider = self._detect_best_provider()
        
        self._initialize_manager()
    
    def _detect_best_provider(self) -> str:
        """Detect the best available LLM provider."""
        # Priority: Gemini (free + powerful) > Hugging Face (free + local) > OpenAI (paid)
        
        if os.getenv("GEMINI_API_KEY"):
            return "gemini"
        
        if os.getenv("OPENAI_API_KEY"):
            return "openai"
        
        # Default to Hugging Face (always available, no API key needed)
        return "huggingface"
    
    def _initialize_manager(self):
        """Initialize the appropriate LLM manager."""
        try:
            if self.provider == "gemini":
                self.active_manager = GeminiModelManager(
                    api_key=self.api_key,
                    model_name=self.model_name or "gemini-2.5-flash"
                )
            
            elif self.provider == "huggingface":
                # Use lightweight models for free deployment
                default_models = {
                    "chat": "microsoft/DialoGPT-small",
                    "sentiment": "cardiffnlp/twitter-roberta-base-sentiment-latest",
                    "qa": "distilbert-base-cased-distilled-squad"
                }
                
                model_name = self.model_name or default_models.get("chat")
                task = self._infer_task_from_model(model_name)
                
                self.active_manager = LLMModelManager(
                    model_name=model_name,
                    task=task
                )
            
            elif self.provider == "openai":
                self.active_manager = self._create_openai_manager()
            
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
                
        except Exception as e:
            print(f"Failed to initialize {self.provider} manager: {e}")
            # Fallback to Hugging Face
            if self.provider != "huggingface":
                print("Falling back to Hugging Face models...")
                self.provider = "huggingface"
                self._initialize_manager()
    
    def _infer_task_from_model(self, model_name: str) -> str:
        """Infer the task type from model name."""
        if "sentiment" in model_name.lower():
            return "text-classification"
        elif "qa" in model_name.lower() or "squad" in model_name.lower():
            return "question-answering"
        elif "summarization" in model_name.lower() or "bart" in model_name.lower():
            return "summarization"
        elif "translation" in model_name.lower():
            return "translation"
        else:
            return "text-generation"
    
    def _create_openai_manager(self):
        """Create OpenAI manager (placeholder for future implementation)."""
        # This would implement OpenAI API integration
        raise NotImplementedError("OpenAI integration coming soon")
    
    def load_model(self) -> bool:
        """Load the LLM model."""
        if self.active_manager is None:
            return False
        
        success = self.active_manager.load_model()
        
        if success:
            self.metadata = {
                "provider": self.provider,
                "model_loaded": True,
                "loaded_at": datetime.now().isoformat()
            }
        
        return success
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text using the active LLM.
        
        Args:
            prompt: Input text prompt
            **kwargs: Provider-specific parameters
            
        Returns:
            Generated text
        """
        if self.active_manager is None:
            raise ValueError("No LLM manager initialized")
        
        if self.provider == "gemini":
            return self.active_manager.generate_text(prompt, **kwargs)
        
        elif self.provider == "huggingface":
            results = self.active_manager.generate_text(prompt, **kwargs)
            return results[0] if isinstance(results, list) else results
        
        else:
            raise ValueError(f"Text generation not implemented for {self.provider}")
    
    def chat(self, message: str, **kwargs) -> str:
        """
        Chat with the LLM.
        
        Args:
            message: User message
            **kwargs: Provider-specific parameters
            
        Returns:
            LLM response
        """
        if self.provider == "gemini":
            return self.active_manager.chat(message, **kwargs)
        
        elif self.provider == "huggingface":
            # Use text generation for chat
            return self.generate_text(message, **kwargs)
        
        else:
            raise ValueError(f"Chat not implemented for {self.provider}")
    
    def analyze_text(self, text: str, task: str = "sentiment") -> Dict[str, Any]:
        """
        Analyze text for various tasks.
        
        Args:
            text: Text to analyze
            task: Analysis task
            
        Returns:
            Analysis results
        """
        if self.provider == "gemini":
            result = self.active_manager.analyze_text(text, task)
            # If Gemini returns a string, wrap it in a dict
            if isinstance(result, str):
                return {"task": task, "result": result}
            return result
        
        elif self.provider == "huggingface":
            if task == "sentiment":
                return self.active_manager.classify_text(text)
            else:
                # Use text generation for other tasks
                prompt = f"Analyze this text for {task}: {text}"
                result = self.generate_text(prompt, max_length=100)
                return {"task": task, "result": result}
        
        else:
            raise ValueError(f"Text analysis not implemented for {self.provider}")
    
    def answer_question(self, question: str, context: Optional[str] = None) -> str:
        """
        Answer a question.
        
        Args:
            question: Question to answer
            context: Optional context
            
        Returns:
            Answer
        """
        if self.provider == "gemini":
            return self.active_manager.answer_question(question, context)
        
        elif self.provider == "huggingface":
            if context:
                result = self.active_manager.answer_question(question, context)
                return result.get("answer", "No answer found")
            else:
                return self.generate_text(f"Question: {question}\nAnswer:", max_length=100)
        
        else:
            raise ValueError(f"Question answering not implemented for {self.provider}")
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded."""
        return (self.active_manager is not None and 
                self.active_manager.is_model_loaded())
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information."""
        if self.active_manager is None:
            return {
                "model_loaded": False,
                "provider": self.provider,
                "error": "No manager initialized"
            }
        
        info = self.active_manager.get_model_info()
        info.update({
            "provider": self.provider,
            "manager_type": "ComprehensiveLLM",
            "metadata": self.metadata
        })
        
        return info
    
    def reload_model(self) -> bool:
        """Reload the model."""
        return self.load_model()


# Predefined configurations for different use cases
LLM_CONFIGS = {
    "chatbot": {
        "provider": "gemini",
        "model_name": "gemini-2.5-flash",
        "description": "Best for conversational AI"
    },
    "sentiment_analysis": {
        "provider": "huggingface",
        "model_name": "cardiffnlp/twitter-roberta-base-sentiment-latest",
        "description": "Analyze text sentiment"
    },
    "question_answering": {
        "provider": "gemini",
        "model_name": "gemini-2.5-flash",
        "description": "Answer questions from context"
    },
    "text_generation": {
        "provider": "gemini",
        "model_name": "gemini-2.5-flash",
        "description": "Generate creative text"
    },
    "code_assistant": {
        "provider": "gemini",
        "model_name": "gemini-2.5-flash",
        "description": "Help with coding tasks"
    },
    "lightweight_chat": {
        "provider": "huggingface",
        "model_name": "microsoft/DialoGPT-small",
        "description": "Lightweight chat for free deployment"
    }
}


def create_llm_for_task(task: str = "chatbot", api_key: Optional[str] = None) -> ComprehensiveLLMManager:
    """
    Create an LLM manager optimized for a specific task.
    
    Args:
        task: Task type (chatbot, sentiment_analysis, etc.)
        api_key: API key for cloud providers
        
    Returns:
        Configured ComprehensiveLLMManager
    """
    if task not in LLM_CONFIGS:
        available = ", ".join(LLM_CONFIGS.keys())
        raise ValueError(f"Unknown task: {task}. Available: {available}")
    
    config = LLM_CONFIGS[task]
    
    return ComprehensiveLLMManager(
        provider=config["provider"],
        model_name=config["model_name"],
        api_key=api_key
    )