# -*- coding: utf-8 -*-
import sys
import api

d = dict(p.split('=') for p in sys.argv[2][1:].split('&') if len(p.split('=')) == 2)
# print("Dictionary: %s" % d)
try:
    print("Usao sam u try...")
    f = {
        "index": api.list_index,
        "trending": api.list_trending,
        "popular": api.list_popular,
        "search": api.list_search,
        "searchVideos": api.list_search_videos,
        "play": api.play
    }[d.pop('f', 'index')]
    f(**d)
except:
    # print("Usao sam u except...")
    api.list_index()