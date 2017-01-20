'''
import queue
import threading

q = queue.Queue()
a=2
with open ('testurl.txt', 'r') as url_file:
    for url in url_file:
        q.put(url)

def grab_data_from_queue():
    while not q.empty():
        print (q.get())

for i in range(3):
    print(i)
    t1 = threading.Thread(target=grab_data_from_queue())
    t1.start()  # start the thread
    print('next')

    q.join()


import queue
import threading
import urllib
from urllib.request import Request


# called by each thread
def get_url(q, url):
    q.put(urllib.request.urlopen(url).read())

theurls = ["http://google.com", "http://yahoo.com", "http://twitter.com", "http://fb.com"]

q = queue.Queue()

for u in theurls:
    t = threading.Thread(target=get_url, args = (q,u))
    t.daemon = True
    t.start()

s = q.get()
print (s)
print('\n')



'''






#!/usr/bin/python

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("Starting " + self.name)
        print_time(self.name, self.counter, 5)
        print ("Exiting " + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

print ("Exiting Main Thread")
