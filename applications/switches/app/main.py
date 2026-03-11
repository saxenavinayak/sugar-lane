from fastapi import Depends, FastAPI

from .deps import require_env_vars
from .routers import get_switch, health

app = FastAPI(dependencies=[Depends(require_env_vars)])


app.include_router(get_switch.router)
app.include_router(health.router)


@app.get("/")
async def root():
    return {"message": "Switch status"}