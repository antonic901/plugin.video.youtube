import os
import sys
import urllib
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

ADDON_HANDLE = int(sys.argv[1])
ADDON_VFS_PATH = sys.argv[0]

addon = xbmcaddon.Addon()


def add_item(
    title,
    icon=None,
    thumb=None,
    url=None,
    url_params=None,
    video_infotag=None,
    video_duration=None,
    is_folder=True,
    total_items=0,
):
    item = xbmcgui.ListItem(title)

    art = {}
    if icon:
        art["icon"] = os.path.join(
            addon.getAddonInfo("path"), "resources", "media", icon
        )
    if thumb:
        art["thumb"] = thumb
    item.setArt(art)

    if not url:
        url = "{}?{}".format(ADDON_VFS_PATH, urllib.urlencode(url_params))

    if video_infotag is not None:
        is_folder = False
        item.setInfo("video", video_infotag)
        item.setProperty("IsPlayable", "True")

    if video_duration:
        item.addStreamInfo("video", {"duration": video_duration})

    return xbmcplugin.addDirectoryItem(ADDON_HANDLE, url, item, is_folder, total_items)


def end_listing():
    return xbmcplugin.endOfDirectory(ADDON_HANDLE)


def play(url):
    xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, xbmcgui.ListItem(path=url))


def get_search_input(heading, default_text=""):
    keyboard = xbmc.Keyboard(default_text, heading)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    return None
