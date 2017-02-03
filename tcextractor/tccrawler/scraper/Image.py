from io import BytesIO
import logging
from PIL import Image
from threading import Thread
from .parser import Fetch


class Image_size:
    def __init__(self):
        self.allowed_types = ['image/jpeg', 'text/html', 'image/jpg', 'image/png', 'image/gif', 'image/webp',
                              'image/tiff', 'image/bmp', ""]
        self.threads = 4
        self.width = 300
        self.height = 300

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
            logging.exception("ERROR message")
        return res

    def body_image_fetch(url, data):

        response = Fetch(url, "").get_url_data()

        i = Image.open(BytesIO(response.content))

        i = i.__dict__
        res = {'mode': i['mode'], 'height': i['size'][0], 'width': i['size'][1],
               'mime': response.headers.get('Content-Type'),
               'size': response.headers.get('content-length'), 'url: ': url}
        data.append(res)

    def get_best_images(self, urls):
        while urls:
            data = []
            n_item = []
            n_threads = []
            if len(urls) > self.threads:
                image_sublist = urls[0:self.threads]
                print(image_sublist)
                del (urls[0:self.threads])
            else:
                image_sublist = urls[0:len(urls)]
                del (urls[0:len(urls)])
            for url in image_sublist:
                t = Thread(target=Image_size.body_image_fetch, args=(url, data))
                t.start()
                n_threads.append(t)

                for thread in n_threads:
                    thread.join()
            print('threading done')
            for item in data:
                # print(item)
                if item['height'] > self.height and item['width'] > self.width:
                    n_item = item
                    self.height = item['height']
                    self.width = item['width']
                else:
                    continue
            if not n_item:
                continue
            else:
                print(n_item)
                return [n_item]
            break




'''
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

'''