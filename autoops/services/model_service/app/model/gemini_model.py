"""
AutoOps Gemini API Integration
Google Gemini API support for high-quality LLM capabilities.
"""

import os
import json
from datetime import datetime
from typing import Any, Dict, Optional, List, Union

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class GeminiModelManager:
    """Manages Google Gemini API integration for LLM capabilities."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-pro"):
        """
        Initialize the Gemini model manager.
        
        Args:
            api_key: Google API key (or set GEMINI_API_KEY env var)
            model_name: Gemini model name (gemini-pro, gemini-pro-vision)
        """
        if genai is None:
            raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")
        
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self.model = None
        self.metadata = {}
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key required. Set GEMINI_API_KEY environment variable or pass api_key parameter. "
                "Get your key from: https://makersuite.google.com/app/apikey"
            )
    
    def load_model(self) -> bool:
        """
        Initialize Gemini API connection.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            # Configure API
            genai.configure(api_key=self.api_key)
            
            # Initialize model
            self.model = genai.GenerativeModel(self.model_name)
            
            # Store metadata
            self.metadata = {
                "model_name": self.model_name,
                "model_type": "Gemini API",
                "provider": "Google",
                "loaded_at": datetime.now().isoformat(),
                "api_configured": True
            }
            
            print(f"✅ Gemini model ({self.model_name}) loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load Gemini model: {e}")
            return False
    
    def generate_text(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        top_p: float = 0.8,
        top_k: int = 40
    ) -> str:
        """
        Generate text using Gemini API.
        
        Args:
            prompt: Input text prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            top_p: Top-p sampling parameter
            top_k: Top-k sampling parameter
            
        Returns:
            Generated text string
        """
        if self.model is None:
            raise ValueError("Gemini model not loaded")
        
        try:
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k
            )
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Handle safety filters and empty responses
            if response.candidates and response.candidates[0].content.parts:
                return response.text
            else:
                # Handle blocked or empty responses
                if response.candidates and response.candidates[0].finish_reason:
                    reason = response.candidates[0].finish_reason
                    if reason == 2:  # SAFETY
                        return "Response blocked by safety filters. Please try a different prompt."
                    elif reason == 3:  # RECITATION
                        return "Response blocked due to recitation concerns. Please try a different prompt."
                    else:
                        return f"Response generation stopped (reason: {reason}). Please try a different prompt."
                else:
                    return "No response generated. Please try a different prompt."
            
        except Exception as e:
            raise ValueError(f"Text generation failed: {str(e)}")
    
    def chat(self, message: str, conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Have a conversation with Gemini.
        
        Args:
            message: User message
            conversation_history: Previous conversation (optional)
            
        Returns:
            Gemini's response
        """
        if self.model is None:
            raise ValueError("Gemini model not loaded")
        
        try:
            # Start chat session
            chat = self.model.start_chat(history=conversation_history or [])
            
            # Send message
            response = chat.send_message(message)
            
            # Handle safety filters and empty responses
            if response.candidates and response.candidates[0].content.parts:
                return response.text
            else:
                return "Response blocked or empty. Please try a different message."
            
        except Exception as e:
            raise ValueError(f"Chat failed: {str(e)}")
    
    def analyze_text(self, text: str, task: str = "sentiment") -> Dict[str, Any]:
        """
        Analyze text for various tasks.
        
        Args:
            text: Text to analyze
            task: Analysis task (sentiment, summary, keywords, etc.)
            
        Returns:
            Analysis results
        """
        if self.model is None:
            raise ValueError("Gemini model not loaded")
        
        prompts = {
            "sentiment": f"Analyze the sentiment of this text and respond with ONLY ONE WORD: either 'positive', 'negative', or 'neutral'. Text: {text}",
            "summary": f"Summarize this text in 2-3 sentences: {text}",
            "keywords": f"Extract the main keywords from this text (comma-separated): {text}",
            "classify": f"Classify this text into a category: {text}",
            "translate": f"Translate this text to English: {text}"
        }
        
        if task not in prompts:
            prompt = f"Analyze this text for {task}: {text}"
        else:
            prompt = prompts[task]
        
        try:
            response = self.model.generate_content(prompt)
            
            # Handle safety filters and empty responses
            if response.candidates and response.candidates[0].content.parts:
                result_text = response.text.strip().lower()
            else:
                result_text = "Response blocked or empty. Please try a different prompt."
            
            # For sentiment, clean up the response to just the sentiment word
            if task == "sentiment":
                # Extract just the sentiment word
                if "positive" in result_text:
                    result_text = "positive"
                elif "negative" in result_text:
                    result_text = "negative"
                elif "neutral" in result_text:
                    result_text = "neutral"
                else:
                    # If Gemini didn't follow instructions, default to neutral
                    result_text = "neutral"
            
            # Return as string for the comprehensive LLM to wrap
            return result_text
            
        except Exception as e:
            raise ValueError(f"Text analysis failed: {str(e)}")
    
    def answer_question(self, question: str, context: Optional[str] = None) -> str:
        """
        Answer a question, optionally with context.
        
        Args:
            question: Question to answer
            context: Additional context (optional)
            
        Returns:
            Answer string
        """
        if self.model is None:
            raise ValueError("Gemini model not loaded")
        
        try:
            if context:
                prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
            else:
                prompt = f"Question: {question}\n\nAnswer:"
            
            response = self.model.generate_content(prompt)
            
            # Handle safety filters and empty responses
            if response.candidates and response.candidates[0].content.parts:
                return response.text
            else:
                return "Response blocked or empty. Please try a different prompt."
            
        except Exception as e:
            raise ValueError(f"Question answering failed: {str(e)}")
    
    def code_generation(self, description: str, language: str = "python") -> str:
        """
        Generate code based on description.
        
        Args:
            description: What the code should do
            language: Programming language
            
        Returns:
            Generated code
        """
        if self.model is None:
            raise ValueError("Gemini model not loaded")
        
        try:
            prompt = f"Write {language} code that {description}. Only return the code, no explanations:"
            
            response = self.model.generate_content(prompt)
            
            # Handle safety filters and empty responses
            if response.candidates and response.candidates[0].content.parts:
                return response.text
            else:
                return "Response blocked or empty. Please try a different prompt."
            
        except Exception as e:
            raise ValueError(f"Code generation failed: {str(e)}")
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.model is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information and metadata.
        
        Returns:
            Dictionary containing model information
        """
        return {
            "model_loaded": self.is_model_loaded(),
            "model_name": self.model_name,
            "model_type": "Gemini API",
            "provider": "Google",
            "api_configured": self.api_key is not None,
            "capabilities": [
                "text_generation",
                "chat",
                "question_answering", 
                "text_analysis",
                "code_generation",
                "translation"
            ],
            "metadata": self.metadata.copy()
        }
    
    def reload_model(self) -> bool:
        """Reload the model."""
        return self.load_model()


# Predefined Gemini configurations
GEMINI_MODELS = {
    "gemini-2.5-flash": {
        "name": "gemini-2.5-flash",
        "description": "Fast and efficient model for text tasks",
        "best_for": ["chat", "analysis", "code", "reasoning"]
    },
    "gemini-2.5-pro": {
        "name": "gemini-2.5-pro",
        "description": "Most capable model for complex tasks",
        "best_for": ["complex_reasoning", "analysis", "code", "research"]
    },
    "gemini-pro-vision": {
        "name": "gemini-pro-vision", 
        "description": "Multimodal model for text and images",
        "best_for": ["image_analysis", "visual_qa", "multimodal"]
    }
}


def create_gemini_manager(model_name: str = "gemini-2.5-flash", api_key: Optional[str] = None) -> GeminiModelManager:
    """
    Create a Gemini manager with specified model.
    
    Args:
        model_name: Gemini model name
        api_key: API key (optional, uses env var if not provided)
        
    Returns:
        Configured GeminiModelManager instance
    """
    return GeminiModelManager(api_key=api_key, model_name=model_name)