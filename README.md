# YouTube for Original Xbox
You can now again watch YouTube on Original Xbox!
![Fanart](https://github.com/antonic901/xbox-youtube/blob/master/images/fanart.png?raw=true)

## Table of Contents
- [Info](#info)
- [Requirements](#requirements)
- [How to install](#how-to-install)
- [Running](#running)
- [Functionalities](#functionalities)
- [Video](#video)
- [Some images](#some-images)

## Info
This is plugin for XBMC4Xbox that aims to resurrect streaming of videos from YouTube on this dated hardware. Plugin is coded in Python and it's using [Invidious](https://invidious.io) for fetching data.

## Requirements
 - You need softmodded or hardmodded Xbox
 - You need latest release of [XBMC4Xbox](https://www.xbmc4xbox.org.uk/) as your main Dashboard
 - You know how to transfer files between your PC and Xbox (a.k.a know how to use FTP to transfer files)

## How to install
 - Download latest release from [here](https://github.com/antonic901/xbox-youtube/releases)
 - Extract downloaded archive.
 - Before we begin installing plugin you first need to checkout does your XBMC4Xbox have all required modules. Go to **Q:\scripts\\.modules** and check does this folder contain these four modules:
    + **script.module.beautifulsoup**
    + **script.module.xbmcaddon**
    + **script.module.xbmcswift2** (this is probably the one that you don't have, but don't worry!)
    + **script.module.xbmcvfs**
 - If you have all of four modules installed jump to next step, but if not keep reading! When you extracted downloaded archive you could notice two folders of which one is **modules**. Inside this folder you will find all modules required by this plugin. Depending on which module you are missing, copy that module to **Q:\scripts\\.modules** (INFO: in most cases you won't have xmbcswift2 module. You can also install it using Addons4Xbox Installer)
 - Finally, install plugin by copying **YouTube** folder from archive to **Q:\plugins\video**

## Running
- Open plugin from XBMC4Xbox located in Videos -> Plugins

## Functionalities
Status values:
- ✓ - Functionality implemented
- ✗ - Functionality not yet implemented

| Functionality                                     | Status |
|---------------------------------------------------|:------:|
| Trending videos (All, Music, Gaming, News, Movies)|   ✓    |
| Popular Videos                                    |   ✓    |
| Suggested Videos                                  |   ✓    |
| Search videos, playlists, channels                |   ✓    |
| Search history                                    |   ✓    |
| Channel explore (Videos, Latest, Playlists, Related Channels)|   ✓    |
| Search channel by videos and playlists            |   ✓    |
| Subscribe/Unsubscribe to/from channel             |   ✓    |
| Import subscriptions from YouTube                 |   ✓    |
| Autoplay next video                               |   ✗    |
| HLS and DASH adaptive streams (Lives)             |   ✗    |

## Support
<a href="https://www.buymeacoffee.com/antonic901" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## Video
[![Watch the video](https://i.postimg.cc/7Y2g3QyT/Screenshot-from-2022-06-23-13-35-13.png)](https://youtu.be/At9XPKZNprM)
## Some images
![Searching](https://github.com/antonic901/xbox-youtube/blob/master/images/screenshot003.bmp?raw=true)
![Channel search](https://github.com/antonic901/xbox-youtube/blob/master/images/screenshot009.bmp?raw=true)
![Streaming video](https://github.com/antonic901/xbox-youtube/blob/master/images/screenshot006.bmp?raw=true)
![Popular](https://github.com/antonic901/xbox-youtube/blob/master/images/screenshot002.bmp?raw=true)
![Search History](https://github.com/antonic901/xbox-youtube/blob/master/images/screenshot004.bmp?raw=true)
![Subscriptions](https://github.com/antonic901/xbox-youtube/blob/master/images/screenshot001.bmp?raw=true)
![Channel](https://github.com/antonic901/xbox-youtube/blob/master/images/screenshot005.bmp?raw=true)
![Settings](https://github.com/antonic901/xbox-youtube/blob/master/images/screenshot000.bmp?raw=true)
![Frontend](https://github.com/antonic901/xbox-youtube/blob/master/images/screenshot000.png?raw=true)
