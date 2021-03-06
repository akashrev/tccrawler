from PIL import Image
import requests
from threading import Thread
from io import BytesIO

# f_json = dict()
# image = dict()

threads = 4
height = 400
width = 400

urls = ['http://g-ecx.images-amazon.com/images/G/31/gno/sprites/nav-sprite-global_bluebeacon-1x_optimized._CB295619377_.png',
            'http://g-ecx.images-amazon.com/images/G/31/x-locale/common/transparent-pixel._CB386942716_.gif',
            'http://g-ecx.images-amazon.com/images/G/31/img17/SVD/Feb/1028774_GWHERO_4500X900_GPS._UX1500_SX1500_.jpg',
            'http://g-ecx.images-amazon.com/images/G/31/img16/Gateway/292x292_electronics_2._CB536127208_.png',
            'http://g-ecx.images-amazon.com/images/G/31/img16/Gateway/292x292_fashion_2._CB536127211_.png',
            'http://g-ecx.images-amazon.com/images/G/31/img16/Gateway/292x292_Home_2._CB536127208_.png',
            'http://g-ecx.images-amazon.com/images/G/31/img16/Gateway/292x292_beauty_2._CB536127208_.png',
            'http://g-ecx.images-amazon.com/images/G/31/img16/Gateway/938x1280_without_COD._UX491_SX491_CB526061067_.jpg',
            'http://g-ecx.images-amazon.com/images/G/31/img16/Gateway/938x1280_without_COD._UX491_SX491_CB526061067_.jpg',
            'http://g-ecx.images-amazon.com/images/G/31/img16/Gateway/600x428_todays_deals._CB527352642_.png',
            'http://g-ecx.images-amazon.com/images/G/31/img16/Gateway/600x969_todays_deals._CB527352669_.png']





def body_image_fetch(url):

    response = requests.get(
        url,
        headers={
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36"
        }
    )
    i = Image.open(BytesIO(response.content))

    i = (i.__dict__)
    res = {'mode': i['mode'], 'height': i['size'][0], 'width': i['size'][1], 'mime':response.headers.get('Content-Type'),
               'size':response.headers.get('content-length'), 'url: ':url}
    data.append(res)

while urls:
    data = []
    n_item = []
    n_threads = []
    if len(urls) > threads:
        image_sublist = urls[0:threads]
        print(image_sublist)
        del (urls[0:threads])
    else:
        image_sublist = urls[0:len(urls)]
        del (urls[0:len(urls)])
    # print('a', urls)
    # print('image_sublist', image_sublist)
    # self.urls = urls
    for url in image_sublist:
        t = Thread(target=body_image_fetch, args=(url,data))
        t.start()
        n_threads.append(t)

        for thread in n_threads:
            thread.join()
    print('threading done')
    for item in data:
        # print(item)
        if item['height'] > height and item['width'] > width:
            n_item = item
            height = item['height']
            width = item['width']
        else:
            continue
    # print('f_______',n_item)
    if not n_item:
        continue
    else:
        print ('final', n_item)
        print(type([n_item]))
        break


'''

    i = 0
    while i < len(data):
        print(data[i])
        if data[i]['height'] > height and data[i]['width'] > width:
            # n_item = item
            height = data[i]['height']
            width = data[i]['width']
            if i != 0:
                data.pop(i-1)
        else:
            # print(data)
            data.pop(i)
        i = i + 1
    if not data:
        continue
    else:
        print('f_data',data)
        break


'''

'''
    # while len(data)>1:
    for c, image_data in enumerate(data):
        print(c)
        print('data', data)
        print('image data',image_data)
        print('\n\n')

        if image_data['height'] > height and image_data['width'] > width:
            print('better image ',image_data)
            height = image_data['height']
            width = image_data['width']

            print(height, width)
            print('old data list', data)
            if data[(c-1)>0]:
                print('yes')
                print(c)
                del data[c-1]
                print('new data list', data)
                print('\n\n')
            else:
                print('no')
        else:
            print('image size is not suff', c)
            print('to delete', data[c])
            del data[c]
    print('f_data', data)
    break
'''