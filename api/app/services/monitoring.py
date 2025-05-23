"""Monitoring module for the API."""
import logging
import time
from datetime import datetime

import prometheus_client
from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Gauge, Histogram
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
logger = logging.getLogger(__name__)

# Define metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total count of requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
)
ACTIVE_REQUESTS = Gauge(
    "http_requests_active", "Active requests", ["method", "endpoint"]
)
ERROR_COUNT = Counter(
    "http_request_errors_total", "Total count of errors", ["method", "endpoint"]
)
TENANT_REQUEST_COUNT = Counter(
    "tenant_requests_total",
    "Total count of requests per tenant",
    ["tenant_id", "method", "endpoint"],
)
EMBEDDING_GENERATION_COUNT = Counter(
    "embedding_generation_total", "Total count of embedding generations", ["tenant_id"]
)
EMBEDDING_GENERATION_ERROR_COUNT = Counter(
    "embedding_generation_errors_total",
    "Total count of embedding generation errors",
    ["tenant_id"],
)
RAG_QUERY_COUNT = Counter(
    "rag_query_total", "Total count of RAG queries", ["tenant_id"]
)
RAG_QUERY_ERROR_COUNT = Counter(
    "rag_query_errors_total", "Total count of RAG query errors", ["tenant_id"]
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting Prometheus metrics."""

    async def dispatch(self, request: Request, call_next):
        """Process the request and collect metrics."""
        method = request.method
        path = request.url.path
        tenant_id = request.headers.get("X-Tenant-ID", "unknown")

        # Track request count and latency
        ACTIVE_REQUESTS.labels(method=method, endpoint=path).inc()
        start_time = time.time()

        # Process the request
        try:
            response = await call_next(request)
            status_code = response.status_code

            # Record metrics
            REQUEST_COUNT.labels(
                method=method, endpoint=path, status=status_code
            ).inc()
            TENANT_REQUEST_COUNT.labels(
                tenant_id=tenant_id, method=method, endpoint=path
            ).inc()

            # Log the request
            logger.info(
                f"Request: {method} {path} - Status: {status_code} - "
                f"Tenant: {tenant_id}"
            )

            return response
        except Exception:
            # Record error metrics
            ERROR_COUNT.labels(method=method, endpoint=path).inc()
            logger.error(f"Error processing request: {method} {path}")
            raise
        finally:
            # Record latency and decrement active requests
            request_latency = time.time() - start_time
            REQUEST_LATENCY.labels(method=method, endpoint=path).observe(
                request_latency
            )
            ACTIVE_REQUESTS.labels(method=method, endpoint=path).dec()


def track_embedding_generation(tenant_id: str, success: bool = True):
    """Track embedding generation metrics."""
    EMBEDDING_GENERATION_COUNT.labels(tenant_id=tenant_id).inc()
    if not success:
        EMBEDDING_GENERATION_ERROR_COUNT.labels(tenant_id=tenant_id).inc()
        logger.error(f"Embedding generation failed for tenant: {tenant_id}")
    else:
        logger.info(f"Embedding generation succeeded for tenant: {tenant_id}")


def track_rag_query(tenant_id: str, success: bool = True):
    """Track RAG query metrics."""
    RAG_QUERY_COUNT.labels(tenant_id=tenant_id).inc()
    if not success:
        RAG_QUERY_ERROR_COUNT.labels(tenant_id=tenant_id).inc()
        logger.error(f"RAG query failed for tenant: {tenant_id}")
    else:
        logger.info(f"RAG query succeeded for tenant: {tenant_id}")


def setup_monitoring(app: FastAPI):
    """Set up monitoring for the FastAPI application."""
    # Add Prometheus middleware
    app.add_middleware(PrometheusMiddleware)

    # Add Prometheus metrics endpoint
    @app.get("/metrics")
    async def metrics():
        """Expose Prometheus metrics."""
        return Response(
            prometheus_client.generate_latest(),
            media_type="text/plain",
        )

    # Add health check endpoint
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
        }

    # Add readiness check endpoint
    @app.get("/ready")
    async def ready():
        """Readiness check endpoint."""
        # In a real application, this would check database connectivity,
        # external service availability, etc.
        try:
            # Perform any necessary checks here
            return {
                "status": "ready",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception:
            return {
                "status": "not ready",
                "timestamp": datetime.now().isoformat(),
            }

    logger.info("Monitoring setup complete")
