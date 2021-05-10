"""CertificateContext Tranform."""
from typing import List, Optional

from canari.maltego.entities import Domain, Organization, Location, IPv4Address, Entity
from canari.maltego.transform import Transform
from canari.framework import RequestFilter

from censys_maltego.transforms.common.entities import SSLCertificate
from censys_maltego.transforms.common.utils import (
    check_api_creds,
    list_to_string,
    is_ipv4,
)

__author__ = "Censys Team"
__copyright__ = "Copyright 2021, censys_maltego Project"
__credits__ = ["Aidan Holland"]

__license__ = "Apache-2.0"
__version__ = "0.1"
__maintainer__ = "Censys Team"
__email__ = "support@censys.io"
__status__ = "Development"


def json_to_entity(json: dict, link: Optional[str] = None) -> List[Entity]:
    """Censys JSON response to entities.

    Args:
        json (dict): Censys JSON response.
        link (str): Optional; Link label for entity relationships.

    Returns:
        List[Entity]: List of entities to respond.
    """
    entities: List[Entity] = []
    kwargs = {}
    if link:
        kwargs["link_label"] = link

    country = list_to_string(json.get("country", []))
    if country:
        entities.append(
            Location(
                country=list_to_string(json.get("country", [])),
                area=list_to_string(json.get("province", [])),
                city=list_to_string(json.get("locality", [])),
                **kwargs
            )
        )

    org = list_to_string(json.get("organization", []))
    if org:
        entities.append(Organization(org, **kwargs))

    return entities


@RequestFilter(check_api_creds)
class CertificateContext(Transform):
    """Certificate to Domains, Organizations, Locations."""

    # The transform input entity type.
    input_type = SSLCertificate

    def do_transform(self, request, response, config):
        """Do Transform."""
        from censys.search import CensysCertificates

        provided_cert = request.entity

        c = CensysCertificates(
            config["censys.local.api_id"], config["censys.local.api_secret"]
        )

        if hasattr(provided_cert, "fingerprint"):
            res = c.view(provided_cert.fingerprint)
            parsed = res.get("parsed")

            entities = json_to_entity(parsed.get("subject"), link="Subject")
            entities.extend(json_to_entity(parsed.get("issuer"), link="Issuer"))

            for entity in entities:
                response += entity

            for name in parsed.get("names", []):
                if is_ipv4(name):
                    response += IPv4Address(name)
                else:
                    response += Domain(name)

        return response
