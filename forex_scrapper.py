import urllib.request
import os
import time
import datetime
import numpy

if not  os.path.exists("html_files"):
	os.mkdir("html_files")

current_time_step=datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
	
response = urllib.request.urlopen("https://")
	
html = response.read()
f=open("html_files/forex" + current_time_step +".html","wb")
f.write(html)
f.close()
print("requesting ")

time.sleep(numpy.random.randint(60,high=120, size=1))