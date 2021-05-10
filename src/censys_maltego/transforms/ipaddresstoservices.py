"""IPAddressToServices Tranform."""
from canari.maltego.entities import IPv4Address, Service
from canari.maltego.transform import Transform
from canari.maltego.message import MaltegoException
from canari.framework import RequestFilter

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
class IPAddressToServices(Transform):
    """IPv4 Address to Services."""

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
            raise MaltegoException(f"No Services found for {ip}")

        for service in services:
            response += Service(
                service.get("service_name"),
                port=service.get("port"),
                banner=service.get("banner"),
            )

        return response
