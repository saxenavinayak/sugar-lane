import asyncio
import time

from kasa import Discover, Credentials
from arguments import KASA_USERNAME, KASA_PASSWORD, DeviceHosts


async def main():
    creds = Credentials(username=KASA_USERNAME, password=KASA_PASSWORD)
    dev = await Discover.discover_single(credentials=creds, host=DeviceHosts.vin_bedroom.value)
    await dev.turn_on()
    time.sleep(5)
    await dev.turn_off()

if __name__ == "__main__":
    asyncio.run(main())

