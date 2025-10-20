"""
AutoOps CLI - Status Command
Command to check AutoOps service status.
"""

import requests
import json
from typing import Dict, Any, Optional


def check_status(
    service: str = "all",
    url: str = "http://localhost:8000",
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Check AutoOps service status.
    
    Args:
        service: Service to check ("model" or "all")
        url: Service URL
        verbose: Enable verbose output
        
    Returns:
        Dictionary with status result
    """
    try:
        if service in ["model", "all"]:
            return check_model_service_status(url, verbose)
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


def check_model_service_status(
    url: str = "http://localhost:8000",
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Check model service status.
    
    Args:
        url: Service URL
        verbose: Enable verbose output
        
    Returns:
        Dictionary with status result
    """
    try:
        # Check health endpoint
        health_result = check_health_endpoint(url)
        if not health_result["success"]:
            return health_result
        
        # Check readiness endpoint
        readiness_result = check_readiness_endpoint(url)
        if not readiness_result["success"]:
            return readiness_result
        
        # Get detailed status if verbose
        status_info = {}
        if verbose:
            status_info = get_detailed_status(url)
        
        return {
            "success": True,
            "service": "model",
            "url": url,
            "health": health_result["data"],
            "readiness": readiness_result["data"],
            "status": status_info
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def check_health_endpoint(url: str) -> Dict[str, Any]:
    """
    Check health endpoint.
    
    Args:
        url: Service URL
        
    Returns:
        Dictionary with health check result
    """
    try:
        response = requests.get(f"{url}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": data
            }
        else:
            return {
                "success": False,
                "error": f"Health check failed with status {response.status_code}"
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Health check failed: {str(e)}"
        }


def check_readiness_endpoint(url: str) -> Dict[str, Any]:
    """
    Check readiness endpoint.
    
    Args:
        url: Service URL
        
    Returns:
        Dictionary with readiness check result
    """
    try:
        response = requests.get(f"{url}/health/ready", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": data
            }
        else:
            return {
                "success": False,
                "error": f"Readiness check failed with status {response.status_code}"
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Readiness check failed: {str(e)}"
        }


def get_detailed_status(url: str) -> Dict[str, Any]:
    """
    Get detailed service status.
    
    Args:
        url: Service URL
        
    Returns:
        Dictionary with detailed status information
    """
    try:
        # Get status endpoint
        response = requests.get(f"{url}/health/status", timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Status endpoint failed with status {response.status_code}"
            }
            
    except requests.RequestException as e:
        return {
            "error": f"Status endpoint failed: {str(e)}"
        }


def check_metrics_endpoint(url: str) -> Dict[str, Any]:
    """
    Check metrics endpoint.
    
    Args:
        url: Service URL
        
    Returns:
        Dictionary with metrics check result
    """
    try:
        response = requests.get(f"{url}/metrics", timeout=10)
        
        if response.status_code == 200:
            return {
                "success": True,
                "metrics_available": True,
                "content_type": response.headers.get("content-type", "unknown")
            }
        else:
            return {
                "success": False,
                "error": f"Metrics endpoint failed with status {response.status_code}"
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Metrics endpoint failed: {str(e)}"
        }


def format_status_output(status: Dict[str, Any]) -> str:
    """
    Format status output for display.
    
    Args:
        status: Status dictionary
        
    Returns:
        Formatted status string
    """
    if not status["success"]:
        return f"❌ Service is not healthy: {status['error']}"
    
    output = ["✅ Service is healthy"]
    
    # Add health information
    if "health" in status:
        health = status["health"]
        output.append(f"  Status: {health.get('status', 'unknown')}")
        output.append(f"  Service: {health.get('service', 'unknown')}")
        output.append(f"  Version: {health.get('version', 'unknown')}")
        output.append(f"  Uptime: {health.get('uptime', 'unknown')} seconds")
    
    # Add readiness information
    if "readiness" in status:
        readiness = status["readiness"]
        output.append(f"  Model loaded: {readiness.get('model_loaded', 'unknown')}")
        output.append(f"  Model version: {readiness.get('model_version', 'unknown')}")
    
    return "\n".join(output)
