from PIL import Image
import requests
from threading import Thread
from io import BytesIO

threads = 4

f_json = dict()
image = dict()

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





def body_image_fetch(url,data):

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
    #
    # print('mode: ',i['mode'])
    # # print(i['size'])
    # print('height: ',i['size'][0])
    # print('width: ',i['size'][1])
    #
    # print('mime: ',response.headers.get('Content-Type'))
    # print('size: ',response.headers.get('content-length'))
    # return i_json


while urls:
    data = []
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
        print (str(url))
        t = Thread(target=body_image_fetch, args=(url,data))
        t.start()
        n_threads.append(t)

        for thread in n_threads:
            thread.join()

        for image_data in data :
            print(image_data)
            if(image_data['height']>200 and image_data['width']>200):
                print('..................',image_data)
                break
        break
    break

        # print(target)

