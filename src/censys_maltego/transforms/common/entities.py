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

__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Censys Team"
__email__ = "support@censys.io"
__status__ = "Development"

__all__ = ["CensysEntity", "SSLCertificate", "IPv6Address"]


class CensysEntity(Entity):
    """This is the base entity used to optionally define the namespace for all your other entities. The namespace is the
    string preceding the name of your entity separated by a dot (i.e. 'foo' in 'foo.BarTransform'). If _namespace_ is
    not defined as a class variable, then the namespace will be generated based on the name of your Canari package. For
    example, if your project's name is 'sniffmypackets' then the namespace will also be 'sniffmypackets'.
    """

    pass


class SSLCertificate(Entity):
    _category_ = "Infrastructure"
    _type_ = "maltego.X509Certificate"
    subject = StringEntityField(
        "subject", display_name="Subject", is_value=True
    )
    issuer = StringEntityField("issuer", display_name="Issuer")
    subjectDN = StringEntityField("subjectDN", display_name="Subject DN")
    issuerDN = StringEntityField("issuerDN", display_name="Issuer DN")
    ski = StringEntityField("ski", display_name="SKI")
    aki = StringEntityField("aki", display_name="AKI")
    serial = StringEntityField("serial", display_name="Serial")
    san = ArrayEntityField("san", display_name="SAN")
    usage = ArrayEntityField("usage", display_name="Usage")
    issuanceid = IntegerEntityField(
        "issuanceid", display_name="Issuance ID"
    )
    validFrom = StringEntityField("validFrom", display_name="Valid From")
    validTo = StringEntityField("validTo", display_name="Valid Until")
    country = StringEntityField("country", display_name="Country")
    organization = StringEntityField(
        "organization", display_name="Organization"
    )
    fingerprint = StringEntityField("fingerprint", display_name="SHA-256 Fingerprint")
    censys_url  = StringEntityField("censys_url", display_name="Censys URL")

class IPv6Address(IPv4Address):
    _type_ = "maltego.IPv6Address"