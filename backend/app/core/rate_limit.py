import time
from collections import defaultdict
from typing import Dict, List
from fastapi import Request, HTTPException, status

class InMemoryRateLimiter:
    """
    Sliding window in-memory rate limiter with automatic cleanup.
    Provides protection against brute-force and spamming attacks.
    """
    def __init__(self):
        self._requests: Dict[str, List[float]] = defaultdict(list)
        
    def check_rate_limit(self, key: str, max_requests: int, window_seconds: int):
        now = time.time()
        window_start = now - window_seconds
        
        # Clean requests older than the sliding window
        self._requests[key] = [t for t in self._requests[key] if t > window_start]
        
        if len(self._requests[key]) >= max_requests:
            retry_after = int(window_seconds - (now - self._requests[key][0]))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Límite de solicitudes excedido. Por favor intente de nuevo en {max(1, retry_after)} segundos.",
                headers={"Retry-After": str(max(1, retry_after))}
            )
            
        self._requests[key].append(now)

limiter = InMemoryRateLimiter()

def rate_limit_login(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    key = f"login:{client_ip}"
    # Max 5 login attempts per minute per IP
    limiter.check_rate_limit(key=key, max_requests=5, window_seconds=60)

def rate_limit_tips(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    key = f"tips:{client_ip}"
    # Max 10 confidential tips per 10 minutes per IP
    limiter.check_rate_limit(key=key, max_requests=10, window_seconds=600)

def rate_limit_register(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    key = f"register:{client_ip}"
    # Max 3 account registrations per 10 minutes per IP to prevent automated bot flooding
    limiter.check_rate_limit(key=key, max_requests=3, window_seconds=600)
