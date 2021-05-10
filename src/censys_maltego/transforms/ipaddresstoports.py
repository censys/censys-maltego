"""IPAddressToPorts Tranform."""
from canari.maltego.entities import IPv4Address, Port
from canari.maltego.transform import Transform
from canari.maltego.message import MaltegoException
from canari.framework import RequestFilter

from censys_maltego.transforms.common.utils import check_api_creds

__author__ = "Censys Team"
__copyright__ = "Copyright 2021, censys_maltego Project"
__credits__ = ["Art Sturdevant", "Aidan Holland"]

__license__ = "Apache-2.0"
__version__ = "0.2"
__maintainer__ = "Censys Team"
__email__ = "support@censys.io"
__status__ = "Development"

FIELDS = ["ports"]


@RequestFilter(check_api_creds)
class IPAddressToPorts(Transform):
    """IPv4 Address to Ports."""

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

        services = res.get("services", [])

        if len(services) == 0:
            raise MaltegoException(f"No Ports found for {ip}")

        for service in services:
            response += Port(service.get("port"))

        return response
