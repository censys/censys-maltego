import argparse
import json
import logging
import os

from censys_maltego import Censys
from maltego_trx.transform import DiscoverableTransform

log_file_path = os.path.dirname(os.path.realpath(__file__))
log_file_name = 'censys_maltego_transform.log'

logging.basicConfig(filename=os.path.join(log_file_path, log_file_name), level=logging.INFO)


def get_credentials():

    try:
        credentials_path = os.path.dirname(os.path.realpath(__file__))
        credentials_file = '.env'
        cred_dict = None

        with open(os.path.join(credentials_path, credentials_file), 'r') as creds_file:
            cred_dict = json.loads(creds_file.read())

        return cred_dict

    except Exception as e:
        logging.critical("Please enter your credentials in the .env file in the transforms directory.")
        raise e


class search_ipv4_to_domains(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request, response):

        env_config = get_credentials()
        api_id, api_secret = env_config.get('censys_api_id'), env_config.get('censys_api_secret')

        ev = request.Value
        ep = request.Properties

        response = Censys(api_id, api_secret, max_pages=env_config.get('max_pages', 1)).search_ipv4_to_domains(
            ip_address=ev,
            object_properties=ep
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--censys_api_id",
                        required=False,
                        metavar='XXXXXXXXXX',
                        help="(optional) You must provide your Censys API ID here or as an environmental variable CENSYS_API_ID")
    parser.add_argument("--censys_api_secret",
                        required=False,
                        metavar='XXXXXXXXXX',
                        help="(optional) You must provide your Censys API SECRET here or as an environmental variable CENSYS_API_SECRET")

    parser.add_argument('entity_value')
    parser.add_argument('entity_properties')

    args = parser.parse_args()

    censys_api_id = os.getenv('CENSYS_API_ID', args.censys_api_id)
    censys_api_secret = os.getenv('CENSYS_API_SECRET', args.censys_api_secret)
    ev = args.entity_value
    ep = args.entity_properties

    Censys(censys_api_id, censys_api_secret).search_ipv4_to_domains(
        ip_address=ev, object_properties=ep
    )
