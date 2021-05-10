import pytest
from parameterized import parameterized

from canari.maltego.message import MaltegoException

from censys_maltego.transforms.common.utils import (
    check_api_creds,
    is_ipv4,
    list_to_string,
)

from ..utils import TestCase


class TestUtils(TestCase):
    API_EXEC_MATCH = "Please configure your Censys API credentials at: "

    def test_check_api_creds(self):
        with pytest.raises(MaltegoException, match=self.API_EXEC_MATCH):
            check_api_creds(None, None, {})

    def test_check_api_creds_default(self):
        with pytest.raises(MaltegoException, match=self.API_EXEC_MATCH):
            check_api_creds(
                None,
                None,
                {
                    "censys.local.api_id": "YOUR_API_ID",
                    "censys.local.api_secret": "YOUR_API_SECRET",
                    "censys.local.max_records": 5,
                },
            )

    def test_check_valid_api_creds(self):
        check_api_creds(None, None, self.config)

    @parameterized.expand(
        [
            ("8.8.8.8", True),
            ("google.com", False),
            ("123.123.123.123", True),
        ]
    )
    def test_is_ipv4(self, string, expected):
        assert expected == is_ipv4(string)

    @parameterized.expand(
        [
            ([], ""),
            (["string1", "string2"], "string1, string2"),
        ]
    )
    def test_list_to_string(self, list, expected):
        assert expected == list_to_string(list)
