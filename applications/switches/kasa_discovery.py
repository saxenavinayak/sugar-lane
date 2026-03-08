import asyncio
import time

from kasa import Discover, Credentials
from applications.switches.app.arguments import KASA_USERNAME, KASA_PASSWORD, DeviceHosts

async def light_is_on(light_name):
    creds = Credentials(username=KASA_USERNAME, password=KASA_PASSWORD)
    dev = await Discover.discover_single(credentials=creds, host=light_name)
    await dev.update()
    return dev.is_on

    

# async def main():
#     creds = Credentials(username=KASA_USERNAME, password=KASA_PASSWORD)
#     dev = await Discover.discover_single(credentials=creds, host=DeviceHosts.vin_bedroom.value)
#     await dev.turn_on()
#     time.sleep(5)
#     await dev.turn_off()

# if __name__ == "__main__":
#     asyncio.run(main())

