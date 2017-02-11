import requests

cont = requests.get('http://gigam.es/imtw_Tribez', allow_redirects=True).content
print(cont)


