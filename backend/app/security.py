import logging
import os
import secrets
from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


def require_api_key(
    api_key: Optional[str] = Security(api_key_header),
) -> None:
    expected_api_key = os.getenv("OPSPILOT_API_KEY")
    if not expected_api_key:
        logger.error("api_authentication_not_configured")
        raise HTTPException(
            status_code=503,
            detail="API authentication is not configured",
        )

    if api_key is None or not secrets.compare_digest(
        api_key,
        expected_api_key,
    ):
        logger.warning("api_authentication_failed")
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
        )
