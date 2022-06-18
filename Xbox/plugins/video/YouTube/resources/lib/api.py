# -*- coding: utf-8 -*-
import requests
import gui
import os.path
import invidious

COLOR_CODE_MAIN = 'ffe52d27'
PLUGIN_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ICON = os.path.join(PLUGIN_PATH, 'icon.png')

LIMIT = 20

def play(**kwargs):
    stream_url = invidious.getVideoLink(kwargs.get('id', None))
    if stream_url:
        gui.play(stream_url)

def list_index():
    gui.add_item('Trending', url_params={'f': 'trending'}, is_folder=True)
    gui.add_item('Popular', url_params={'f': 'popular'}, is_folder=True)
    gui.add_item('Search', url_params={'f': 'search', 'q': '-'}, is_folder=True)
    gui.end_listing()

def list_trending(**kwargs):
    page_number = int(kwargs.pop('pageNumber', 1)) + 1

    if page_number == 2:
        ## TODO Fetch region from system or plugin settings
        gui.add_item('All', ICON, {'f': 'trending', 'pageNumber': page_number}, is_folder=True)
        gui.add_item('Music', ICON, {'f': 'trending', 'pageNumber': page_number, 'type': 'music'}, is_folder=True)
        gui.add_item('Gaming', ICON, {'f': 'trending', 'pageNumber': page_number, 'type': 'gaming'}, is_folder=True)
        gui.add_item('News', ICON, {'f': 'trending', 'pageNumber': page_number, 'type': 'news'}, is_folder=True)
        gui.add_item('Movies', ICON, {'f': 'trending', 'pageNumber': page_number, 'type': 'movies'}, is_folder=True)

    else:
        videos = invidious.getTrending(kwargs.pop('type', None))
        for video in videos[:LIMIT]:
            video_id = video['videoId']
            title = video['title']
            description = video['description']
            date = video['published']
            channel_id = video['authorId']
            channel_title = video['author']
            thumb = video['videoThumbnails'][3]['url']
            duration_in_seconds = video['lengthSeconds']
            gui.add_item(title, thumb, {'f': 'play', 'id': video_id},
                {'title': title, 'plot': description, 'year': date, 'director': channel_title},
                    duration_in_seconds, total_items=21)

    gui.end_listing()

def list_popular(**kwargs):
    videos = invidious.getPopular()
    for video in videos[:LIMIT]:
        video_id = video['videoId']
        title = video['title']
        date = video['published']
        channel_id = video['authorId']
        channel_title = video['author']
        thumb = video['videoThumbnails'][3]['url']
        duration_in_seconds = video['lengthSeconds']
        gui.add_item(title, thumb, {'f': 'play', 'id': video_id},
            {'title': title, 'year': date, 'director': channel_title},
                duration_in_seconds, total_items=LIMIT + 1)

    gui.end_listing()

def list_search(**kwargs):
    page_number = int(kwargs.pop('pageNumber', 1)) + 1

    if page_number == 2 and kwargs.get('q') == '-' and kwargs.get('type', None) == None:
        # gui.add_item('All', url_params={'f': 'search', 'q': '-', 'type': 'all'}, is_folder=True)
        gui.add_item('Videos', url_params={'f': 'searchVideos', 'q': '-', 'type': 'video'}, is_folder=True)
        gui.add_item('Playlists', url_params={'f': 'search', 'q': '-', 'type': 'playlist'}, is_folder=True)
        gui.add_item('Channels', url_params={'f': 'search', 'q': '-', 'type': 'channel'}, is_folder=True)

    elif page_number == 2 and kwargs.get('q') == '-' and kwargs.get('type', None) != None:
        q = gui.get_search_input('Search')
        kwargs['q'] = q

        if kwargs.get('type') == 'video':
            videos = invidious.search(q, page_number-1, kwargs.get('type'))
            for video in videos:
                # print "%s" % video['videoId']
                video_id = video['videoId']
                # print "%s" % video['title']
                title = video['title']
                # print "%s" % video['description']
                description = video['description']
                # print "%s" % video['published']
                date = video['published']
                # print "%s" % video['authorId']
                channel_id = video['authorId']
                # print "%s" % video['author']
                channel_title = video['author']
                thumb = video['videoThumbnails'][3]['url']
                # print "%s" % video['lengthSeconds']
                duration_in_seconds = video['lengthSeconds']
                gui.add_item(title, thumb, {'f': 'play', 'id': video_id},
                    {'title': title, 'plot': description, 'year': date, 'director': channel_title},
                        duration_in_seconds, total_items=20)


        else:
            gui.notify('Not implemented.')

    gui.end_listing()

def list_search_videos(**kwargs):
    page_number = int(kwargs.pop('pageNumber', 1)) + 1
    if page_number == 2 and kwargs.get('q') == '-':
        q = gui.get_search_input('Search')
        kwargs['q'] = q
    videos = invidious.search(kwargs.get('q'), page_number-1, kwargs.get('type'))
    if not videos:
        return
    for video in videos:
        video_id = video['videoId']
        title = video['title']
        description = video['description']
        date = video['published']
        channel_id = video['authorId']
        channel_title = video['author']
        thumb = video['videoThumbnails'][3]['url']
        duration_in_seconds = video['lengthSeconds']
        gui.add_item(title, thumb, {'f': 'play', 'id': video_id},
            {'title': title, 'plot': description, 'year': date, 'director': channel_title},
                duration_in_seconds, total_items=LIMIT + 1)

    kwargs['f'] = 'searchVideos'
    kwargs['pageNumber'] = page_number
    gui.add_item('[B][COLOR %s]Next page (%s)[/COLOR][/B]' % (COLOR_CODE_MAIN, page_number), ICON, kwargs,
                    is_folder=True, total_items=LIMIT + 1)

    gui.end_listing()