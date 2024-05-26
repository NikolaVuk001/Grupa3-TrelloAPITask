import requests
from Config.config import API_KEY, TOKEN
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import HTTPError, RetryError


class TrelloClient:

    def __init__(self):
        self.session = requests.session()
        # self.session.params = {"key": API_KEY, "token": TOKEN}
        self.session.params = {"key": API_KEY, "token": TOKEN}
        retries = Retry(total=6, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount(prefix="https://", adapter=adapter)
        self.session.headers = {"Accept": "application/json"}
        self.base_url = "https://api.trello.com/1/"

    def get(self, endpoint, params: dict = None):
        if params is not None:
            self.session.params.update(params)

        try:
            response = self.session.get(self.base_url + endpoint)
            response.raise_for_status()
            return response.json()

        except RetryError:
            print("Retry error occurred.")
            return None
        except HTTPError:
            print(f"Došlo je do greške sa Trello web serverom: {response.status_code}")
            return None
        finally:
            self.session.close()

    def post(self, endpoint, params: dict = None):
        if params is not None:
            self.session.params.update(params)
        try:
            response = self.session.post(self.base_url + endpoint)
            response.raise_for_status()
            return response.json()
            pass
        except RetryError:
            print("Retry error occurred.")
        except HTTPError:
            print(f"Došlo je do greške sa Trello web serverom: {response.status_code}")
        finally:
            self.session.close()
