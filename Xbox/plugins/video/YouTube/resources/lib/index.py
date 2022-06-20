# -*- coding: utf-8 -*-
import sys
import api

d = dict(p.split('=') for p in sys.argv[2][1:].split('&') if len(p.split('=')) == 2)
print("Dictionary: %s" % d)
try:
    f = {
        "index": api.list_index,
        "trending": api.list_trending,
        "popular": api.list_popular,
        "channelMenu": api.list_channel_menu,
        "channelVideos": api.list_channel_videos,
        "channelLatest": api.list_channel_latest,
        "channelPlaylists": api.list_channel_playlists,
        "channelSearch": api.list_channel_search,
        "channelRelated": api.list_channel_related,
        "searchMenu": api.list_search_menu,
        "searchVideos": api.list_search_videos,
        "searchPlaylists": api.list_search_playlists,
        "searchChannels": api.list_search_channels,
        "subscriptions": api.list_subscriptions,
        "settings": api.open_settings,
        "play": api.play,
        "importSubscriptions": api.import_subscription,
        "subscribe": api.subscribe,
        "videosPlaylists": api.list_videos_playlists,
        "suggestedVideos": api.list_suggested_videos
    }[d.pop('f', 'index')]
    f(**d)
except:
    api.list_index()