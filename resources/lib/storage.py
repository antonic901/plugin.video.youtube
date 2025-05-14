import os
import json
import xbmc

from .gui import addon


def get_storage_path(storage_name):
    storage_path = "special://profile/addon_data/{}/{}.json".format(
        addon.getAddonInfo("id"), storage_name
    )
    return xbmc.translatePath(storage_path)


def load_storage(storage_name):
    storage_path = get_storage_path(storage_name)
    if not os.path.exists(storage_path):
        return {}

    try:
        with open(storage_path, "r") as f:
            storage = json.load(f)
        return storage
    except Exception:
        xbmc.log("could not load storage: '{}'".format(storage_path), xbmc.LOGNOTICE)
    return None


def sync_storage(storage_name, storage_data):
    if not storage_data:
        return

    storage_path = get_storage_path(storage_name)
    try:
        dir_path = os.path.dirname(storage_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(storage_path, "w") as f:
            json.dump(storage_data, f)
    except Exception:
        xbmc.log("could not sync storage: '{}'".format(storage_path), xbmc.LOGNOTICE)
