import pytest
import responses

from canari.maltego.message import (
    MaltegoException,
    MaltegoTransformRequestMessage,
    MaltegoTransformResponseMessage,
)
from canari.maltego.entities import IPv4Address

from censys_maltego.transforms.common.entities import Location
from censys_maltego.transforms.ipaddresstolocation import IPAddressToLocation

from .utils import TestCase

VIEW_HOST_JSON = {
    "result": {
        "location": {
            "country": "United States",
            "country_code": "US",
            "city": "Chicago",
            "province": "Illinois",
            "timezone": "America/Chicago",
            "postal_code": 12345,
            "coordinates": {
                "latitude": 37.751,
                "longitude": -97.822,
            },
        }
    }
}


class TestIPAddressToLocation(TestCase):
    tranform = IPAddressToLocation()

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
        location = VIEW_HOST_JSON["result"]["location"]
        coordinates = location.get("coordinates", {})

        location_entity = Location(
            country=location.get("country"),
            countrycode=location.get("country_code"),
            latitude=coordinates.get("latitude"),
            longitude=coordinates.get("longitude"),
            city=location.get("city"),
            area=location.get("province"),
            timezone=location.get("timezone"),
            zipcode=location.get("postal_code"),
        )
        expected = response + location_entity
        assert actual == expected

    def test_no_location_transform(self):
        no_location_json = VIEW_HOST_JSON.copy()
        no_location_json["result"]["location"] = None
        self.responses.add(
            responses.GET,
            f"{self.v2_base_url}/hosts/{self.test_ip}",
            status=200,
            json=no_location_json,
        )

        request = MaltegoTransformRequestMessage()
        request += IPv4Address(self.test_ip)
        with pytest.raises(
            MaltegoException, match=f"No Location found for {self.test_ip}"
        ):
            self.tranform.do_transform(
                request, MaltegoTransformResponseMessage(), self.config
            )
