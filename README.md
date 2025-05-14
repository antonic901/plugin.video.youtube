## Invidious based YouTube addon for Original Xbox and XBMC
This is YouTube addon which utilize unofficial YouTube API from Invidious project. It aims to resurrect YouTube streaming on this ancient 20+ years old hardware.

## How to install
Use official repository of XBMC to install this addon.

## Important Info:
With latest changes of Google lot of public Inivdious instances are no longer working or are partially working. It's recommended to run self-hosted instance. You can find more info [here](https://docs.invidious.io/installation/#docker-compose-method-production). Using self-hosted instance you will bypass region blocking because video stream urls will be generated for your's region (country).

## F.A.Q
### 1. Some videos don't play. Why?

There is lot of reasons, but some of them can be:
- Region blocking - For example you are located in Europe, but you are using Invidious instance from UK/US. Some videos will work but most of them won't because of region blocking. To fix this you must use instance from your country or [self-hosted](https://docs.invidious.io/installation/#docker-compose-method-production) instance.

- Missing streams - There are some videos which don't have valid streams. This is issue with some real old videos. There is no help for this.

- IP address of instance is blocked by Google - this is case with most public instances. If you are running [self-hosted]() instance restart you router to get new public IP address and try again. Advace - don't expose self-hosted instance to the public!
