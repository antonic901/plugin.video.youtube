import sys
import urlparse
import xbmc

import resources.lib.router as router


class Dictionary(dict):
    def as_bool(self, key, default=None):
        value = self.get(key, None)
        if value is not None:
            return value.lower() == "true"

        if default is not None:
            return default

        raise ValueError("invalid key: '{}'".format(key))

    def as_int(self, key, default=None):
        value = self.get(key, None)
        if value is not None:
            return int(value)

        if default is not None:
            return default

        raise ValueError("invalid key: '{}'".format(key))

    def as_float(self, key, default=None):
        value = self.get(key, None)
        if value is not None:
            return float(value)

        if default is not None:
            return default

        raise ValueError("invalid key: '{}'".format(key))

    def as_string(self, key, default=None):
        value = self.get(key, None)
        if value is not None:
            return value

        if default is not None:
            return default

        raise ValueError("invalid key: '{}'".format(key))


def run():
    # parse URL params
    url_params = Dictionary(urlparse.parse_qsl(sys.argv[2][1:]))

    route = "index"
    if url_params:
        route = url_params.pop("route", None)

    if route == "index":
        router.list_index()
    elif route == "trending":
        router.list_trending(url_params)
    elif route == "popular":
        router.list_popular()
    elif route == "search":
        router.list_search()
    elif route == "search_result":
        router.list_search_result(url_params)
    elif route == "playlist":
        router.list_playlist(url_params)
    elif route == "playlists":
        router.list_playlists(url_params)
    elif route == "channel":
        router.list_channel(url_params)
    elif route == "channel_result":
        router.list_channel_result(url_params)
    elif route == "channels":
        router.list_channels(url_params)
    elif route == "play":
        router.play(url_params)
    else:
        xbmc.log("wrong route: '{}'".format(route), xbmc.LOGNOTICE)
