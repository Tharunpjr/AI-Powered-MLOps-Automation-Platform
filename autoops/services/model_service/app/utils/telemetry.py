"""
AutoOps Model Service - Telemetry and Metrics
Telemetry collection and metrics utilities.
"""

import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from prometheus_client import (
    Counter, Histogram, Gauge, Info,
    CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global metrics registry
REGISTRY = CollectorRegistry()

# Service metrics
SERVICE_INFO = Info('autoops_service_info', 'Service information', registry=REGISTRY)
SERVICE_UPTIME = Gauge('autoops_service_uptime_seconds', 'Service uptime in seconds', registry=REGISTRY)
SERVICE_START_TIME = Gauge('autoops_service_start_time_seconds', 'Service start time', registry=REGISTRY)

# Model metrics
MODEL_LOAD_COUNT = Counter('autoops_model_load_total', 'Total model loads', ['status'], registry=REGISTRY)
MODEL_LOAD_DURATION = Histogram('autoops_model_load_duration_seconds', 'Model load duration', registry=REGISTRY)
MODEL_PREDICTION_COUNT = Counter('autoops_model_predictions_total', 'Total predictions', ['model_version'], registry=REGISTRY)
MODEL_PREDICTION_DURATION = Histogram('autoops_model_prediction_duration_seconds', 'Prediction duration', ['model_version'], registry=REGISTRY)
MODEL_ERROR_COUNT = Counter('autoops_model_errors_total', 'Total model errors', ['error_type'], registry=REGISTRY)

# HTTP metrics
HTTP_REQUEST_COUNT = Counter('autoops_http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status_code'], registry=REGISTRY)
HTTP_REQUEST_DURATION = Histogram('autoops_http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'], registry=REGISTRY)

# System metrics
SYSTEM_MEMORY_USAGE = Gauge('autoops_system_memory_usage_bytes', 'System memory usage', registry=REGISTRY)
SYSTEM_CPU_USAGE = Gauge('autoops_system_cpu_usage_percent', 'System CPU usage', registry=REGISTRY)


class TelemetryCollector:
    """Collects and manages telemetry data."""
    
    def __init__(self):
        """Initialize the telemetry collector."""
        self.start_time = time.time()
        self._setup_service_info()
    
    def _setup_service_info(self):
        """Setup service information metrics."""
        SERVICE_INFO.info({
            'service': 'AutoOps Model Service',
            'version': '1.0.0',
            'environment': 'production'
        })
        
        SERVICE_START_TIME.set(self.start_time)
    
    def update_uptime(self):
        """Update service uptime metric."""
        uptime = time.time() - self.start_time
        SERVICE_UPTIME.set(uptime)
    
    def record_model_load(self, success: bool, duration: float):
        """
        Record model load metrics.
        
        Args:
            success: Whether the model load was successful
            duration: Load duration in seconds
        """
        status = "success" if success else "failure"
        MODEL_LOAD_COUNT.labels(status=status).inc()
        MODEL_LOAD_DURATION.observe(duration)
    
    def record_prediction(self, model_version: str, duration: float):
        """
        Record prediction metrics.
        
        Args:
            model_version: Version of the model used
            duration: Prediction duration in seconds
        """
        MODEL_PREDICTION_COUNT.labels(model_version=model_version).inc()
        MODEL_PREDICTION_DURATION.labels(model_version=model_version).observe(duration)
    
    def record_error(self, error_type: str):
        """
        Record error metrics.
        
        Args:
            error_type: Type of error that occurred
        """
        MODEL_ERROR_COUNT.labels(error_type=error_type).inc()
    
    def record_http_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """
        Record HTTP request metrics.
        
        Args:
            method: HTTP method
            endpoint: Request endpoint
            status_code: Response status code
            duration: Request duration in seconds
        """
        HTTP_REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status_code=str(status_code)
        ).inc()
        
        HTTP_REQUEST_DURATION.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
    
    def update_system_metrics(self, memory_usage: float, cpu_usage: float):
        """
        Update system metrics.
        
        Args:
            memory_usage: Memory usage in bytes
            cpu_usage: CPU usage percentage
        """
        SYSTEM_MEMORY_USAGE.set(memory_usage)
        SYSTEM_CPU_USAGE.set(cpu_usage)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get a summary of current metrics.
        
        Returns:
            Dictionary containing metrics summary
        """
        uptime = time.time() - self.start_time
        
        return {
            "service": {
                "uptime_seconds": uptime,
                "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                "status": "running"
            },
            "metrics_available": [
                "model_load_count",
                "model_prediction_count", 
                "http_request_count",
                "system_metrics"
            ]
        }


# Global telemetry collector instance
telemetry_collector = TelemetryCollector()


def setup_telemetry():
    """Setup telemetry collection."""
    logger.info("Setting up telemetry collection")
    telemetry_collector.update_uptime()


def get_metrics() -> str:
    """
    Get Prometheus metrics in text format.
    
    Returns:
        Prometheus metrics in text format
    """
    telemetry_collector.update_uptime()
    return generate_latest(REGISTRY)


def get_metrics_content_type() -> str:
    """
    Get the content type for metrics.
    
    Returns:
        Content type for Prometheus metrics
    """
    return CONTENT_TYPE_LATEST


def record_model_load(success: bool, duration: float):
    """
    Record model load metrics.
    
    Args:
        success: Whether the model load was successful
        duration: Load duration in seconds
    """
    telemetry_collector.record_model_load(success, duration)


def record_prediction(model_version: str, duration: float):
    """
    Record prediction metrics.
    
    Args:
        model_version: Version of the model used
        duration: Prediction duration in seconds
    """
    telemetry_collector.record_prediction(model_version, duration)


def record_error(error_type: str):
    """
    Record error metrics.
    
    Args:
        error_type: Type of error that occurred
    """
    telemetry_collector.record_error(error_type)


def record_http_request(method: str, endpoint: str, status_code: int, duration: float):
    """
    Record HTTP request metrics.
    
    Args:
        method: HTTP method
        endpoint: Request endpoint
        status_code: Response status code
        duration: Request duration in seconds
    """
    telemetry_collector.record_http_request(method, endpoint, status_code, duration)


def get_telemetry_summary() -> Dict[str, Any]:
    """
    Get telemetry summary.
    
    Returns:
        Dictionary containing telemetry summary
    """
    return telemetry_collector.get_metrics_summary()
