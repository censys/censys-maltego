"""IPAddressToCertificate Tranform."""
from canari.maltego.entities import IPv4Address
from canari.maltego.transform import Transform
from canari.maltego.message import MaltegoException
from canari.framework import EnableDebugWindow, RequestFilter

from censys_maltego.transforms.common.utils import check_api_creds, list_to_string
from censys_maltego.transforms.common.entities import SSLCertificate

__author__ = "Censys Team"
__copyright__ = "Copyright 2021, censys_maltego Project"
__credits__ = ["Aidan Holland"]

__license__ = "Apache-2.0"
__version__ = "0.1"
__maintainer__ = "Censys Team"
__email__ = "support@censys.io"
__status__ = "Development"

FIELDS_MAPPING = {
    "subject": "443.https.tls.certificate.parsed.subject.common_name",
    "fingerprint": "443.https.tls.certificate.parsed.fingerprint_sha256",
    "organization": "443.https.tls.certificate.parsed.subject.organization",
    "subjectDN": "443.https.tls.certificate.parsed.subject_dn",
    "issuer": "443.https.tls.certificate.parsed.issuer.common_name",
    "issuerDN": "443.https.tls.certificate.parsed.issuer_dn",
    "serial": "443.https.tls.certificate.parsed.serial_number",
    "country": "443.https.tls.certificate.parsed.issuer.country",
    "validFrom": "443.https.tls.certificate.parsed.validity.start",
    "validTo": "443.https.tls.certificate.parsed.validity.end",
    "san": "443.https.tls.certificate.parsed.extensions.subject_alt_name.dns_names",
    "usage": "443.https.tls.certificate.parsed.extensions.subject_alt_name.ip_addresses",
}
FIELDS_TYPES = {
    "subject": str,
    "organization": str,
    "issuer": str,
    "country": str,
    "san": list,
    "usage": list,
}


@RequestFilter(check_api_creds)
@EnableDebugWindow
class IPAddressToCertificate(Transform):
    """IPv4 Address to Certificate."""

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
                f"ip: {ip} AND 443.https.tls.certificate.parsed.fingerprint_sha256: *",
                fields=list(FIELDS_MAPPING.values()),
                max_records=1,
            )
        )
        if len(res) == 0:
            raise MaltegoException(f"No search results found for {ip}")

        result = res[0]

        kwargs = {}
        for kw, censys_field in FIELDS_MAPPING.items():
            value = result.get(censys_field)
            expected_type = FIELDS_TYPES.get(kw, str)
            if not isinstance(value, expected_type) and isinstance(value, list):
                value = list_to_string(value)
            kwargs[kw] = value

        if "usage" in kwargs:
            new_usage = []
            for use in kwargs.get("usage"):
                new_usage.append(use.strip())
            kwargs["usage"] = new_usage

        if "fingerprint" in kwargs:
            fingerprint = kwargs.get("fingerprint")
            kwargs["censys_url"] = f"https://censys.io/certificates/{fingerprint}"

        response += SSLCertificate(**kwargs)

        return response
