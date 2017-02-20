import requests
import time

url = 'http://www3.weforum.org/docs/IP/2016/CO/WEF_AM17_FutureofRetailInsightReport.pdf'

t1 = time.time()
r = requests.get(url)
print(r.headers["content-type"])
if r.headers["content-type"] in ['application/pdf', 'pdf']:
    print('yes')
print(time.time() - t1)

