import pytest
import responses

from canari.maltego.message import (
    MaltegoException,
    MaltegoTransformRequestMessage,
    MaltegoTransformResponseMessage,
)
from canari.maltego.entities import Domain, IPv4Address

from censys_maltego.transforms.common.utils import is_ipv4
from censys_maltego.transforms.domaintosubdomains import DomainToSubdomains

from .utils import TestCase

SEARCH_CERTIFICATE_JSON = {
    "results": [{"parsed.names": [f"1.1.{i}.{j}" for j in range(3)]} for i in range(4)]
    + [{"parsed.names": ["google.com", "drive.google.com"]}],
    "metadata": {"pages": 1},
}


class TestDomainToSubdomains(TestCase):
    tranform = DomainToSubdomains()

    def test_do_transform(self):
        self.responses.add(
            responses.POST,
            f"{self.v1_api_on_v2_base_url}/search/certificates",
            status=200,
            json=SEARCH_CERTIFICATE_JSON,
        )

        request = MaltegoTransformRequestMessage()
        request += Domain(self.test_domain)
        response = MaltegoTransformResponseMessage()
        actual = self.tranform.do_transform(request, response, self.config)

        for result in SEARCH_CERTIFICATE_JSON["results"]:
            for subdomain in result.get("parsed.names"):
                if is_ipv4(subdomain):
                    response += IPv4Address(subdomain)
                else:
                    response += Domain(subdomain)
        assert actual == response

    def test_no_location_transform(self):
        no_asn_json = SEARCH_CERTIFICATE_JSON.copy()
        no_asn_json["results"] = []
        self.responses.add(
            responses.POST,
            f"{self.v1_api_on_v2_base_url}/search/certificates",
            status=200,
            json=no_asn_json,
        )

        request = MaltegoTransformRequestMessage()
        request += Domain(self.test_domain)
        with pytest.raises(
            MaltegoException, match=f"No Certificates found for {self.test_domain}"
        ):
            self.tranform.do_transform(
                request, MaltegoTransformResponseMessage(), self.config
            )
