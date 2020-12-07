import tkinter as tk
from tkinter.font import Font
import requests, json, gzip
import sys
import math
from datetime import datetime



#with gzip.open('city.list.json.gz', 'rb') as f:
#	city_list = json.loads(f.read(), encoding="utf-8")
#f = open('shorten_city_list.dat', 'rb')
#city_list = json.loads(f.read())
f = open('state_codes.json', 'rb')
state_list = json.loads(f.read())



def get_json_for(keyword, city, state):
	my_api_key = "&appid=a42f37900713e6f27f6ca0cf3f8cd566&units=imperial"
	base_url = "http://api.openweathermap.org/data/2.5/"
	try:
		return requests.get(base_url + keyword + "?q=" + city + "," + state + my_api_key).json()
	except requests.ConnectionError:
		print("Connection issue")
		sys.exit()

def abbv(state):
	if(len(state) <= 0):
		return ""
	state = state.upper()
	for val in state_list:
		if val["state"] == state:
			return val["name"]
	state = state.lower()
	return state[0].upper() + state[1:]

def print_curr_weather(response, city, state):
	current_temp = response["main"]["temp"]
	desc = response["weather"][0]["description"]
	if(city.strip()):
		state = ', '+state
	tk.Label(root, text = "Current weather for "+city+state)\
					.grid(row=5, column=4, columnspan =2, sticky='nesw')
	tk.Label(root, text = "-----------------------------")\
					.grid( row=6, column=4, columnspan =2, sticky='nesw')
	tk.Label(root, text = "Current temp: "+str(current_temp)+" F")\
					.grid(row=7, column=4, columnspan=2, sticky='nesw')
	tk.Label(root, text = "Description: " + str(desc))\
					.grid(row=10, column=4, columnspan=2, sticky='nesw')
	tk.Label(root, text = "-----------------------------")\
					.grid(row=11, column=4, columnspan =2, sticky='nesw')
	tk.Label(root, text = "Next 5 Days:")\
					.grid(row=12, column=4, columnspan =2, sticky='nesw')

def print_the_forecast(col_num, max, min, desc, date):
	tk.Label(root, text = "Date: " + str(date.month)+"/"+str(date.day))\
					.grid(row=13, column=col_num, columnspan=2, ipadx=int(ws/16), sticky='nesw')
	tk.Label(root, text = "---------------")\
					.grid(row=14, column=col_num, columnspan=2, ipadx=int(ws/16), sticky='nesw')
	tk.Label(root, text = "Max temp: "+ str(max)+" F")\
					.grid(row=15, column=col_num, columnspan=2, sticky='nesw')
	tk.Label(root, text = "Min temp: "+ str(min)+" F")\
					.grid(row=16, column=col_num, columnspan=2, sticky='nesw')
	max_desc_count = 0
	desc_str = ""
	for val in desc:
		if(desc[val] > max_desc_count):
			desc_str = val
			max_desc_count = desc[val]
	tk.Label(root, text = "Description: "+ desc_str)\
					.grid(row=17, column=col_num, columnspan=2, sticky='nesw')

def get_time(timestamp):
	return datetime.utcfromtimestamp(timestamp)

def max_min_desc(list_obj, start, max_val, min_val, desc):
	obj=list_obj[start]
	if obj["weather"][0]["description"] in desc:
		desc[obj["weather"][0]["description"]] += 1
	else:
		desc[obj["weather"][0]["description"]] = 1
	ret_list={}
	if(obj["main"]["temp_max"] > max_val):
		ret_list["max"] = obj["main"]["temp_max"]
	else:
		ret_list["max"] = max_val
	if(obj["main"]["temp_min"] < min_val):
		ret_list["min"] = obj["main"]["temp_min"]
	else:
		ret_list["min"] = min_val
	return ret_list
 

def merge_to_days(forecast_list, curr_weather):
	timezone = curr_weather["timezone"]
	curr_time=get_time(curr_weather["dt"]+timezone)
	num_vals_today=math.floor((24-curr_time.hour)/3)
	curr_max_temp = curr_weather["main"]["temp_max"]
	curr_min_temp = curr_weather["main"]["temp_min"]
	header.grid_remove()
	tk.Label(root, text="Weather App").grid(row=0, column=4, columnspan=2, ipadx=int(ws/16))
	#Deal with the values for rest of day then print them
	for val in range(num_vals_today):
		if(forecast_list[val]["main"]["temp_max"] > curr_max_temp):
			curr_max_temp = forecast_list[val]["main"]["temp_max"]
		elif(forecast_list[val]["main"]["temp_min"] < curr_min_temp):
			curr_min_temp = forecast_list[val]["main"]["temp_min"]
	tk.Label(root, text = "Max temp: "+ str(curr_max_temp)+" F")\
					.grid(row=8, column=4, columnspan=2, sticky='nesw')
	tk.Label(root, text = "Min temp: "+ str(curr_min_temp)+" F")\
					.grid(row=9, column=4, columnspan=2, sticky='nesw')
	#Deal with next 4 days
	for x in range(4):
		start_num = x*8+num_vals_today
		curr_obj= forecast_list[start_num]
		desc = {}
		first_for_comp = max_min_desc(forecast_list, start_num, curr_obj["main"]["temp_max"], curr_obj["main"]["temp_min"], desc)
		max_temp=first_for_comp["max"]
		min_temp=first_for_comp["min"]
		timestamp=curr_obj["dt"]+timezone
		for val in range(7):
			curr_obj=forecast_list[start_num+val+1]
			val = max_min_desc(forecast_list, start_num+val+1, max_temp, min_temp, desc)
			max_temp=val["max"]
			min_temp=val["min"]	
		print_the_forecast(x*2, max_temp, min_temp, desc, get_time(timestamp).date())
	#Deal with final day
	start_num = 32+num_vals_today
	curr_obj=forecast_list[start_num]
	desc={}
	first_for_comp = max_min_desc(forecast_list, start_num, curr_obj["main"]["temp_max"], curr_obj["main"]["temp_min"], desc)
	max_temp=first_for_comp["max"]
	min_temp=first_for_comp["min"]
	desc[curr_obj["weather"][0]["description"]]=1
	for x in range(7-num_vals_today):
		start_num = 32+num_vals_today+x
		val  = max_min_desc(forecast_list, start_num, max_temp, min_temp, desc)
		max_temp=val["max"]
		min_temp=val["min"]
	timestamp=forecast_list[39]["dt"]+timezone
	print_the_forecast(8, max_temp, min_temp, desc, get_time(timestamp).date())

def make_space():
	number_space=int(ws/Font.measure(Font(), " "))
	retStr = ''
	for x in range(number_space):
		retStr += " "
	return retStr
	
def read(event=None):
	city = city_entry.get()
	state = abbv(state_entry.get())
	if(city):
		state_with_comma = ","+state
	else:
		state_with_comma = state
	state = abbv(state)
	response_curr_weather = get_json_for('weather',city,state_with_comma)
	if(str(response_curr_weather["cod"]) == "200" ):
		print_curr_weather(response_curr_weather,city,state)
		forecast_response = get_json_for('forecast',city,state_with_comma)
		merge_to_days(forecast_response["list"], response_curr_weather)
	else:
		spaceVar = make_space()
		tk.Label(root, text = spaceVar).grid(row=5, column=0, columnspan=10)
		tk.Label(root, text = "That is not a valid city").grid(row=5, column = 4, columnspan=2)
		for val in range(12):
			newLabel = tk.Label(root, text = spaceVar)
			newLabel.grid(row = 6+val, column = 0, columnspan=10)

def draw_header():
	tk.Label(root, text="Enter state: ").grid(row=1, column = 4, sticky='e')
	state_entry.configure(background='white', fg='black')
	tk.Label(root, text="Enter city: ").grid(row=2, column = 4, sticky='e')
	city_entry.configure(background='white', fg='black')
	search_button = tk.Button(root, text="Search", command=(lambda : read()))
	search_button.grid(row = 3, column = 5, sticky='w')
	search_button.configure(background='white',fg='black')
	close_button = tk.Button(root, text="Close", command=(lambda : root.destroy()))
	close_button.grid(row = 3, column = 4, sticky='e')
	close_button.configure(background='white',fg='black')
		
#set globals
font_fam = 'Helvetica'
font_size = 12
font_option = 'bold'
root = tk.Tk()
min_height = (font_size+2)*34
ws = int(root.winfo_screenwidth())-50
hs = max(int(root.winfo_screenheight()/2), min_height)
root.geometry("%dx%d+0+25" % (ws,hs))
root.configure(background='blue')
root.option_add('*Background','blue')
root.option_add('*Foreground', 'dark gray') 
gen_font = (font_fam, font_size, font_option)
root.option_add("*Font", gen_font)
root.title("Weather App")
root.bind('<Return>', read)

#start the program
pad=int((ws)/2)
header = tk.Label(root, text="Weather App")
header.grid(row=0, column=4, columnspan=2, ipadx=pad)
state_entry = tk.Entry(root)
state_entry.grid(row=1, column = 5, sticky='w')
city_entry = tk.Entry(root)
city_entry.grid(row=2, column = 5, sticky='w')
draw_header()

root.mainloop()
