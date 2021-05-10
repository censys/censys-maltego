"""Common Utilities for our tranforms."""
import os
import re

from canari.maltego.message import MaltegoException

RE_IP_PATTERN = re.compile(
    r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
)


def check_api_creds(request, response, config):
    """Check if API credentials are default.

    If they are not changed from the config. It is set to None.
    This is to be used with canari.framework.RequestFilter.

    Args:
        request: A MaltegoTransformRequest object.
        response: A MaltegoTransformResponse object.
        config: A CanariConfig object.
    """
    try:
        api_id = config["censys.local.api_id"]
        api_secret = config["censys.local.api_secret"]

        if (
            not api_id
            or api_id == "YOUR_API_ID"
            or not api_secret
            or api_secret == "YOUR_API_SECRET"
        ):
            raise KeyError
    except KeyError as error:
        config_path = os.path.join(
            os.path.expanduser("~"), ".canari", "censys_maltego.conf"
        )
        raise MaltegoException(
            f"Please configure your Censys API credentials at: {config_path}"
        ) from error


def is_ipv4(string: str) -> bool:
    """Check if the string is a valid IPv4 IP Address.

    Args:
        string (str): String to check.

    Returns:
        bool: If string is an IP.
    """
    return bool(re.search(RE_IP_PATTERN, string))


def list_to_string(lst: list = []) -> str:
    """Join list with commas.

    Args:
        lst (list): List to join.

    Returns:
        str: Joined list.
    """
    return ", ".join(lst)
