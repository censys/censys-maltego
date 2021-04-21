"""Common Entities for our tranforms."""
from canari.maltego.entities import IPv4Address
from canari.maltego.message import (
    Entity,
    StringEntityField,
    ArrayEntityField,
    IntegerEntityField,
)

__author__ = "Censys Team"
__copyright__ = "Copyright 2021, censys Project"
__credits__ = ["Aidan Holland"]

__license__ = "Apache-2.0"
__version__ = "0.1"
__maintainer__ = "Censys Team"
__email__ = "support@censys.io"
__status__ = "Development"

__all__ = ["CensysEntity", "SSLCertificate", "IPv6Address"]


class CensysEntity(Entity):
    """Censys Base Entity."""

    pass


class SSLCertificate(Entity):
    """SSL Certificate Entity.

    Goes by 'maltego.X509Certificate' in Maltego.
    """

    _category_ = "Infrastructure"
    _type_ = "maltego.X509Certificate"
    subject = StringEntityField("subject", display_name="Subject", is_value=True)
    issuer = StringEntityField("issuer", display_name="Issuer")
    subjectDN = StringEntityField("subjectDN", display_name="Subject DN")
    issuerDN = StringEntityField("issuerDN", display_name="Issuer DN")
    ski = StringEntityField("ski", display_name="SKI")
    aki = StringEntityField("aki", display_name="AKI")
    serial = StringEntityField("serial", display_name="Serial")
    san = ArrayEntityField("san", display_name="SAN")
    usage = ArrayEntityField("usage", display_name="Usage")
    issuanceid = IntegerEntityField("issuanceid", display_name="Issuance ID")
    validFrom = StringEntityField("validFrom", display_name="Valid From")
    validTo = StringEntityField("validTo", display_name="Valid Until")
    country = StringEntityField("country", display_name="Country")
    organization = StringEntityField("organization", display_name="Organization")
    # These are additional Censys specific fields
    fingerprint = StringEntityField("fingerprint", display_name="SHA-256 Fingerprint")
    censys_url = StringEntityField("censys_url", display_name="Censys URL")


class IPv6Address(IPv4Address):
    """IPv6 Address Entity."""

    _type_ = "maltego.IPv6Address"
