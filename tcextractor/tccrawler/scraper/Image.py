from io import BytesIO
import logging
from PIL import Image
from threading import Thread
from .parser import Fetch

class Image_size:
    def __init__(self):
        self.allowed_types = ['image/jpeg', 'text/html', 'image/jpg', 'image/png', 'image/gif', 'image/webp',
                              'image/tiff', 'image/bmp', ""]
        self.width = 300
        self.height = 300

    def get_best_images(self, urls):
        images, header = {}, {"length": 0}
        headers = []
        for url in urls:
            if url:
                header = Fetch(url, "").get_header()
                headers.append(header)
            if header:
                images.update({url: int(header)})
        return self.get_5_url(images)

    def get_5_url(self, images):
        response, threads, res = [], [], []
        count = 1
        for url in sorted(images, key=images.__getitem__)[-5:]:
            thread = Thread(target=self.get_image_dimension, args=(url, response, count))
            thread.start()
            count += 1
            threads.append(thread)

        for thread in threads:
            thread.join()
        print()
        for data in response:
            if data["width"] >= self.width and data["height"] >= self.height:
                self.height = data["height"]
                self.width = data["width"]
                res.append(data)
        return res

    #########
    def get_image_dimension(self, url, response, count):
        res = ""
        try:
            fetch_obj = Fetch(url, Fetch(url, "").get_url_data())
            header = fetch_obj.get_header()
            raw = fetch_obj.get_content(raw=True)
            print(url)
            if header["status"] == 200 and header["type"] in self.allowed_types:
                im = Image.open(BytesIO(raw))
                res = {
                    "url": url,
                    "width": int(im.size[0]),
                    "height": int(im.size[1]),
                    "ratio": float((im.size[1] / im.size[0]) * 100),
                    "size": im.size[0]*im.size[1] if header["length"] == 0 else header["length"],
                    "mime": str(header["type"]),
                }
                response.insert(count, res)
        except Exception:
            logging.exception("ERROR meassage")
        return res
