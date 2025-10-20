"""
AutoOps LLM Model Manager
Large Language Model support with Hugging Face Transformers.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List, Union

import torch
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification,
    AutoModelForQuestionAnswering, pipeline, Pipeline
)


class LLMModelManager:
    """Manages LLM loading, inference, and operations using Hugging Face Transformers."""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-small", task: str = "text-generation"):
        """
        Initialize the LLM model manager.
        
        Args:
            model_name: Hugging Face model name or local path
            task: Task type (text-generation, text-classification, question-answering, etc.)
        """
        self.model_name = model_name
        self.task = task
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.metadata = {}
        
        # Model cache directory
        self.cache_dir = Path("models/llm_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def load_model(self) -> bool:
        """
        Load LLM model from Hugging Face Hub or local cache.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            print(f"Loading LLM model: {self.model_name}")
            print(f"Task: {self.task}")
            print(f"Device: {self.device}")
            
            # Create pipeline (handles model and tokenizer automatically)
            self.pipeline = pipeline(
                task=self.task,
                model=self.model_name,
                device=0 if self.device.type == "cuda" else -1,
                cache_dir=str(self.cache_dir),
                torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32
            )
            
            # Store metadata
            self.metadata = {
                "model_name": self.model_name,
                "task": self.task,
                "device": str(self.device),
                "loaded_at": datetime.now().isoformat(),
                "model_type": "LLM"
            }
            
            print(f"✅ LLM model loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load LLM model: {e}")
            return False
    
    def generate_text(
        self, 
        prompt: str, 
        max_length: int = 100, 
        temperature: float = 0.7,
        num_return_sequences: int = 1
    ) -> List[str]:
        """
        Generate text using the loaded model.
        
        Args:
            prompt: Input text prompt
            max_length: Maximum length of generated text
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = random)
            num_return_sequences: Number of sequences to generate
            
        Returns:
            List of generated text strings
        """
        if self.pipeline is None or self.task != "text-generation":
            raise ValueError("Text generation model not loaded")
        
        try:
            results = self.pipeline(
                prompt,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=num_return_sequences,
                do_sample=True,
                pad_token_id=self.pipeline.tokenizer.eos_token_id
            )
            
            # Extract generated text
            if isinstance(results, list):
                return [result['generated_text'] for result in results]
            else:
                return [results['generated_text']]
                
        except Exception as e:
            raise ValueError(f"Text generation failed: {str(e)}")
    
    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        Classify text using the loaded model.
        
        Args:
            text: Input text to classify
            
        Returns:
            Classification results with labels and scores
        """
        if self.pipeline is None or self.task != "text-classification":
            raise ValueError("Text classification model not loaded")
        
        try:
            result = self.pipeline(text)
            
            if isinstance(result, list):
                return result[0]  # Return first result
            return result
            
        except Exception as e:
            raise ValueError(f"Text classification failed: {str(e)}")
    
    def answer_question(self, question: str, context: str) -> Dict[str, Any]:
        """
        Answer a question based on context.
        
        Args:
            question: Question to answer
            context: Context text containing the answer
            
        Returns:
            Answer with confidence score
        """
        if self.pipeline is None or self.task != "question-answering":
            raise ValueError("Question answering model not loaded")
        
        try:
            result = self.pipeline(question=question, context=context)
            return result
            
        except Exception as e:
            raise ValueError(f"Question answering failed: {str(e)}")
    
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        """
        Summarize text using the loaded model.
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            Summary text
        """
        if self.pipeline is None or self.task != "summarization":
            raise ValueError("Summarization model not loaded")
        
        try:
            result = self.pipeline(text, max_length=max_length, min_length=min_length)
            
            if isinstance(result, list):
                return result[0]['summary_text']
            return result['summary_text']
            
        except Exception as e:
            raise ValueError(f"Text summarization failed: {str(e)}")
    
    def translate_text(self, text: str) -> str:
        """
        Translate text using the loaded model.
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        if self.pipeline is None or self.task != "translation":
            raise ValueError("Translation model not loaded")
        
        try:
            result = self.pipeline(text)
            
            if isinstance(result, list):
                return result[0]['translation_text']
            return result['translation_text']
            
        except Exception as e:
            raise ValueError(f"Translation failed: {str(e)}")
    
    def get_embeddings(self, texts: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Get text embeddings using sentence transformers.
        
        Args:
            texts: Single text or list of texts
            
        Returns:
            Embeddings as list(s) of floats
        """
        try:
            from sentence_transformers import SentenceTransformer
            
            # Use a lightweight embedding model
            embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = embedding_model.encode(texts)
            
            if isinstance(texts, str):
                return embeddings.tolist()
            return [emb.tolist() for emb in embeddings]
            
        except ImportError:
            raise ValueError("sentence-transformers not installed. Run: pip install sentence-transformers")
        except Exception as e:
            raise ValueError(f"Embedding generation failed: {str(e)}")
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.pipeline is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information and metadata.
        
        Returns:
            Dictionary containing model information
        """
        info = {
            "model_loaded": self.is_model_loaded(),
            "model_name": self.model_name,
            "task": self.task,
            "device": str(self.device),
            "model_type": "LLM",
            "metadata": self.metadata.copy()
        }
        
        if self.pipeline is not None:
            try:
                # Get model size info
                if hasattr(self.pipeline.model, 'num_parameters'):
                    info["parameters"] = self.pipeline.model.num_parameters()
                elif hasattr(self.pipeline.model, 'config'):
                    config = self.pipeline.model.config
                    info["model_config"] = {
                        "vocab_size": getattr(config, 'vocab_size', 'unknown'),
                        "hidden_size": getattr(config, 'hidden_size', 'unknown'),
                        "num_layers": getattr(config, 'num_hidden_layers', 'unknown')
                    }
            except:
                pass
        
        return info
    
    def reload_model(self) -> bool:
        """Reload the model."""
        return self.load_model()


# Predefined model configurations for common use cases
PREDEFINED_MODELS = {
    "chat": {
        "model_name": "microsoft/DialoGPT-small",
        "task": "text-generation",
        "description": "Conversational AI chatbot"
    },
    "sentiment": {
        "model_name": "cardiffnlp/twitter-roberta-base-sentiment-latest",
        "task": "text-classification",
        "description": "Sentiment analysis (positive/negative/neutral)"
    },
    "qa": {
        "model_name": "distilbert-base-cased-distilled-squad",
        "task": "question-answering",
        "description": "Question answering from context"
    },
    "summarize": {
        "model_name": "facebook/bart-large-cnn",
        "task": "summarization",
        "description": "Text summarization"
    },
    "translate_en_fr": {
        "model_name": "Helsinki-NLP/opus-mt-en-fr",
        "task": "translation",
        "description": "English to French translation"
    },
    "text_generation": {
        "model_name": "gpt2",
        "task": "text-generation",
        "description": "General text generation"
    }
}


def create_llm_manager(model_type: str = "chat") -> LLMModelManager:
    """
    Create an LLM manager with predefined configuration.
    
    Args:
        model_type: Type of model (chat, sentiment, qa, summarize, etc.)
        
    Returns:
        Configured LLMModelManager instance
    """
    if model_type not in PREDEFINED_MODELS:
        available = ", ".join(PREDEFINED_MODELS.keys())
        raise ValueError(f"Unknown model type: {model_type}. Available: {available}")
    
    config = PREDEFINED_MODELS[model_type]
    return LLMModelManager(
        model_name=config["model_name"],
        task=config["task"]
    )