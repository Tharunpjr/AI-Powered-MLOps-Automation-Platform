"""
AutoOps CLI - Start Command
Command to start AutoOps services.
"""

import subprocess
import time
import requests
from typing import Dict, Any


def start_service(
    service: str = "all",
    port: int = 8000,
    host: str = "0.0.0.0",
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Start AutoOps services.
    
    Args:
        service: Service to start ("model" or "all")
        port: Port for model service
        host: Host for model service
        verbose: Enable verbose output
        
    Returns:
        Dictionary with start result
    """
    try:
        if service in ["model", "all"]:
            return start_model_service(port, host, verbose)
        else:
            return {
                "success": False,
                "error": f"Unknown service: {service}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def start_model_service(
    port: int = 8000,
    host: str = "0.0.0.0",
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Start the model service.
    
    Args:
        port: Port for model service
        host: Host for model service
        verbose: Enable verbose output
        
    Returns:
        Dictionary with start result
    """
    try:
        # Change to model service directory
        import os
        os.chdir("services/model_service")
        
        # Set environment variables
        env = os.environ.copy()
        env["PYTHONPATH"] = "../../"
        env["MODEL_PATH"] = "../../models/model.pkl"
        env["LOG_LEVEL"] = "INFO" if verbose else "WARNING"
        
        # Build uvicorn command
        cmd = [
            "python", "-m", "uvicorn",
            "app.main:app",
            "--host", host,
            "--port", str(port),
            "--reload"
        ]
        
        if verbose:
            cmd.append("--log-level")
            cmd.append("info")
        
        print(f"🚀 Starting model service on {host}:{port}")
        
        # Start the service
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for startup
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Model service started successfully")
            print(f"📖 API documentation: http://{host}:{port}/docs")
            print(f"🏥 Health check: http://{host}:{port}/health")
            print(f"📊 Metrics: http://{host}:{port}/metrics")
            
            return {
                "success": True,
                "process": process,
                "url": f"http://{host}:{port}"
            }
        else:
            # Process exited, get error
            stdout, stderr = process.communicate()
            return {
                "success": False,
                "error": f"Service failed to start: {stderr}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def wait_for_service(url: str, timeout: int = 30) -> bool:
    """
    Wait for service to be ready.
    
    Args:
        url: Service URL
        timeout: Timeout in seconds
        
    Returns:
        True if service is ready, False otherwise
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
        
        time.sleep(1)
    
    return False
