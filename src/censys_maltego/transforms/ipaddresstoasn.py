"""IPAddressToASN Tranform."""
from canari.maltego.entities import IPv4Address
from canari.maltego.transform import Transform
from canari.maltego.message import MaltegoException
from canari.framework import RequestFilter

from censys_maltego.transforms.common.entities import AS
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
class IPAddressToASN(Transform):
    """IPv4 Address to ASN."""

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

        autonomous_system = res.get("autonomous_system")
        if not autonomous_system:
            raise MaltegoException(f"No Autonomous System found for {ip}")

        asn = AS(
            autonomous_system.get("asn"),
            name=autonomous_system.get("name"),
            countrycode=autonomous_system.get("country_code"),
        )

        return response + asn
