from fastapi import APIRouter, Depends, HTTPException, status
from kasa import Discover, Credentials, TimeoutError
from pydantic import BaseModel
from ..deps import require_env_vars
from ..arguments import host_map, KASA_PASSWORD, KASA_USERNAME

# Health check if switches are reachable

router = APIRouter(
    prefix="/health",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    dependencies=[Depends(require_env_vars)]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_health_of_switches():
    # Returns first unavailable device, OK otherwise
    creds = Credentials(username=KASA_USERNAME, password=KASA_PASSWORD)
    for key,value in host_map.items():
        try:
            dev = await Discover.discover_single(credentials=creds, host=value)
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Device {key} with host {value} not reachable"
            )
    return {
        status.HTTP_200_OK: "All devices reachable"
        }
    

        


