import requests
import re
import json

# url = \
#     "https://brandnewsblog.com/2017/01/15/300-twittos-du-marketing-et-de-la-communication-en-suivre-en-2017/"



with open('../../urls.json') as file:
    file = json.load(file)
    provider_name = ""
    for url in file:
        try:

            origin = requests.head(url, allow_redirects=True).url

            urlregex = "((?:http|ftp)s?):\/\/(?:www)?\.?(([^\.]+)\.([^\/\.]+)\.?([^\/\.]+)?\.?([^\/\.]+)?)(.+)?"

            print origin
            if 'com' in re.search(urlregex, origin).group(2).split('.'):  # if '.com' in the end of url, fetcjh just previous word
                com_index = (re.search(urlregex, origin).group(2).split('.')).index("com")
                provider_name = re.search(urlregex, origin).group(2).split('.')[com_index-1]



            elif origin.split('/')[2].split('.')[0] == 'www':
                provider_name = re.search(urlregex, origin).group(2).split('.')[0]



            elif len(re.search(urlregex, origin).group(2).split('.')) == 2:  # if len of url is 2 then fetch out first word
                provider_name = re.search(urlregex, origin).group(3)


            elif len(re.search(urlregex, origin).group(2).split('.')) == 3:  # if length of url is 3
                if len(re.search(urlregex, origin).group(5)) == 2:  # if the last word of url is of length 2
                    if len(re.search(urlregex, origin).group(4)) != 2:
                        provider_name = re.search(urlregex, origin).group(4)
                    else:
                        provider_name = re.search(urlregex, origin).group(3)
                else:
                    provider_name = re.search(urlregex, origin).group(4)
            elif len(re.search(urlregex, origin).group(2).split('.')) == 4:
                provider_name = re.search(urlregex, origin).group(4)
            else:
                provider_name = re.search(urlregex, origin).group(3)
            print provider_name
            with open('../../nresult.log', 'a') as result:
                result.write(origin)
                result.write('\n')
                result.write(provider_name)
                result.write('\n')
                result.write('\n')
        except Exception as e:
            print(e)
            continue
