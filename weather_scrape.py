import urllib.request
import os
import time
import datetime
import numpy

if not  os.path.exists("html_files"):
	os.mkdir("html_files")

for i in range(120):
	current_time_step=datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
	response = urllib.request.urlopen("https://weather.com/weather/hourbyhour/l/29634:4:US")
	html = response.read()
	print(html)
	f=open("html_files/weather" + current_time_step +".html","wb")
	f.write(html)

	f.close()
	print("requesting weather channel again this hour")
	time.sleep(3600)

