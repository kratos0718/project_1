import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.utils.logger import correlation_id_ctx_var, logger

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract correlation ID from headers or generate a new one
        correlation_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Set the correlation ID in the context variable
        token = correlation_id_ctx_var.set(correlation_id)
        
        try:
            logger.info(f"Incoming request: {request.method} {request.url.path}")
            response = await call_next(request)
            # Attach the correlation ID to the response header
            response.headers["X-Request-ID"] = correlation_id
            logger.info(f"Completed request: {request.method} {request.url.path} with status {response.status_code}")
            return response
        finally:
            correlation_id_ctx_var.reset(token)
