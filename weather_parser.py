from bs4 import BeautifulSoup
import os
import glob
import pandas as pd

if not os.path.exists("parsed_files"):
	os.mkdir("parsed_files")

df=pd.DataFrame()
truth=pd.DataFrame()
count=1

for file_name in glob.glob("html_files/*.html"):
	print("parsing"+file_name)
	scrapping_time = os.path.splitext(os.path.basename(file_name))[0].replace("weather","")
	f = open(file_name, "r")
	soup=BeautifulSoup(f.read(),'html.parser')
	f.close()
	weather_table=soup.find("table",{"classname":"twc-table"})
	weather_tbody = weather_table.find("tbody")
	weather_rows = weather_tbody.find_all("tr")

	for i in range(1,16):
		weather_time= weather_rows[i].find("td",{"class":"twc-sticky-col "}).find("div",{"class":"hourly-time"}).find("span",{"class":"dsx-date"}).text
		weather_date= weather_rows[i].find("td",{"class":"twc-sticky-col "}).find("div",{"class":"hourly-date"}).text
		weather_condition=weather_rows[i].find("td",{"class":"hidden-cell-sm description"}).find("span").text
		weather_feels=weather_rows[i].find("td",{"class":"feels"}).find("span").text
		weather_temp=weather_rows[i].find("td",{"class":"temp"}).find("span").text
		weather_precip=weather_rows[i].find("td",{"class":"precip"}).find("span",{"class":""}).find("span").text
		weather_humid=weather_rows[i].find("td",{"class":"humidity"}).find("span",{"class":""}).find("span").text
		weather_wind=weather_rows[i].find("td",{"class":"wind"}).find("span").text
		time_away=i
		df = df.append({
			'weather_time': weather_time, 
			'weather_date': weather_date,
			'weather_condition': weather_condition,
			'weather_temp': weather_temp,
			'weather_feels': weather_feels,
			'weather_precip': weather_precip,
			'weather_humid': weather_humid,
			'weather_wind': weather_wind,
			'time_backstep':time_away
			}, ignore_index=True)
df.weather_feels=df.weather_feels.str.strip('Â°')
df.weather_temp=df.weather_temp.str.strip('Â°')
df.weather_humid=df.weather_humid.str.strip('%')
df.weather_precip=df.weather_precip.str.strip('%')
df.weather_wind=df.weather_wind.str.extract('(\d+)')


print(df)
df.to_csv("parsed_files/weatherchanneldata.csv")
	

