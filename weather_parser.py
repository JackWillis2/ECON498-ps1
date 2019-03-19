from bs4 import BeautifulSoup
import os
import glob
import pandas as pd

if not os.path.exists("parsed_files"):
	os.mkdir("parsed_files")

df=pd.DataFrame

for file_name in glob.glob("html_files/*.html"):
	print("parsing"+file_name)
	scrapping_time = os.path.splitext(os.path.basename(file_name))[0].replace("weather","")
	f = open(file_name, "r")
	soup=BeautifulSoup(f.read(),'html.parser')
	f.close()
	weather_table=soup.find("table",{"classname":"twc-table"})
	weather_tbody = weather_table.find("tbody")
	weather_rows = weather_tbody.find_all("tr")
weather_time= weather_rows[0].find("td",{"class":"twc-sticky-col "}).find("div",{"class":"hourly-time"}).find("span",{"class":"dsx-date"}).text
print(weather_time)