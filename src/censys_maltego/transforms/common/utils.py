"""Common Utilities for our tranforms."""
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
    r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
)


def generate_location(res: dict) -> Location:
    """Generate a Location Entity from a Censys search response.

    Args:
        res (dict): A Censys search response.

    Returns:
        canari.maltego.entities.Location: A location for a given asset.
    """
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
    """Check if API credentials are default.

    If they are not changed from the config. It is set to None.
    This is to be used with canari.framework.RequestFilter.

    Args:
        request: A MaltegoTransformRequest object.
        response: A MaltegoTransformResponse object.
        config: A CanariConfig object.
    """
    if config["censys.local.api_id"] == "YOUR_API_ID":
        config["censys.local.api_id"] = None
    if config["censys.local.api_secret"] == "YOUR_API_SECRET":
        config["censys.local.api_id"] = None


def is_ip(string: str) -> bool:
    """Check if the string is a valid IPv4 IP Address.

    Args:
        string (str): String to check.

    Returns:
        bool: If string is an IP.
    """
    return bool(re.search(RE_IP_PATTERN, string))


def list_to_string(lst: list = []) -> str:
    """Join list with commas.

    Args:
        lst (list): List to join.

    Returns:
        str: Joined list.
    """
    return ", ".join(lst)
