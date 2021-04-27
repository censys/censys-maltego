import pytest
import responses

from canari.maltego.message import (
    MaltegoException,
    MaltegoTransformRequestMessage,
    MaltegoTransformResponseMessage,
)
from canari.maltego.entities import Domain, IPv4Address

from censys_maltego.transforms.common.utils import is_ipv4
from censys_maltego.transforms.ipaddresstodomains import IPAddressToDomains

from .utils import TestCase

SEARCH_IPV4_JSON = {
    "results": [{"443.https.tls.certificate.parsed.names": ["google.com", "8.8.8.8"]}],
    "metadata": {"pages": 1},
}


class TestIPAddressToDomains(TestCase):
    tranform = IPAddressToDomains()

    def test_do_transform(self):
        self.responses.add(
            responses.POST,
            f"{self.v1_base_url}/search/ipv4",
            status=200,
            json=SEARCH_IPV4_JSON,
        )

        request = MaltegoTransformRequestMessage()
        request += IPv4Address(self.test_ip)
        response = MaltegoTransformResponseMessage()
        actual = self.tranform.do_transform(request, response, self.config)

        for domain in SEARCH_IPV4_JSON["results"][0][
            "443.https.tls.certificate.parsed.names"
        ]:
            if is_ipv4(domain):
                response += IPv4Address(domain)
            else:
                response += Domain(domain)
        assert actual == response

    def test_no_results_transform(self):
        no_results_json = SEARCH_IPV4_JSON.copy()
        no_results_json["results"] = []
        self.responses.add(
            responses.POST,
            f"{self.v1_base_url}/search/ipv4",
            status=200,
            json=no_results_json,
        )

        request = MaltegoTransformRequestMessage()
        request += IPv4Address(self.test_ip)
        with pytest.raises(
            MaltegoException, match=f"No search results found for {self.test_ip}"
        ):
            self.tranform.do_transform(
                request, MaltegoTransformResponseMessage(), self.config
            )

    def test_no_domains_transform(self):
        no_domains_json = SEARCH_IPV4_JSON.copy()
        no_domains_json["results"][0]["443.https.tls.certificate.parsed.names"] = []
        self.responses.add(
            responses.POST,
            f"{self.v1_base_url}/search/ipv4",
            status=200,
            json=no_domains_json,
        )

        request = MaltegoTransformRequestMessage()
        request += IPv4Address(self.test_ip)
        with pytest.raises(
            MaltegoException, match=f"No Domains found for {self.test_ip}"
        ):
            self.tranform.do_transform(
                request, MaltegoTransformResponseMessage(), self.config
            )
