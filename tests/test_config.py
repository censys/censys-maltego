import pytest

from canari.maltego.message import MaltegoException

from censys_maltego.transforms.common.utils import check_api_creds

from .utils import TestCase


class TestConfig(TestCase):
    def test_check_api_creds(self):
        with pytest.raises(
            MaltegoException, match="Please configure your Censys API credentials at: "
        ):
            check_api_creds(None, None, {})

    def test_check_api_creds_default(self):
        with pytest.raises(
            MaltegoException, match="Please configure your Censys API credentials at: "
        ):
            check_api_creds(
                None,
                None,
                {
                    "censys.local.api_id": "YOUR_API_ID",
                    "censys.local.api_secret": "YOUR_API_SECRET",
                    "censys.local.max_records": 5,
                },
            )
