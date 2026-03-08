from fastapi import APIRouter, Depends
from kasa import Discover, Credentials
from ..deps import require_env_vars
from ..arguments import host_map, KASA_PASSWORD, KASA_USERNAME

router = APIRouter(
    prefix="/switches",
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_env_vars)]
)

@router.get("/")
async def get_lights():
    return host_map

@router.get("/{switch_id}")
async def get_switch_status(switch_id: str):
    if (switch_id not in host_map):
        return {"Error": f"Switch ID must be one of: {list(host_map.keys())}"}

    creds = Credentials(username=KASA_USERNAME, password=KASA_PASSWORD)
    dev = await Discover.discover_single(credentials=creds, host=host_map[switch_id])
    await dev.update()
    return {
        "is_on": dev.is_on,
        "alias": dev.alias,
        "host": dev.host,
        "port": dev.port,
        "region": dev.region,
        "location": dev.location,
        "mac_addy": dev.mac
    }
