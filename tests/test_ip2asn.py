import pytest
import responses

from canari.maltego.message import (
    MaltegoException,
    MaltegoTransformRequestMessage,
    MaltegoTransformResponseMessage,
)
from canari.maltego.entities import IPv4Address

from censys_maltego.transforms.common.entities import AS
from censys_maltego.transforms.ipaddresstoasn import IPAddressToASN

from .utils import TestCase

VIEW_HOST_JSON = {
    "result": {
        "autonomous_system": {
            "asn": 15169,
            "name": "GOOGLE",
            "country_code": "US",
        }
    }
}


class TestIPAddressToASN(TestCase):
    tranform = IPAddressToASN()

    def test_do_transform(self):
        self.responses.add(
            responses.GET,
            f"{self.v2_base_url}/hosts/{self.test_ip}",
            status=200,
            json=VIEW_HOST_JSON,
        )

        request = MaltegoTransformRequestMessage()
        request += IPv4Address(self.test_ip)
        response = MaltegoTransformResponseMessage()
        actual = self.tranform.do_transform(request, response, self.config)
        autonomous_system = VIEW_HOST_JSON["result"]["autonomous_system"]
        asn = AS(
            autonomous_system["asn"],
            name=autonomous_system["name"],
            countrycode=autonomous_system["country_code"],
        )
        expected = response + asn
        assert actual == expected

    def test_no_location_transform(self):
        no_asn_json = VIEW_HOST_JSON.copy()
        no_asn_json["result"]["autonomous_system"] = None
        self.responses.add(
            responses.GET,
            f"{self.v2_base_url}/hosts/{self.test_ip}",
            status=200,
            json=no_asn_json,
        )

        request = MaltegoTransformRequestMessage()
        request += IPv4Address(self.test_ip)
        with pytest.raises(
            MaltegoException, match=f"No Autonomous System found for {self.test_ip}"
        ):
            self.tranform.do_transform(
                request, MaltegoTransformResponseMessage(), self.config
            )
