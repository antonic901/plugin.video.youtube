import xbmc

import requests


class InvidiousAPI:
    def __init__(self, addon):
        self.url = addon.getSetting("instance")
        self.region = addon.getSetting("region")

    def _make_request(self, url, params=None, headers=None):
        if not headers:
            headers = {"accept": "application/json", "user-agent": "xbox-youtube"}

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                return None
            return response.json()
        except Exception as e:
            xbmc.log(
                "Invidious API returned error: {}".format(str(e)), level=xbmc.LOGERROR
            )
        return None

    def format_thumbnail(self, thumb):
        if "http" in thumb:
            return thumb
        return "{}{}".format(self.url, thumb)

    def search(self, q, page=1, type=None):
        params = {}
        params["q"] = q
        if page:
            params["page"] = str(page)
        if type:
            params["type"] = type

        return self._make_request(self.url + "/api/v1/search", params)

    def search_channel(self, channel_id, q, page=1):
        params = {"q": q}
        if page:
            params["page"] = str(page)

        return self._make_request(
            self.url + "/api/v1/channels/" + channel_id + "/search", params
        )

    def get_trending(self, type):
        params = {"region": self.region}
        if type:
            params["type"] = type

        return self._make_request(self.url + "/api/v1/trending", params)

    def get_popular(self):
        return self._make_request(self.url + "/api/v1/popular")

    def get_video_information(self, video_id):
        return self._make_request(self.url + "/api/v1/videos/" + video_id)

    def get_channel_videos(self, channel_id):
        channel = self._make_request(
            self.url + "/api/v1/channels/" + channel_id + "/latest"
        )
        if not channel:
            return None

        return channel.get("videos", None)

    def get_channel_playlists(self, channel_id):
        channel = self._make_request(
            self.url + "/api/v1/channels/" + channel_id + "/playlists"
        )
        if not channel:
            return None

        return channel.get("playlists", None)

    def get_playlist_videos(self, playlistId):
        playlist = self._make_request(self.url + "/api/v1/playlists/" + playlistId)
        if not playlist:
            return None

        return playlist.get("videos", None)
