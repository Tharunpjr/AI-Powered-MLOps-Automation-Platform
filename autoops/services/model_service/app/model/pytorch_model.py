"""
AutoOps PyTorch Model Manager
Deep learning model management with PyTorch support.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union, List

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader


class SimpleNeuralNet(nn.Module):
    """Simple feedforward neural network for regression/classification."""
    
    def __init__(self, input_size: int, hidden_sizes: List[int], output_size: int):
        super(SimpleNeuralNet, self).__init__()
        
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.2))
            prev_size = hidden_size
        
        layers.append(nn.Linear(prev_size, output_size))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)


class TabularDataset(Dataset):
    """PyTorch dataset for tabular data."""
    
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = torch.FloatTensor(X)
        self.y = torch.FloatTensor(y)
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class PyTorchModelManager:
    """Manages PyTorch model loading, saving, training, and inference."""
    
    def __init__(self, model_path: str = "models/pytorch_model.pt"):
        """
        Initialize the PyTorch model manager.
        
        Args:
            model_path: Path to the model file
        """
        self.model_path = Path(model_path)
        self.metadata_path = self.model_path.parent / "pytorch_model_metadata.json"
        self.model: Optional[nn.Module] = None
        self.metadata: Dict[str, Any] = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    def load_model(self) -> bool:
        """
        Load PyTorch model from storage.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not self.model_path.exists():
                print(f"PyTorch model file not found at {self.model_path}")
                return False
            
            checkpoint = torch.load(self.model_path, map_location=self.device)
            
            # Reconstruct model architecture
            model_config = checkpoint.get('model_config', {})
            self.model = SimpleNeuralNet(
                input_size=model_config.get('input_size', 4),
                hidden_sizes=model_config.get('hidden_sizes', [64, 32]),
                output_size=model_config.get('output_size', 1)
            )
            
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.model.to(self.device)
            self.model.eval()
            
            # Load metadata
            self._load_metadata()
            
            print(f"PyTorch model loaded successfully from {self.model_path}")
            return True
            
        except Exception as e:
            print(f"Failed to load PyTorch model: {e}")
            return False
    
    def save_model(
        self, 
        model: nn.Module, 
        model_config: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Save PyTorch model to storage.
        
        Args:
            model: The PyTorch model to save
            model_config: Model architecture configuration
            metadata: Optional metadata to save with the model
            
        Returns:
            True if model saved successfully, False otherwise
        """
        try:
            # Ensure directory exists
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare checkpoint
            checkpoint = {
                'model_state_dict': model.state_dict(),
                'model_config': model_config,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save model
            torch.save(checkpoint, self.model_path)
            
            # Save metadata
            if metadata is None:
                metadata = {}
            
            metadata.update({
                "saved_at": datetime.now().isoformat(),
                "model_type": "PyTorch",
                "model_class": type(model).__name__,
                "model_path": str(self.model_path),
                "device": str(self.device),
                "model_config": model_config
            })
            
            self._save_metadata(metadata)
            
            print(f"PyTorch model saved successfully to {self.model_path}")
            return True
            
        except Exception as e:
            print(f"Failed to save PyTorch model: {e}")
            return False
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """
        Make predictions using the loaded model.
        
        Args:
            features: Input features (numpy array)
            
        Returns:
            Predictions as numpy array
        """
        if self.model is None:
            raise ValueError("No model loaded")
        
        self.model.eval()
        with torch.no_grad():
            X = torch.FloatTensor(features).to(self.device)
            predictions = self.model(X)
            return predictions.cpu().numpy()
    
    def train_model(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        hidden_sizes: List[int] = [64, 32],
        epochs: int = 100,
        batch_size: int = 32,
        learning_rate: float = 0.001
    ) -> Dict[str, Any]:
        """
        Train a PyTorch model.
        
        Args:
            X_train: Training features
            y_train: Training targets
            X_val: Validation features (optional)
            y_val: Validation targets (optional)
            hidden_sizes: Hidden layer sizes
            epochs: Number of training epochs
            batch_size: Batch size
            learning_rate: Learning rate
            
        Returns:
            Training history and metrics
        """
        input_size = X_train.shape[1]
        output_size = 1 if len(y_train.shape) == 1 else y_train.shape[1]
        
        # Reshape targets if needed
        if len(y_train.shape) == 1:
            y_train = y_train.reshape(-1, 1)
        if y_val is not None and len(y_val.shape) == 1:
            y_val = y_val.reshape(-1, 1)
        
        # Create model
        model = SimpleNeuralNet(input_size, hidden_sizes, output_size)
        model.to(self.device)
        
        # Create datasets and dataloaders
        train_dataset = TabularDataset(X_train, y_train)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        
        if X_val is not None and y_val is not None:
            val_dataset = TabularDataset(X_val, y_val)
            val_loader = DataLoader(val_dataset, batch_size=batch_size)
        else:
            val_loader = None
        
        # Loss and optimizer
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        
        # Training history
        history = {
            'train_loss': [],
            'val_loss': []
        }
        
        # Training loop
        for epoch in range(epochs):
            model.train()
            train_loss = 0.0
            
            for batch_X, batch_y in train_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            train_loss /= len(train_loader)
            history['train_loss'].append(train_loss)
            
            # Validation
            if val_loader is not None:
                model.eval()
                val_loss = 0.0
                
                with torch.no_grad():
                    for batch_X, batch_y in val_loader:
                        batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                        outputs = model(batch_X)
                        loss = criterion(outputs, batch_y)
                        val_loss += loss.item()
                
                val_loss /= len(val_loader)
                history['val_loss'].append(val_loss)
                
                if (epoch + 1) % 10 == 0:
                    print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
            else:
                if (epoch + 1) % 10 == 0:
                    print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss:.4f}")
        
        self.model = model
        
        # Save model config
        model_config = {
            'input_size': input_size,
            'hidden_sizes': hidden_sizes,
            'output_size': output_size,
            'epochs': epochs,
            'batch_size': batch_size,
            'learning_rate': learning_rate
        }
        
        return {
            'history': history,
            'model_config': model_config,
            'final_train_loss': history['train_loss'][-1],
            'final_val_loss': history['val_loss'][-1] if val_loader else None
        }
    
    def evaluate_model(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            X_test: Test features
            y_test: Test targets
            
        Returns:
            Dictionary containing evaluation metrics
        """
        if self.model is None:
            raise ValueError("No model loaded")
        
        predictions = self.predict(X_test)
        
        if len(y_test.shape) == 1:
            y_test = y_test.reshape(-1, 1)
        
        mse = np.mean((predictions - y_test) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(predictions - y_test))
        
        # R² score
        ss_res = np.sum((y_test - predictions) ** 2)
        ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        metrics = {
            "mse": float(mse),
            "rmse": float(rmse),
            "mae": float(mae),
            "r2": float(r2)
        }
        
        return metrics
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information and metadata.
        
        Returns:
            Dictionary containing model information
        """
        info = {
            "model_loaded": self.model is not None,
            "model_path": str(self.model_path),
            "device": str(self.device),
            "metadata": self.metadata.copy()
        }
        
        if self.model is not None:
            info.update({
                "model_type": "PyTorch",
                "model_class": type(self.model).__name__,
                "model_version": self.metadata.get("version", "unknown"),
                "last_updated": self.metadata.get("saved_at", "unknown"),
                "parameters": sum(p.numel() for p in self.model.parameters())
            })
        
        return info
    
    def _load_metadata(self) -> None:
        """Load model metadata from file."""
        try:
            if self.metadata_path.exists():
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
        except Exception as e:
            print(f"Failed to load metadata: {e}")
            self.metadata = {}
    
    def _save_metadata(self, metadata: Dict[str, Any]) -> None:
        """Save model metadata to file."""
        try:
            with open(self.metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            self.metadata = metadata
        except Exception as e:
            print(f"Failed to save metadata: {e}")
