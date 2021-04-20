from canari.maltego.entities import Location

LOCATION_FIELDS = [
    "location.latitude",
    "location.longitude",
    "location.country",
    "location.country_code",
]


def generate_location(res: dict):
    return Location(
        country=res.get("location.country", "Unknown"),
        countrycode=res.get("location.country_code"),
        latitude=res.get("location.latitude"),
        longitude=res.get("location.longitude"),
    )


def check_api_creds(request, response, config):
    if config["censys.local.api_id"] == "YOUR_API_ID":
        config["censys.local.api_id"] = None
    if config["censys.local.api_secret"] == "YOUR_API_SECRET":
        config["censys.local.api_id"] = None
