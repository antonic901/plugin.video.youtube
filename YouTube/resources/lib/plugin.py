from xbmcswift2 import Plugin, listitem, actions
from invidious import InvidiousApi

import os, json

plugin = Plugin()
invidious = InvidiousApi(plugin)

history = plugin.get_storage('history.json', file_format='json')
favorites = plugin.get_storage('favorites.json', file_format='json')

# Tools

def get_icon(icon='logo.png'):
    return "{}\\resources\\icons\\{}".format(os.getcwd(), icon)

def get_stream(id, quality):
    streams = invidious.fetch('/api/v1/videos/{}'.format(id))['formatStreams']
    for stream in streams:
        if stream['resolution'] == quality:
            return stream['url']
    # if preferred quality not found, use 360p by default
    for stream in streams:
        if stream['resolution'] == '360p':
            return stream['url']
    return 'not_found'

def add_videos(videos):
    items = []
    if videos:
        for video in videos:
            if plugin.get_setting('video-quality-select', bool):
                path = plugin.url_for('streams', id=video['videoId'])
            else:
                path = plugin.url_for('play', url=video['videoId'], details=json.dumps({'label': video['title'], 'icon': video['videoThumbnails'][3]['url']}))
            items.append({
                'label': video['title'],
                'thumbnail': video['videoThumbnails'][3]['url'],
                'path': path,
                'context_menu': [
                    (
                        plugin.get_string(830).format(video['author']),
                        actions.update_view(plugin.url_for('channels_menu', id=video['authorId']))
                    ),
                    (
                        plugin.get_string(831),
                        actions.update_view(plugin.url_for('list_videos_recommended', id=video['videoId']))
                    )
                ],
                # 'replace_context_menu': True,
                'is_playable': not plugin.get_setting('video-quality-select', bool),
            })
    return items

def add_playlists(playlists):
    items = []
    for playlist in playlists:
        items.append({
            'label': playlist['title'],
            'thumbnail': playlist['playlistThumbnail'],
            'path': plugin.url_for('playlists_videos_id', id=playlist['playlistId'], page=1),
            'context_menu': [
                (
                    plugin.get_string(830).format(playlist['author']),
                    actions.update_view(plugin.url_for('channels_menu', id=playlist['authorId']))
                ),
            ],
            'replace_context_menu': True
        })
    return items

def add_channels(channels):
    items = []
    if channels:
        for channel in channels:
            if channel['authorId'] in favorites:
                context_menu = (
                    plugin.get_string(832),
                    actions.background(plugin.url_for('subscriptions_del', id=channel['authorId']))
                )
            else:
                context_menu = (
                    plugin.get_string(833),
                    actions.background(plugin.url_for('subscriptions_add', channel=json.dumps(channel)))
                )             
            items.append({
                'label': channel['author'],
                'thumbnail': "https:{}".format(channel['authorThumbnails'][3]['url']),
                'path': plugin.url_for('channels_menu', id=channel['authorId']),
                'context_menu': [context_menu],            
                'replace_context_menu': True
            })
    return items

# Tools

# Videos

@plugin.route('/videos/recommended/<id>')
def list_videos_recommended(id):
    items = add_videos(invidious.fetch('/api/v1/videos/{}'.format(id), region='include', fields='recommendedVideos')['recommendedVideos'])
    return plugin.finish(items)

# Videos

# Playlist

@plugin.route('/playlists/videos/<id>/<page>')
def playlists_videos_id(id, page):
    page = int(page)
    items = add_videos(invidious.fetch('/api/v1/playlists/{}'.format(id), fields='videos', page=page)['videos'])
    if items:
        items.append({
            'label': plugin.get_string(732).format(page + 1),
            'path': plugin.url_for('playlists_videos_id', id=id, page=page + 1),
            'icon': get_icon()
        })
    return plugin.finish(items)

# Playlist

# Root menu

@plugin.route('/')
def show_root_menu():
    if not invidious.fetch('/api/v1/stats'):
        return plugin.finish([])
    print(plugin.url_for('trending'))
    items = [
        {
            'label': plugin.get_string(30301),
            'icon': get_icon('trend.png'),
            'path': plugin.url_for('trending')
        },
        {
            'label': plugin.get_string(30302),
            'icon': get_icon('popular.png'),
            'path': plugin.url_for('popular')
        },
        {
            'label': plugin.get_string(30303),
            'icon': get_icon('search.png'),
            'path': plugin.url_for('search_menu')
        },
        {
            'label': plugin.get_string(30304),
            'icon': get_icon('sub.png'),
            'path': plugin.url_for('subscriptions')
        },
        {
            'label': plugin.get_string(30305),
            'icon': get_icon('settings.png'),
            'path': plugin.url_for('settings')
        },
    ]
    return plugin.finish(items)

# Root menu

# Trending

@plugin.route('/trending/menu')
def trending():
    items = [
        {
            'label': plugin.get_string(430),
            'icon': get_icon('all.png'),
            'path': plugin.url_for('trending_videos', type='Default')
        },
        {
            'label': plugin.get_string(431),
            'icon': get_icon('music.png'),
            'path': plugin.url_for('trending_videos', type='Music')
        },
        {
            'label': plugin.get_string(432),
            'icon': get_icon('game.png'),
            'path': plugin.url_for('trending_videos', type='Gaming')
        },
        {
            'label': plugin.get_string(433),
            'icon': get_icon('news.png'),
            'path': plugin.url_for('trending_videos', type='News')
        },
        {
            'label': plugin.get_string(434),
            'icon': get_icon('movies.png'),
            'path': plugin.url_for('trending_videos', type='Movies')
        }
    ]
    return plugin.finish(items)

@plugin.route('/trending/videos/<type>')
def trending_videos(type):     
    items = add_videos(invidious.fetch('/api/v1/trending', type=type, region='include'))
    return plugin.finish(items)

# Trending

# Popular

@plugin.route('/popular')
def popular():
    items = add_videos(invidious.fetch('/api/v1/popular'))
    return plugin.finish(items)

# Popular

# Channel

@plugin.route('/channels/<id>')
def channels_menu(id):
    items = [
        {
            'label': plugin.get_string(530),
            'icon': get_icon(),
            'path': plugin.url_for('channels_videos', id=id, page=1)
        },
        {
            'label': plugin.get_string(531),
            'icon': get_icon(),
            'path': plugin.url_for('channels_latest', id=id)
        },
        {
            'label': plugin.get_string(532),
            'icon': get_icon('playlist.png'),
            'path': plugin.url_for('channels_playlists', id=id)
        },
        {
            'label': plugin.get_string(533),
            'icon': get_icon('search.png'),
            'path': plugin.url_for('channels_search', id=id, query='-', page=0)
        },
        {
            'label': plugin.get_string(534),
            'icon': get_icon(),
            'path': plugin.url_for('channels_related_channels', id=id)
        }
    ]
    return items

@plugin.route('/channels/videos/<id>/<page>')
def channels_videos(id, page):
    page = int(page)
    items = add_videos(invidious.fetch('/api/v1/channels/videos/{}'.format(id), page=page).get('videos', None))
    if items:
        items.append({
            'label': plugin.get_string(732).format(page + 1),
            'path': plugin.url_for('channels_videos', id=id, page=page + 1),
            'icon': get_icon()
        })
    return plugin.finish(items)

@plugin.route('/channels/latest/<id>')
def channels_latest(id):
    items = add_videos(invidious.fetch('/api/v1/channels/latest/{}'.format(id)))
    return plugin.finish(items)

@plugin.route('/channels/playlists/<id>')
def channels_playlists(id):
    items = add_playlists(invidious.fetch('/api/v1/channels/playlists/{}'.format(id))['playlists'])
    return plugin.finish(items)

@plugin.route('/channels/search/<id>/<query>/<page>')
def channels_search(id, query, page):
    page = int(page)
    if page == 0:
        query = plugin.keyboard(heading=plugin.get_string(630))
        if query:
            url = plugin.url_for('channels_search', id=id, query=query, page=1)
            plugin.redirect(url)
    else:
        items = add_videos(invidious.fetch('/api/v1/channels/search/{}'.format(id), q=query, page=page))
        if items:
            items.append({
                'label': plugin.get_string(732).format(page + 1),
                'path': plugin.url_for('channels_search', id=id, query=query, page=page + 1),
                'icon': get_icon()
            })
        return items

@plugin.route('/channels/related-channels/<id>')
def channels_related_channels(id):
    items = add_channels(invidious.fetch('/api/v1/channels/{}'.format(id), fields='relatedChannels')['relatedChannels'])
    return plugin.finish(items)

# Channel

# Search

@plugin.route('/search/menu')
def search_menu():
    items = [
        {
            'label': plugin.get_string(632),
            'icon': get_icon(),
            'path': plugin.url_for('search', type='video')
        },
        {
            'label': plugin.get_string(633),
            'icon': get_icon('movies.png'),
            'path': plugin.url_for('search', type='movie')
        },
        {
            'label': plugin.get_string(634),
            'icon': get_icon('playlist.png'),
            'path': plugin.url_for('search', type='playlist')
        },
        {
            'label': plugin.get_string(635),
            'icon': get_icon(),
            'path': plugin.url_for('search', type='channel')
        },
        {
            'label': plugin.get_string(636),
            'icon': get_icon(),
            'path': plugin.url_for('search_history_clear')
        }
    ]
    for value in history.values():
        items.append({
            'label': plugin.get_string(631).format(value['query'], value['type']),
            'icon': get_icon(),
            'path': plugin.url_for('search_result', query=value['query'], type=value['type'], page=1),
            'context_menu': [
                (
                    plugin.get_string(834),
                    'RunPlugin({})'.format(plugin.url_for('search_history_delete', query=value['query']))
                )
            ],
        })
    return plugin.finish(items)

@plugin.route('/search/<type>')
def search(type):
    query = plugin.keyboard(heading=plugin.get_string(630))
    if query:
        search_history_add(query, type)
        url = plugin.url_for('search_result', query=query, type=type, page=1)
        plugin.redirect(url)

@plugin.route('/search/<query>/<type>/<page>')
def search_result(query, type, page):
    page = int(page)
    if type == 'playlist':
        items = add_playlists(invidious.fetch('/api/v1/search', q=query, type=type, page=page, region='include'))
    elif type == 'channel':
        items = add_channels(invidious.fetch('/api/v1/search', q=query, type=type, page=page, region='include'))
    else:
        items = add_videos(invidious.fetch('/api/v1/search', q=query, type=type, page=page, region='include'))
    if items:
        items.append({
            'label': plugin.get_string(732).format(page + 1),
            'path': plugin.url_for('search_result', query=query, type=type, page=page + 1),
            'icon': get_icon()
        })
    return items

@plugin.route('/search/history/add/<query>/<type>')
def search_history_add(query, type):
    history.update({
        query: {
        'query': query,
        'type': type
    }})
    history.sync()

@plugin.route('/search/history/del/<query>')
def search_history_delete(query):
    del history[query]
    history.sync()
    plugin.notify(plugin.get_string(734).format(query))

@plugin.route('/search/history/clear')
def search_history_clear():
    history.clear()
    history.sync()
    plugin.notify(plugin.get_string(735))

# Search

# Subscriptions

@plugin.route('/subscriptions')
def subscriptions():
    items = [{
        'label': plugin.get_string(650),
        'icon': get_icon(),
        'path': plugin.url_for('subscriptions_clear')
    }]
    for channel in favorites.values():
        items.append({
            'label': channel['author'],
            'thumbnail': channel['thumb'],
            'path': plugin.url_for('channels_menu', id=channel['authorId']),
            'context_menu': [(
                plugin.get_string(832),
                'RunPlugin({})'.format(plugin.url_for('subscriptions_del', id=channel['authorId']))
            )],
            'replace_context_menu': True
        })
    return items

@plugin.route('/subscriptions/import')
def subscriptions_import():
    channels = readCsvFile()
    if channels:
        for channel in channels:
            subscriptions_add(json.dumps({
                'author': channel[2],
                'authorId': channel[0]
            }))
        plugin.notify(plugin.get_string(736))
    else:
        plugin.notify(plugin.get_string(737))

def readCsvFile(file_name='subscriptions.csv', location='E:\\'):
    filePath = os.path.join(location, file_name)
    print(filePath)
    if not os.path.isfile(filePath):
        return []
    with open(filePath) as csv_file:
        import csv
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        channels = []
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                if row != []:
                    channels.append(row)
            line_count = line_count + 1
        return channels

@plugin.route('/subscriptions/add/<channel>')
def subscriptions_add(channel):
    channel = json.loads(channel)
    try:
        favorites.update({
            channel['authorId']: {
            'authorId': channel['authorId'],
            'author': channel['author'],
            'thumb': "https:{}".format(channel['authorThumbnails'][3]['url'])
        }})
    except KeyError:
        favorites.update({
            channel['authorId']: {
            'authorId': channel['authorId'],
            'author': channel['author'],
            'thumb': get_icon()
        }})
    favorites.sync()
    plugin.notify(plugin.get_string(738).format(channel['author']))

@plugin.route('/subscriptions/del/<id>')
def subscriptions_del(id):
    del favorites[id]
    favorites.sync()
    plugin.notify(plugin.get_string(739))

@plugin.route('/subscriptions/clear')
def subscriptions_clear():
    favorites.clear()
    favorites.sync()
    plugin.notify(plugin.get_string(740))

# Subscriptions

# Settings

@plugin.route('/settings')
def settings():
    plugin.open_settings()

# Settings

# Streams

@plugin.route('/streams/<id>')
def streams(id):
    items = []
    video = invidious.fetch('/api/v1/videos/{}'.format(id), fields='formatStreams,title,videoThumbnails')
    if video:
        for stream in video['formatStreams']:
            items.append({
                'label': '{} ({};{} / {})'.format(stream['resolution'], stream['container'], stream['encoding'], stream['type']),
                'icon': video['videoThumbnails'][3]['url'],
                'path': plugin.url_for('play', url=stream['url'], details=json.dumps({'label': video['title'], 'icon': video['videoThumbnails'][3]['url']})),
                'is_playable': True,
            })
    return plugin.finish(items)

@plugin.route('/play/<url>/<details>')
def play(url, details):
    if not plugin.get_setting('video-quality-select', bool):
        url = get_stream(url, plugin.get_setting('video-quality', unicode))
        if url == 'not_found':
            plugin.notify(plugin.get_string(741))
            return
    details = json.loads(details)
    if plugin.get_setting('use-dash', bool):
        print('Using dash to stream content...')
        url = "{}{}".format(invidious.get_api(), url[41:])
    print('Starting stream from: {}'.format(url))
    return plugin.set_resolved_url(listitem.ListItem(label=details['label'], icon=details['icon'], thumbnail=details['icon'],path=url))

# Streams

# Entrypoint
def run():
    plugin.run()