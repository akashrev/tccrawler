from PIL import Image
import requests
import time
from io import BytesIO

st1 = time.time()

data = requests.get("https://media.giphy.com/media/l2R0aKwejYr8ycKAg/giphy.gif").content

def colour(data):
    i = Image.open(BytesIO(data))
    if i.mode == "RGB":
        h = i.histogram()
        return (
                sum(i * w for i, w in enumerate(h[0: 256])) / sum(h[0: 256]),
                sum(i * w for i, w in enumerate(h[256: 256 * 2])) / sum(h[256: 256 * 2]),
                sum(i * w for i, w in enumerate(h[256 * 2: 256 * 3])) / sum(h[256 * 2: 256 *3]),
            )
    elif i.mode == "RGBA":
        h = i.histogram()
        return (
            sum(i * w for i, w in enumerate(h[0: 256])) / sum(h[0: 256]),
            sum(i * w for i, w in enumerate(h[256: 256 * 2])) / sum(h[256: 256 * 2]),
            sum(i * w for i, w in enumerate(h[256 * 2: 256 * 3])) / sum(h[256 * 2: 256 * 3]),
            sum(i * w for i, w in enumerate(h[256 * 3: 256 * 4])) / sum(h[256 * 3: 256 * 4]),
        )
    elif i.mode == "P":
        h = i.getpalette()
        return (
            sum(i * w for i, w in enumerate(h[0: 256])) / sum(h[0: 256]),
            sum(i * w for i, w in enumerate(h[256: 256 * 2])) / sum(h[256: 256 * 2]),
            sum(i * w for i, w in enumerate(h[256 * 2: 256 * 3])) / sum(h[256 * 2: 256 * 3]),
        )
print(colour(data))
print(time.time() - st1)