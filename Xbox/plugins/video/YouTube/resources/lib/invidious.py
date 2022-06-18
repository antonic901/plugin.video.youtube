import requests
import os.path
import gui

## TODO Read this from configuration file or plugin settings
API = "http://192.168.0.18:9007"
REGION = "US"
RESOLUTION = "360p"
CONTAINER = "mp4"

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
    video = getInfoAboutVideo(id)
    if video:
        for stream in video['formatStreams']:
            if stream['resolution'] == RESOLUTION and stream['container'] == CONTAINER:
                return stream['url']
        gui.notify("Can not find streams for {} resolution.".format(RESOLUTION))
        return None
    gui.notify("Video with ID: {} can not be found.".format(id))
    return None
