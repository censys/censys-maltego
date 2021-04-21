import re

from canari.maltego.entities import Location
from canari.maltego.message import Field

LOCATION_FIELDS = [
    "location.latitude",
    "location.longitude",
    "location.country",
    "location.country_code",
    "location.city",
    "location.province",
    "location.timezone",
]
RE_IP_PATTERN = re.compile(
    "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
)


def generate_location(res: dict):
    location = Location(
        country=res.get("location.country", "Unknown"),
        countrycode=res.get("location.country_code"),
        latitude=res.get("location.latitude"),
        longitude=res.get("location.longitude"),
        city=res.get("location.city"),
        area=res.get("location.province"),
    )
    timezone = res.get("location.timezone")
    if timezone:
        location += Field("location.timezone", timezone, display_name="Timezone")
    return location


def check_api_creds(request, response, config):
    if config["censys.local.api_id"] == "YOUR_API_ID":
        config["censys.local.api_id"] = None
    if config["censys.local.api_secret"] == "YOUR_API_SECRET":
        config["censys.local.api_id"] = None


def is_ip(string) -> bool:
    return bool(re.search(RE_IP_PATTERN, string))
