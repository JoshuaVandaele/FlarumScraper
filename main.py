import requests
import getpass
import json
from datetime import datetime
import os

##  CONFIGS  ##

prettyprint_json_file=False
indent=0
pages_to_scrap = ["discussions","users","posts"]

###############

print("Flarum Forum Scrapper V1.1 - By Folfy_Blue")
forumUrl = input("Forum URL: ")

## FUNCTIONS ##

def login():
	payload = {
		'identification': input("Username: "),
		'password': getpass.getpass(),
		'remember': True
	}
	
	session = requests.Session()
	r = session.post("https://"+forumUrl+"/api/token", data=json.dumps(payload), headers = {"Content-Type": "application/vnd.api+json"})

	if r.status_code == 200:
		token = json.loads(r.content)["token"]
		session.cookies.set("flarum_remember",token, domain=forumUrl)
		return session

def scrapPage(session,page):
	print("Scrapping "+page)
	data = [] #not good for memory usage because I have a lot of it, fuck you
	nextUrl = "https://"+forumUrl+"/api/"+page
	while True:
		print("Getting data from '"+nextUrl+"'..",end="\r")
		current = session.get(nextUrl)
		content = json.loads(current.content)
		data.append(content["data"])
		if "next" in content["links"]:
			nextUrl = content["links"]["next"]
		else:
			print("\nDone! Got all "+page+" data.")
			return data

def storeData(data,filename,time):
	path = forumUrl+'/'+time+"/"
	if not os.path.exists(forumUrl):
		os.mkdir(forumUrl)
	if not os.path.exists(path):
		os.mkdir(path)

	with open(path+filename+".json", 'w', encoding='utf-8') as f:
	    json.dump(data, f, ensure_ascii=False, sort_keys=prettyprint_json_file, indent=indent)
	print("Data wrote to '"+path+filename+"'!")

################

session = login()
while not session:
	print("Failed to log in!")
	session = login()

print("Logged in!")

scrapTime = datetime.now().strftime("%Y-%m-%d %H;%M;%S")

for page in pages_to_scrap:
	print()
	storeData(scrapPage(session,page),page,scrapTime)

print("-== Finished! ==-")
