"""IPAddressToLocation Tranform."""
from canari.maltego.entities import IPv4Address
from canari.maltego.transform import Transform
from canari.maltego.message import MaltegoException
from canari.framework import RequestFilter

from censys_maltego.transforms.common.entities import Location
from censys_maltego.transforms.common.utils import check_api_creds

__author__ = "Censys Team"
__copyright__ = "Copyright 2021, censys_maltego Project"
__credits__ = ["Aidan Holland"]

__license__ = "Apache-2.0"
__version__ = "0.2"
__maintainer__ = "Censys Team"
__email__ = "support@censys.io"
__status__ = "Development"


@RequestFilter(check_api_creds)
class IPAddressToLocation(Transform):
    """IPv4 Address to Location."""

    # The transform input entity type.
    input_type = IPv4Address

    def do_transform(self, request, response, config):
        """Do Transform."""
        from censys.search import CensysHosts

        c = CensysHosts(
            config["censys.local.api_id"], config["censys.local.api_secret"]
        )
        ip = request.entity.value
        res = c.view(ip)

        location = res.get("location")
        if not location:
            raise MaltegoException(f"No Location found for {ip}")

        coordinates = location.get("coordinates", {})

        location_entity = Location(
            country=location.get("country"),
            countrycode=location.get("country_code"),
            latitude=coordinates.get("latitude"),
            longitude=coordinates.get("longitude"),
            city=location.get("city"),
            area=location.get("province"),
            timezone=location.get("timezone"),
            zipcode=location.get("postal_code"),
        )

        return response + location_entity
