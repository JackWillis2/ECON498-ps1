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

	for rows in weather_rows:
		weather_time= weather_rows[rows].find("td",{"class":"twc-sticky-col "}).find("div",{"class":"hourly-time"}).find("span",{"class":"dsx-date"}).text
		weather_condition=weather_rows[rows].find("td",{"class":"hidden-cell-sm description"}).find("span").text
		weather_feels=weather_rows[rows].find("td",{"class":"feels"}).find("span").text
		weather_temp=weather_rows[rows].find("td",{"class":"temp"}).find("span").text
		weather_precip=weather_rows[rows].find("td",{"class":"precip"}).find("span",{"class":""}).find("span").text
		weather_humid=weather_rows[rows].find("td",{"class":"humidity"}).find("span",{"class":""}).find("span").text
		weather_wind=weather_rows[rows].find("td",{"class":"wind"}).find("span").text
		print(weather_time)


