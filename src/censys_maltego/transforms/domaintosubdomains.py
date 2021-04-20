from canari.maltego.entities import Domain
from canari.maltego.transform import Transform
from canari.maltego.message import MaltegoException
from canari.framework import EnableDebugWindow, RequestFilter

from censys_maltego.transforms.common.utils import check_api_creds

__author__ = "Censys Team"
__copyright__ = "Copyright 2021, censys_maltego Project"
__credits__ = ["Aidan Holland"]

__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Censys Team"
__email__ = "support@censys.io"
__status__ = "Development"

FIELDS = ["parsed.names"]


@RequestFilter(check_api_creds)
@EnableDebugWindow
class DomainToSubdomains(Transform):
    """Domain to Subdomains."""

    # The transform input entity type.
    input_type = Domain

    def do_transform(self, request, response, config):
        from censys import CensysCertificates

        c = CensysCertificates()
        # c = CensysIPv4(config["censys.local.api_id"], config["censys.local.api_secret"])
        domain = request.entity.value
        res = list(
            c.search(
                f"parsed.names: {domain}",
                fields=FIELDS,
                max_records=config["censys.local.max_records"] or 5,
            )
        )
        if len(res) == 0:
            raise MaltegoException(f"No IPs found for {domain}")

        for result in res:
            for subdomain in result.get("parsed.names"):
                response += Domain(subdomain)

        return response

    def on_terminate(self):
        """This method gets called when transform execution is prematurely terminated. It is only applicable for local
        transforms. It can be excluded if you don't need it."""
        pass
