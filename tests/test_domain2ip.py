import pytest
import responses

from canari.maltego.message import (
    MaltegoException,
    MaltegoTransformRequestMessage,
    MaltegoTransformResponseMessage,
)
from canari.maltego.entities import Domain, IPv4Address

from censys_maltego.transforms.common.entities import IPv6Address
from censys_maltego.transforms.domaintoipaddress import DomainToIPAddress

from .utils import TestCase

SEARCH_IPV4_JSON = {
    "results": [{"ip": f"1.1.1.{i}"} for i in range(4)]
    + [{"ip": "2001:4860:4860::8888"}],
    "metadata": {"pages": 1},
}


class TestDomainToIPAddress(TestCase):
    tranform = DomainToIPAddress()

    def test_do_transform(self):
        self.responses.add(
            responses.POST,
            f"{self.v1_base_url}/search/ipv4",
            status=200,
            json=SEARCH_IPV4_JSON,
        )

        request = MaltegoTransformRequestMessage()
        request += Domain(self.test_domain)
        response = MaltegoTransformResponseMessage()
        actual = self.tranform.do_transform(request, response, self.config)

        for ip in [res.get("ip") for res in SEARCH_IPV4_JSON["results"]]:
            if ":" in ip:
                response += IPv6Address(ip)
            else:
                response += IPv4Address(ip)
        assert actual == response

    def test_no_location_transform(self):
        no_asn_json = SEARCH_IPV4_JSON.copy()
        no_asn_json["results"] = []
        self.responses.add(
            responses.POST,
            f"{self.v1_base_url}/search/ipv4",
            status=200,
            json=no_asn_json,
        )

        request = MaltegoTransformRequestMessage()
        request += Domain(self.test_domain)
        with pytest.raises(
            MaltegoException, match=f"No IPs found for {self.test_domain}"
        ):
            self.tranform.do_transform(
                request, MaltegoTransformResponseMessage(), self.config
            )
