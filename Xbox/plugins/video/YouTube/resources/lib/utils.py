import os, sys
import json

HOST_AND_PATH = os.getcwd()

def createObject(jsonObject):    
    class Generic:
        @classmethod
        def from_dict(cls, dict):
            obj = cls()
            obj.__dict__.update(dict)
            return obj

    return json.loads(jsonObject, object_hook=Generic.from_dict)

'''
    Accept dictionary in format {id: list_of_videos}
'''
def createTempForVideos(videos, path = "{}\\videosPayload.json".format(HOST_AND_PATH)):
    print(path)
    payload = createJson(videos)
    f = open(path, 'w+')
    f.write(payload)
    f.close()

def readTempForVideos(path="{}\\videosPayload.json".format(HOST_AND_PATH)):
    print(path)
    if os.path.isfile(path):
        json_data = open(path).read()
        # videos = createObject(json_data)
        videos = json.loads(json_data)
        return videos
    else:
        return []

def createJson(data):
    json_string = json.dumps(data)
    return json_string
