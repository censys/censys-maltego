"""IPAddressToLocation Tranform."""
from canari.maltego.entities import IPv4Address
from canari.maltego.transform import Transform
from canari.maltego.message import MaltegoException
from canari.framework import RequestFilter

from censys_maltego.transforms.common.utils import (
    check_api_creds,
    LOCATION_FIELDS,
    generate_location,
)

__author__ = "Censys Team"
__copyright__ = "Copyright 2021, censys_maltego Project"
__credits__ = ["Aidan Holland"]

__license__ = "Apache-2.0"
__version__ = "0.1"
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
        from censys import CensysIPv4

        c = CensysIPv4()
        # c = CensysIPv4(config["censys.local.api_id"], config["censys.local.api_secret"])
        ip = request.entity.value
        res = list(
            c.search(
                f"ip: {ip} AND location.country: *",
                fields=LOCATION_FIELDS,
                max_records=1,
            )
        )
        if len(res) == 0:
            raise MaltegoException(f"No search results found for {ip}")

        response += generate_location(res[0])

        return response
