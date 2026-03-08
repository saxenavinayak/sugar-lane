from fastapi import FastAPI
from kasa_discovery import light_is_on
from arguments import host_map
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "init"}

@app.get("/lights/{light_name}")
async def get_light_status(light_name):
    if (light_name not in host_map):
        return {"Error": f"Light name must be one of: {list(host_map.keys())}"}
    is_on = await light_is_on(host_map[light_name])
    print(is_on)
    return {"is_on": is_on}

