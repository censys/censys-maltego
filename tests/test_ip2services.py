import pytest
import responses

from canari.maltego.message import (
    MaltegoException,
    MaltegoTransformRequestMessage,
    MaltegoTransformResponseMessage,
)
from canari.maltego.entities import IPv4Address, Service

from censys_maltego.transforms.ipaddresstoservices import IPAddressToServices

from .utils import TestCase

VIEW_HOST_JSON = {
    "result": {
        "services": [
            {"service_name": "HTTP", "port": 80},
            {"service_name": "HTTPS", "port": 443},
            {"service_name": "HTTP", "port": 8080, "banner": "TEST_BANNER"},
        ]
    }
}


class TestIPAddressToServices(TestCase):
    tranform = IPAddressToServices()

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
        expected = response + [
            Service(s.get("service_name"), port=s.get("port"), banner=s.get("banner"))
            for s in VIEW_HOST_JSON["result"]["services"]
        ]
        assert actual == expected

    def test_no_services_transform(self):
        no_ports_json = VIEW_HOST_JSON.copy()
        no_ports_json["result"]["services"] = []
        self.responses.add(
            responses.GET,
            f"{self.v2_base_url}/hosts/{self.test_ip}",
            status=200,
            json=no_ports_json,
        )

        request = MaltegoTransformRequestMessage()
        request += IPv4Address(self.test_ip)
        with pytest.raises(
            MaltegoException, match=f"No Services found for {self.test_ip}"
        ):
            self.tranform.do_transform(
                request, MaltegoTransformResponseMessage(), self.config
            )
