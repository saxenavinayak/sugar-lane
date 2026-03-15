import os
from fastapi import HTTPException, status

# Required ENV VARS
async def require_env_vars():
    required = ["KASA_USERNAME", "KASA_PASSWORD"]
    missing = [var for var in required if os.getenv(var) is None]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing environment variables: {', '.join(missing)}"
        )
    
    
