from urlparse import urlparse
# from urllib.parse import urlparse
import requests
import re
import json

# url = \
#     "https://brandnewsblog.com/2017/01/15/300-twittos-du-marketing-et-de-la-communication-en-suivre-en-2017/"



with open('../../urls.json') as file:
    file = json.load(file)
    p_name = ""
    for url in file:
        try:

            origin = requests.head(url, allow_redirects=True).url

            urlregex = "((?:http|ftp)s?):\/\/(?:www)?\.?(([^\.]+)\.([^\/\.]+)\.?([^\/\.]+)?\.?([^\/\.]+)?)(.+)?"

            # print re.search(urlregex, origin).group(0)
            # print 'full url:', re.search(urlregex, origin).group(1)                     # http://www.google.co.in
            # print 'http:', re.search(urlregex, origin).group(2)                         # http | https
            # print 'after http:', re.search(urlregex, origin).group(3)                   # google.co.in
            # print 'provider name:', re.search(urlregex, origin).group(4)                # google
            # print 'after pname:', re.search(urlregex, origin).group(5)                  # co
            # print 'after after pname:', re.search(urlregex, origin).group(6)            # in

            # if len(re.search(urlregex, origin).group(1).split('.')[-1]) == 2:
            #     print 'provider name:', re.search(urlregex, origin).group(3).split('.')[-2]

            # print len(re.search(urlregex, origin).group(3).split('.'))
            print origin
            if 'com' in re.search(urlregex, origin).group(2).split('.'):            # if '.com' in the end of url, fetcjh just previous word
                p_name = re.search(urlregex, origin).group(2).split('.')[-2]
                print 'provider name:', re.search(urlregex, origin).group(2).split('.')[-2]

            elif origin.split('/')[2].split('.')[0] == 'www':
                provider_name = re.search(urlregex, origin).group(2).split('.')[0]
                print 'provider name :',provider_name

            elif len(re.search(urlregex, origin).group(2).split('.')) == 2:         # if len of url is 2 then fetch out first word
                print 'provider name:', re.search(urlregex, origin).group(3)
                p_name = re.search(urlregex, origin).group(3)

            elif len(re.search(urlregex, origin).group(2).split('.')) == 3:         # if length of url is 3
                # print 'after pname:', re.search(urlregex, origin).group(5)
                # print re.search(urlregex, origin).group(1).split('.')
                # if 'www' in re.search(urlregex, origin).group(1).split('.'):
                if len(re.search(urlregex, origin).group(5)) == 2:                  # if the last word of url is of length 2
                    if len(re.search(urlregex, origin).group(4)) != 2:
                        print 'provider name:', re.search(urlregex, origin).group(4)
                        p_name = re.search(urlregex, origin).group(4)
                    else:
                        print 'provider name:', re.search(urlregex, origin).group(3)
                        p_name = re.search(urlregex, origin).group(3)
                else:
                    print 'provider name:', re.search(urlregex, origin).group(4)
                    p_name = re.search(urlregex, origin).group(4)
            elif len(re.search(urlregex, origin).group(2).split('.')) == 4:
                print 'provider name:', re.search(urlregex, origin).group(4)
                p_name = re.search(urlregex, origin).group(4)
            # print p_name
            with open ('../../result.log' ,'a') as result:
                result.write(origin)
                result.write('\n')
                result.write(p_name)
                result.write('\n')
                result.write('\n')
        except Exception as e:
            print(e)
            continue
