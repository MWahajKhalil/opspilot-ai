import os
import secrets
from typing import Optional 

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
#Credential location: X-API-Key header
#Missing automatically fails? No—our code will decide


api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)

def require_api_key(
    api_key: Optional[str] = Security(api_key_header),
) -> None:
    expected_api_key = os.getenv("OPSPILOT_API_KEY") # Read the expected key from server configuration.
    if not expected_api_key:
        raise HTTPException(
            status_code=503,
            detail="API authentication is not configured",
        ) # If no key is configured on the server, refuse all requests
    

    if api_key is None or not secrets.compare_digest(
        api_key,
        expected_api_key,
    ):
        raise HTTPException(
            status_code=401,
        detail="Invalid or missing API key",
    )

    


