# Env vars for host names, credentials, etc.
import os
from enum import Enum
# Credentials
KASA_USERNAME = os.getenv("KASA_USERNAME", default="example@google.com")
KASA_PASSWORD = os.getenv("KASA_PASSWORD", default="lol_you_thought")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", default="some_key12345")

# For now, these are hardcoded static IPs as we might get timeouts using Discover.discover
# In the future, we can add healthChecks for each address here on port 80 to see if a host changed
host_map = {
    "vin_bedroom": "10.0.0.84",
    "front_potlights": "10.0.0.158"
}

class DeviceHosts(Enum):
    vin_bedroom = "10.0.0.84"
    front_potlights = "10.0.0.155"
    
