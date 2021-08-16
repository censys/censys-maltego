import unittest

import responses


class TestCase(unittest.TestCase):
    api_id = "test-api-id"
    api_secret = "test-api-secret"
    v1_base_url = "https://censys.io/api/v1"
    v2_base_url = "https://search.censys.io/api/v2"
    v1_api_on_v2_base_url = "https://search.censys.io/api/v1"
    config = {
        "censys.local.api_id": api_id,
        "censys.local.api_secret": api_secret,
        "censys.local.max_records": 5,
    }
    test_ip = "8.8.8.8"
    test_domain = "google.com"

    def setUp(self):
        self.responses = responses.RequestsMock()
        self.responses.start()

        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)
