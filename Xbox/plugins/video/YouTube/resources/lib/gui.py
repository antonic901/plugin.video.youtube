import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin

HOST_AND_PATH = sys.argv[0]
ADDON_HANDLE = int(sys.argv[1])
API = xbmcplugin.getSetting('instance')

def make_info_view_possible():
    xbmcplugin.setContent(ADDON_HANDLE, 'movies')


def add_item(title,
             thumb='',
             url_params='',
             video_info_labels=None,
             duration_in_seconds=None,
             fanart='',
             video_url=None,
             icon='',
             is_playable='true',
             context_menu_items=None,
             subtitle_list=None,
             is_folder=False,
             total_items=0):

    if thumb != None and "http" not in thumb:
        thumb = "{}{}".format(API,thumb)
    item = xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=thumb)
    if video_info_labels is not None:
        item.setInfo(type='video', infoLabels=video_info_labels)
    item.setProperty('IsPlayable', is_playable)
    item.setProperty('fanart_image', fanart)
    if duration_in_seconds is not None:
        item.addStreamInfo('video', {'duration': duration_in_seconds})
    if context_menu_items is not None:
        item.addContextMenuItems(context_menu_items)
    if subtitle_list is not None:
        try:
            item.setSubtitles(subtitle_list)
        except AttributeError:
            pass
    url = video_url or '%s?%s' % (HOST_AND_PATH, urllib.urlencode(url_params))
    return xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=item, isFolder=is_folder,
                                       totalItems=total_items)


def end_listing():
    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def play(url):
    xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, xbmcgui.ListItem(path=url))


def player_play(title, thumb, stream_url):
    title = urllib.unquote_plus(title)
    thumb = urllib.unquote_plus(thumb)
    item = xbmcgui.ListItem(title, thumbnailImage=thumb)
    xbmc.Player().play(stream_url, item)


def get_search_input(heading, default_text=''):
    keyboard = xbmc.Keyboard(default_text, heading)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()


def info_view(view_id=504):
    xbmc.executebuiltin('Container.SetViewMode(%s)' % view_id)


def notify(text):
    xbmc.executebuiltin('Notification(Notification for user,%s,5000,DefaultIconInfo.png)' % text)