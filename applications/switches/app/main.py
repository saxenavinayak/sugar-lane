from fastapi import Depends, FastAPI

from .deps import kasa_token_is_set
from .routers import get_light_status

app = FastAPI(dependencies=[Depends(kasa_token_is_set)])


app.include_router(get_light_status.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}