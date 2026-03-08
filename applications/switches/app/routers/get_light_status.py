from fastapi import APIRouter, Depends
from ..deps import kasa_token_is_set




router = APIRouter(
    prefix="/lights",
    tags=["lights"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(kasa_token_is_set)]
)

@router.get("/")
async def get_lights():
    return {"all lights": "all"}

@router.get("/{switch_id}")
async def get_switch_status(switch_id: str):
    return {"is_on": True}
