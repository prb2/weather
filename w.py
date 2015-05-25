#! /usr/bin/env python

import sys
import urllib2, urllib
import json


usage = "Usage: \"./w.py <city> <today/tomorrow/week/sun/wind>\""

if (len(sys.argv) > 1):
	city = sys.argv[1]

	base = "http://query.yahooapis.com/v1/public/yql?"

	query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="' + city + '" ) and u="f"'

	# query = "select wind from weather.forecast where woeid=2460286"

	url = base + urllib.urlencode({'q':query}) + "&format=json"

	result = urllib2.urlopen(url).read()

	data = json.loads(result);
	
	if (data["query"]["results"] == None):
			print "Invalid city. Please try again."
			sys.exit(0)

	channel = data["query"]["results"]["channel"]; 

	temp = channel["units"]["temperature"]
	speed = " " + channel["units"]["speed"]

	location = channel["location"]
	print "* " + location["city"] + ", " + location["country"]

	
	# print json.dumps(data, sort_keys=True, indent=4, separators=(',',': '))

	print "*"
	
	if (len(sys.argv) == 2):
		current = channel["item"]["condition"]
		print "* Currently " + current["temp"] + " " + temp +  ", " + current["text"]
	else :
		option = sys.argv[2]
		forecast = channel["item"]["forecast"]
		
		if (option == "today"):
			today = forecast[0]
			print "* " + today["day"] + " " + today["date"]
			print "* " + today["text"] + ", with a high of " + today["high"] +  " " + temp + " and a low of " + today["low"] +  " " + temp

		elif (option == "tomorrow"):
			tomorrow = forecast[1]
			print "* " + tomorrow["day"] + " " + tomorrow["date"]
			print "* " + tomorrow["text"] + ", with a high of " + tomorrow["high"] + " " +  temp + " and a low of " + tomorrow["low"] + " " + temp
		
		elif (option == "week"):
				for day in forecast:
					print "* " + day["day"] + " " + day["date"]
					print "* " + day["text"] + ", with a high of " + day["high"] +  " " + temp + " and a low of " + day["low"] +  " " + temp
					if (day != forecast[len(forecast)-1]):
							print "* "

		elif (option == "wind"):
			wind = channel["wind"]
			print "* ~ Wind ~"
			print "* Chill:     " + wind["chill"] +  " " + temp
			print "* Direction: " + wind["direction"] + " degrees"
			print "* Speed:     " + wind["speed"] + speed
		
		elif (option == "sun"):
			sun = channel["astronomy"] 
			print "* Sunrise: " + sun["sunrise"]
			print "* Sunset:  " + sun["sunset"]

		elif (option == "umbrella"):
			# tells you if you need an umbrella or not
			temp = "asdf"

		else  :
			print "* Invalid option."
			print ""
			print usage

	print ""
else :
	print usage
