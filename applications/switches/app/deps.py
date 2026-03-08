import os
from fastapi import HTTPException


async def require_env_vars():
    required = ["KASA_USERNAME", "KASA_PASSWORD"]
    missing = [var for var in required if os.getenv(var) is None]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing environment variables: {', '.join(missing)}"
        )
    
    
