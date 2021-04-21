"""CertificateToIPAddresses Tranform."""
from canari.maltego.entities import IPv4Address
from canari.maltego.transform import Transform
from canari.maltego.message import MaltegoException
from canari.framework import RequestFilter

from censys_maltego.transforms.common.utils import check_api_creds
from censys_maltego.transforms.common.entities import SSLCertificate, IPv6Address

__author__ = "Censys Team"
__copyright__ = "Copyright 2021, censys_maltego Project"
__credits__ = ["Aidan Holland"]

__license__ = "Apache-2.0"
__version__ = "0.1"
__maintainer__ = "Censys Team"
__email__ = "support@censys.io"
__status__ = "Development"

FIELDS = ["ip"]


@RequestFilter(check_api_creds)
class CertificateToIPAddresses(Transform):
    """Certificate To IP Addresses."""

    # The transform input entity type.
    input_type = SSLCertificate

    def do_transform(self, request, response, config):
        """Do Transform."""
        from censys import CensysIPv4

        entity = request.entity

        ip_addresses = []

        if hasattr(entity, "usage"):
            usage = entity.usage
            if isinstance(usage, list) and len(usage) > 0:
                ip_addresses.extend(usage)

        if not hasattr(entity, "fingerprint"):
            raise MaltegoException(f"No fingerprint found for {entity.value}")

        c = CensysIPv4()
        # c = CensysIPv4(config["censys.local.api_id"], config["censys.local.api_secret"])
        fingerprint = entity.fingerprint
        res = list(
            c.search(
                f"{fingerprint}",
                fields=FIELDS,
                max_records=config["censys.local.max_records"] or 5,
            )
        )
        if len(res) == 0:
            raise MaltegoException(f"No search results found for {fingerprint}")

        ip_addresses.extend([host.get("ip") for host in res])

        for ip in ip_addresses:
            ip = ip.strip()
            if ":" in ip:
                response += IPv6Address(ip)
            else:
                response += IPv4Address(ip)

        return response
