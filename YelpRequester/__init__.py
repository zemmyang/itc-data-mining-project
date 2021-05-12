import json
import os
import logging
import requests
import random as r
from unittest.mock import Mock

from YelpRequester import internal_config as ICFG
from YelpRequester import messages as M


class YelpRequester:
    """
    internal functions for the other YR-related classes. used to read the config file and get
    data from it like the API key. also handles the logger.

    not meant to be used directly by outside classes
    """
    def __init__(self) -> None:
        self._initialize_logger()
        self._read_config_file()

    def _initialize_logger(self) -> None:
        """ sets up the logger """
        self.logger = logging.getLogger('yelprequester_logger')

        log_format = logging.Formatter(ICFG.LOG_FORMAT)
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.getcwd()), ICFG.YELPREQUESTER_LOG_FILE))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        self.logger.addHandler(file_handler)

    def _read_config_file(self) -> None:
        """
        looks for the yelprequester.json file.
        it should be in the same directory as main.py
        """
        try:
            with open(ICFG.YELPREQUESTER_CONFIG_FILE) as f:
                self.config_file = json.load(f)
        except FileNotFoundError:
            self.logger.critical(M.YELPREQUESTER_CONFIG_FILE_CRITICAL)
            raise FileNotFoundError(M.YELPREQUESTER_CONFIG_FILE_CRITICAL)
        except Exception as err:
            self.logger.critical(M.YELPREQUESTER_GENERIC_ERROR_CRITICAL.format(message=err))
            raise Exception(M.YELPREQUESTER_GENERIC_ERROR_CRITICAL.format(message=err))
        else:
            self.logger.debug(M.YELPREQUESTER_APIKEY_FOUND_DEBUG.format(logfile=ICFG.YELPREQUESTER_CONFIG_FILE))

    def request(self, path, url_params):
        _api_key = self.get_api_key()

        _url = ICFG.STARTING_URL + path

        _headers = r.choice(ICFG.HEADERS)
        _headers['Authorization'] = f'Bearer {_api_key}'

        _response = requests.request('GET', _url, headers=_headers, params=url_params)
        return _response

    def get_api_key(self) -> str:
        return self.config_file['API_KEY']

    def get_limit(self) -> str:
        return self.config_file['limit']

    def get_locale(self) -> str:
        return self.config_file['locale']

    def get_country(self) -> str:
        return self.config_file['country']

    def get_sql_credentials(self) -> dict:
        return {key: self.config_file[key] for key in ['sql_db', 'sql_host', 'sql_user', 'sql_password']}

    @staticmethod
    def return_fake_request():
        _response = Mock(spec=requests.models.Response)
        _response.json.return_value = {}
        _response.status_code = 400

        return _response

    def check_response(self, response):
        """ find if the response status code is 200 """
        if response.status_code == 200:
            if "error" not in response.json().keys():  # find an error in the response
                return True
            else:
                self.logger.error(M.YELPREQUESTER_ERROR_IN_RESPONSE_WARNING)
        else:
            return False
