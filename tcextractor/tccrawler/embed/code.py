from ..scraper.parser import Fetch
import re


def embed_video(url):
    try:
        provider_name = (Fetch(url, "").expand_url(url))['provider_name']
        if provider_name in ["youtu", "youtube"]:
            yid = url.split('/')[-1]
            if '?' in yid:
                yid = yid.split('?')[0]
            return '<iframe width="560" height="315" src="https://www.youtube.com/embed/"'+yid+'" frameborder="0" allowfullscreen></iframe>'

        elif provider_name == "vmeo":
            vid = url.split('/')[-1]
            vid = re.search(r'^(clip_id)?(\d+)', vid)
            return vid.group(1)

        # elif provider_name == 'vine':
        #     return url
        else:
            return url
    except Exception as e:
        print(e)

"""
https://player.vimeo.com/video/192650605?autoplay=1
https://vimeo.com/moogaloop.swf?clip_id=192650605&amp;autoplay=1
# url = "https://vimeo.com/moogaloop.swf?clip_id=192650605&amp;autoplay=1"

"""

"""
<iframe src="https://player.vimeo.com/video/192650605?title=0&byline=0&portrait=0&badge=0" width="640" height="268" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
<p><a href="https://vimeo.com/192650605">MA by Celia Rowlson-Hall</a> from <a href="https://vimeo.com/factory25">Factory 25</a> on <a href="https://vimeo.com">Vimeo</a>.</p>
"""

"""https://youtu.be/S5X1s8YAgj8"""

"""
<iframe width="560" height="315" src="https://www.youtube.com/embed/S5X1s8YAgj8" frameborder="0" allowfullscreen></iframe>
"""