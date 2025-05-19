# -*- coding: utf-8 -*-
import xbmc
import gui

from datetime import datetime

from .invidious import InvidiousAPI
from .storage import load_storage, sync_storage

invidious = InvidiousAPI(gui.addon)


def add_channel(channel):
    channel_id = channel.get("authorId")
    channel_author = channel.get("author")
    channel_thumb = invidious.format_thumbnail(
        channel.get("authorThumbnails")[1]["url"]
    )

    gui.add_item(
        channel_author,
        "logo.png",
        channel_thumb,
        url_params={"route": "channel", "id": channel_id},
    )


def add_video(video):
    video_id = video.get("videoId")
    video_title = video["title"]
    video_thumb = invidious.format_thumbnail(video["videoThumbnails"][3]["url"])

    # parse video information
    video_infotag = {}
    video_infotag["title"] = video_title

    value = video.get("description")
    if value:
        video_infotag["plot"] = value
    value = video.get("published")
    if value:
        published = datetime.fromtimestamp(value)
        video_infotag["date"] = published.strftime("%Y-%m-%d")

    gui.add_item(
        video_title,
        "logo.png",
        video_thumb,
        url_params={"route": "play", "id": video_id},
        video_infotag=video_infotag,
        video_duration=video.get("lengthSeconds", 0),
    )


def add_playlist(playlist):
    playlist_id = playlist.get("playlistId")
    playlist_title = playlist.get("title")
    playlist_thumb = invidious.format_thumbnail(playlist.get("playlistThumbnail"))
    gui.add_item(
        playlist_title,
        "logo.png",
        playlist_thumb,
        url_params={"route": "playlist", "id": playlist_id},
    )


def add_items(items):
    for item in items:
        item_type = item.get("type")
        if item_type == "channel":
            add_channel(item)
        elif item_type == "video":
            add_video(item)
        elif item_type == "playlist":
            add_playlist(item)
        else:
            xbmc.log("unsupported type: '{}'".format(item_type), xbmc.LOGNOTICE)


def find_stream(streams, resolution):
    for stream in streams:
        if stream["resolution"] == resolution:
            return stream["url"]

    if resolution == "720p":
        return find_stream(streams, "480p")
    if resolution == "480p":
        return find_stream(streams, "360p")
    if resolution == "360p":
        return find_stream(streams, "240p")
    if resolution == "240p":
        return find_stream(streams, "144p")

    return None


def play(url_params):
    video_id = url_params.get("id")
    if not video_id:
        return None

    video_information = invidious.get_video_information(video_id)
    if not video_information:
        return None

    streams = video_information.get("formatStreams")
    if not streams:
        xbmc.log("video with ID '{}' is missing streams".format(video_id))
        return None

    resolution = gui.addon.getSetting("resolution")
    stream_link = find_stream(streams, resolution)
    if not stream_link:
        return None

    xbmc.log("Playing video from: {}".format(stream_link))
    gui.play(stream_link)


def list_index():
    gui.add_item("Trending", "trend.png", url_params={"route": "trending"})
    gui.add_item("Popular", "popular.png", url_params={"route": "popular"})
    gui.add_item("Search", "search.png", url_params={"route": "search", "q": "-"})
    gui.end_listing()


def list_trending(url_params):
    is_root = url_params.as_bool("is_root", True)
    if is_root:
        gui.add_item(
            "All",
            "all.png",
            url_params={"route": "trending", "is_root": False, "type": "default"},
        )
        gui.add_item(
            "Music",
            "music.png",
            url_params={"route": "trending", "is_root": False, "type": "music"},
        )
        gui.add_item(
            "Gaming",
            "game.png",
            url_params={"route": "trending", "is_root": False, "type": "gaming"},
        )
        gui.add_item(
            "Movies",
            "movies.png",
            url_params={"route": "trending", "is_root": False, "type": "movies"},
        )
        return gui.end_listing()

    videos = invidious.get_trending(url_params.as_string("type"))
    if not videos:
        return gui.end_listing()

    add_items(videos)
    return gui.end_listing()


def list_popular():
    videos = invidious.get_popular()
    if not videos:
        return gui.end_listing()

    add_items(videos)
    return gui.end_listing()


def list_search():
    gui.add_item("New Search", "search.png", url_params={"route": "search_result"})

    storage = load_storage("history")
    if storage:
        search_history = storage.get("search_history", [])
        for history in search_history[::-1]:
            gui.add_item(history, url_params={"route": "search_result", "q": history})

    gui.end_listing()


def list_search_result(url_params):
    q = url_params.get("q")
    if not q:
        q = gui.get_search_input("New Search")
        if not q:
            return gui.end_listing()

    storage = load_storage("history")
    if storage is not None:
        search_history = storage.get("search_history", [])
        if len(search_history) > 40:
            search_history = search_history[1:] + search_history[:1]
            search_history[40] = q
        else:
            search_history.append(q)
        storage["search_history"] = search_history
        sync_storage("history", storage)

    page = url_params.as_int("page", 1)
    if page == 1:
        gui.add_item("Channels", url_params={"route": "channels", "q": q})
        gui.add_item("Playlists", url_params={"route": "playlists", "q": q})

    videos = invidious.search(q, page, "video")
    if not videos:
        return gui.end_listing()

    add_items(videos)

    gui.add_item(
        "Next page ({})".format(page + 1),
        url_params={"route": "search_result", "q": q, "page": page + 1},
    )
    return gui.end_listing()


def list_playlist(url_params):
    playlistId = url_params.get("id")
    if not playlistId:
        return gui.end_listing()

    videos = invidious.get_playlist_videos(playlistId)
    if not videos:
        return gui.end_listing()

    add_items(videos)
    return gui.end_listing()


def list_playlists(url_params):
    q = url_params.get("q")
    channel_id = url_params.get("id")

    if not (q or channel_id):
        return gui.end_listing()

    page = url_params.as_int("page", 1)

    playlists = None
    if q:
        playlists = invidious.search(q, page, "playlist")
    elif channel_id:
        playlists = invidious.get_channel_playlists(channel_id)

    if not playlists:
        return gui.end_listing()

    add_items(playlists)

    if q:
        gui.add_item(
            "Next page ({})".format(page + 1),
            url_params={"route": "playlists", "q": q, "page": page + 1},
        )

    return gui.end_listing()


def list_channel(url_params):
    channel_id = url_params.get("id", None)
    if not channel_id:
        return gui.end_listing()

    gui.add_item(
        "Playlists",
        "playlist.png",
        url_params={"route": "playlists", "id": channel_id},
    )
    gui.add_item(
        "Search", "search.png", url_params={"route": "channel_result", "id": channel_id}
    )

    videos = invidious.get_channel_videos(channel_id)
    if not videos:
        return gui.end_listing()

    add_items(videos)
    return gui.end_listing()


def list_channel_result(url_params):
    channel_id = url_params.get("id")
    if not channel_id:
        return gui.end_listing()

    q = url_params.get("q")
    if not q:
        q = gui.get_search_input("Search channel")
        if not q:
            return gui.end_listing()

    page = url_params.as_int("page", 1)

    items = invidious.search_channel(channel_id, q, page)
    if not items:
        return gui.end_listing()

    add_items(items)

    gui.add_item(
        "Next page ({})".format(page + 1),
        url_params={
            "route": "channel_result",
            "id": channel_id,
            "q": q,
            "page": page + 1,
        },
    )
    return gui.end_listing()


def list_channels(url_params):
    q = url_params.get("q")
    if not q:
        return gui.end_listing()

    page = url_params.as_int("page", 1)

    channels = invidious.search(q, page, "channel")
    if not channels:
        return gui.end_listing()

    add_items(channels)

    gui.add_item(
        "Next page ({})".format(page + 1),
        url_params={"route": "channels", "q": q, "page": page + 1},
    )
    return gui.end_listing()
