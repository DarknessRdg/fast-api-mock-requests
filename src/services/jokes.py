import requests
from fastapi.params import Depends

from src.config.settings import get_settings, Settings


class JokeClient:
    """
    Client to actually send request to `joke` API, handle any errors
    and convert/validate data returned.

    This abstract that `joke` API as python class using methods to
    request any resource.
    """
    def __init__(self, settings: Settings = Depends(get_settings)):
        self.base_url = settings.JOKES_BASE_URL

    def search(self) -> str:
        endpoint = f'{self.base_url}/joke/Any'
        response = requests.get(endpoint)
        response.raise_for_status()

        content = response.json()
        first_part = content['setup']
        second_part = content['delivery']
        return f'{first_part} ... {second_part}'


class JokeService:
    """
    A business services that defines an interface for all `joke`
    methods/behavior/functionality available for our internal application
    service.

    This also abstracts the logics necessary to handle with any kind
    of external client. All our internal application must request any kind of
    joke through this service.
    """
    def __init__(self, client: JokeClient = Depends()):
        self._client = client

    def random(self) -> str:
        return self._client.search()
