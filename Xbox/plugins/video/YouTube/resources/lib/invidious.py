import requests
import gui
import xbmcplugin

API = "http://{}:{}".format(xbmcplugin.getSetting('gateway'), xbmcplugin.getSetting('port'))
REGION = xbmcplugin.getSetting("region")
RESOLUTION =xbmcplugin.getSetting("resolution")
CONTAINER = xbmcplugin.getSetting("container")

search_order = xbmcplugin.getSetting("soptions")
channel_sort = xbmcplugin.getSetting("coptions")

HEADERS = {'accept': 'application/json', 'user-agent': 'xbox-youtube'}

def getTrending(type):
    params = {'region': REGION}
    if type:
        params['type'] = type
    response = requests.get(API + "/api/v1/trending", headers=HEADERS, params=params)
    if response.status_code != 200:
        gui.notify('Invidious returned status code: %s' % response.status_code)
        return None
    videos = response.json()
    if not videos:
        gui.notify('Invidious return success, but videos are not found.')
        return None
    return videos

def getPopular():
    response = requests.get(API + "/api/v1/popular", headers=HEADERS)
    if response.status_code != 200:
        gui.notify('Invidious returned status code: %s' % response.status_code)
        return None
    videos = response.json()
    if not videos:
        gui.notify('Invidious return success, but videos are not found.')
        return None
    return videos

def search(q, page, type):
    params = {'region': REGION}
    params['q'] = q
    if page:
        params['page'] = str(page)
    if type:
        params['type'] = type
    response = requests.get("{}/api/v1/search".format(API), headers=HEADERS, params=params)
    if response.status_code != 200:
        gui.notify('Invidious returned status code: %s' % response.status_code)
        return None
    results = response.json()
    if not results:
        gui.notify('Invidious return success, but no results.')
        return None
    return results

def getInfoAboutVideo(id):
    params = {"region": REGION}
    response = requests.get("{}/api/v1/videos/{}".format(API, id), headers=HEADERS, params=params)
    if response.status_code != 200:
        gui.notify('Invidious returned status code: %s' % response.status_code)
        return None
    video = response.json()
    if not video:
        gui.notify('Invidious return success, but video can not be found.')
        return None
    return video

def getVideoLink(id):
    # video = getInfoAboutVideo(id)
    # if video:
    #     for stream in video['formatStreams']:
    #         if stream['resolution'] == RESOLUTION and stream['container'] == CONTAINER:
    #             return stream['url']
    #     gui.notify("Can not find streams for {} resolution.".format(RESOLUTION))
    #     return None
    # gui.notify("Video with ID: {} can not be found.".format(id))
    # return None
    if RESOLUTION == '720p':
        params = {'id': id, 'quality': '22'}
    else:
        params = {'id': id, 'quality': '18'}
    response = requests.get("{}/local-stream-link".format(API), headers=HEADERS, params=params)
    if response.status_code != 200:
        return None
    return response.text

def getInfoAboutPlaylist(id):
    params = {'fields': 'videos', 'pretty': '1'}
    response = requests.get("{}/api/v1/playlists/{}".format(API, id), headers=HEADERS, params=params)
    if response.status_code != 200:
        gui.notify('Invidious returned status code: %s' % response.status_code)
        return None
    playlist = response.json()
    if not playlist:
        gui.notify('Invidious return success, but video can not be found.')
        return None
    return playlist

def getVideosForChannel(id, page_number, sort_by=channel_sort):
    params = {'page': str(page_number), 'sort_by': sort_by}
    response = requests.get("{}/api/v1/channels/{}/videos".format(API, id), headers=HEADERS, params=params)
    if response.status_code != 200:
        gui.notify('Invidious returned status code: %s' % response.status_code)
        return None
    videos = response.json()
    if not videos:
        gui.notify('Invidious return success, but videos can not be found.')
        return None
    return videos

def getLatestForChannel(id):
    response = requests.get("{}/api/v1/channels/{}/latest".format(API, id), headers=HEADERS)
    if response.status_code != 200:
        gui.notify('Invidious returned status code: %s' % response.status_code)
        return None
    videos = response.json()
    if not videos:
        gui.notify('Invidious return success, but videos can not be found.')
        return None
    return videos

def getPlaylistsForChannel(id, sort_by=channel_sort):
    params = {'sort_by': sort_by}
    response = requests.get("{}/api/v1/channels/{}/playlists".format(API,id), headers=HEADERS, params=params)
    if response.status_code != 200:
        gui.notify('Invidious returned status code: %s' % response.status_code)
        return None
    playlists = response.json()
    if not playlists:
        gui.notify('Invidious return success, but playlists can not be found.')
        return None
    return playlists['playlists']

def searchChannel(id, q, page):
    params = {'q': q, 'page': str(page)}
    response = requests.get("{}/api/v1/channels/search/{}".format(API, id), headers=HEADERS, params=params)
    if response.status_code != 200:
        gui.notify('Invidious returned status code: %s' % response.status_code)
        return None
    results = response.json()
    if not results:
        gui.notify('Invidious return success, but no results.')
        return None
    return results

def getInfoAboutChannel(id, sort_by=channel_sort):
    params = {'sort_by': sort_by, 'fields': 'author,authorUrl,relatedChannels', 'pretty': '1'}
    response = requests.get("{}/api/v1/channels/{}".format(API, id), headers=HEADERS, params=params)
    if response.status_code != 200:
        gui.notify('Invidious returned status code: %s' % response.status_code)
        return None
    channel = response.json()
    if not channel:
        gui.notify('Invidious return success, but no results.')
        return None
    return channel