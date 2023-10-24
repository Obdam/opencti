import os
import yaml
from requests.auth import AuthBase

from pycti import __version__
from pycti.connector.opencti_connector_helper import get_config_variable

import google.auth.transport.requests
import google.oauth2.id_token

class GCPServerlessAuth(AuthBase):

    def __init__(self):
        # Get configuration
        config_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config.yml"
        )
        if os.path.isfile(config_file_path):
            with open(config_file_path, "r") as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
        else:
            config = {}

        # Load API config
        self.config = config
        self.opencti_url = get_config_variable(
            "OPENCTI_URL", ["opencti", "url"], config
        )
        self.opencti_token = get_config_variable(
            "OPENCTI_TOKEN", ["opencti", "token"], config
        )

        self.gcp_serverless_token = self.retrieve_gcp_serverless_token(self)
        

    def __call__(self, r):
        """Attach an API token to a custom auth header."""

        r.headers = {
            "User-Agent": "pycti/" + __version__,
            "Authorization": "Bearer " + self.opencti_token,
            "X-Serverless-Authorization": "Bearer " + self.gcp_serverless_token,
        }

        return r
    
    def retrieve_gcp_serverless_token(self):
        auth_req = google.auth.transport.requests.Request()
        return google.oauth2.id_token.fetch_id_token(auth_req, self.opencti_url)