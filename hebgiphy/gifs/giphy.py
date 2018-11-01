from functools import partial
import os

from cached_property import cached_property
from giphy_client import DefaultApi


class Giphy:

    def __init__(self, api_key=os.environ.get('GIPHY_API_KEY'), default_giphy_args={}):
        """Class for working with Giphy API.

        Args:
            api_key (str): The Giphy API Key.
            default_giphy_args (dict): A kwargs `dict` that will be passed to the giphy methods by default.
        """
        self._api_key = api_key
        self._default_args = default_giphy_args

    @cached_property
    def _api(self):
        return DefaultApi()

    def update_default_args(self, kwargs):
        self._default_args.update(kwargs)

    def __getattr__(self, name):
        method = getattr(self._api, name)  # Raises AttributeError if the method doesn't exist on API Instance
        partial_method = partial(method, self._api_key, **self._default_args)
        partial_method.__doc__ = method.__doc__
        return partial_method

    def __dir__(self):
        return super().__dir__() + dir(self._api)


GIPHY_API = Giphy()
