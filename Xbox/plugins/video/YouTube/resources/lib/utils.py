import os, sys
import json
import csv
import shutil

HOST_AND_PATH = os.getcwd()

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

def getHistory(path="{}\\history.json".format(HOST_AND_PATH)):
    if os.path.isfile(path):
        json_data = open(path).read()
        history = json.loads(json_data)
        return history['history']
    else:
        return []

def isAdded(array, q, type):
    for query in array:
        if query['q'].lower() == q.lower() and query['type'] == type:
            return True
    return False

def saveInHistory(q, type, path="{}\\history.json".format(HOST_AND_PATH)):
    updatedHistory = getHistory()
    if isAdded(updatedHistory, q, type):
        pass
    else:
        updatedHistory.append({'q': q, 'type': type})
    payload = createJson({'history': updatedHistory})
    f = open(path, 'w+')
    f.write(payload)
    f.close()

def clear_history(path="{}\\history.json".format(HOST_AND_PATH)):
    payload = createJson({'history': []})
    f = open(path, 'w+')
    f.write(payload)
    f.close()

def createJson(data):
    json_string = json.dumps(data)
    return json_string

def readCsvFile(file_name='subscriptions.csv', location='{}\\'.format(HOST_AND_PATH)):
    filePath = os.path.join(location, file_name)
    print(filePath)
    if os.path.isfile(filePath):
        print("File je pronadjen.")
    else:
        print("File nije pronadjen.")
        return []
    with open(filePath) as csv_file:
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

def writeCsvFile(row, file_name='subscriptions.csv', location='{}\\'.format(HOST_AND_PATH)):
    filePath = os.path.join(location, file_name)
    print(filePath)
    if os.path.isfile(filePath):
        print("File je pronadjen.")
    else:
        print("File nije pronadjen.")
        return False

    with open(filePath, mode='ab') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(row)
        return True

    return False

def copy(file_name='subscriptions.csv', fromPath='E:\\', toPath="{}\\".format(HOST_AND_PATH)):
    original = os.path.join(fromPath, file_name)
    target = os.path.join(toPath,file_name)

    if os.path.isfile(original):
        shutil.copyfile(original, target)
        return True
    else:
        return False

def importSubcriptions():
    return copy()

def isSubscribed(id):
    channels = readCsvFile()
    for channel in channels:
        if channel[0] == id:
            return True

    return False

def subscribe(row):
    print(row)
    if isSubscribed(row[0]):
        return False
    else:
        # return True
        return writeCsvFile(row)