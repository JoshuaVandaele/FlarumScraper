import requests
import getpass
import json
from datetime import datetime
import os

print("Flarum Forum Scrapper V1.0 - By Folfy_Blue")
forumUrl = input("Forum URL: ")

###############

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
		print("Getting data from '"+nextUrl+"'..")
		current = session.get(nextUrl)
		content = json.loads(current.content)
		data.append(content["data"])
		if "next" in content["links"]:
			nextUrl = content["links"]["next"]
		else:
			print("Done! Got all "+page+" data.")
			return data

################

session = login()
while not session:
	print("Failed to log in!")
	session = login()

print("Logged in!")

data = {
	"discussions": scrapPage(session,"discussions"),
	"posts": scrapPage(session,"posts"),
	"users": scrapPage(session,"users")
}

print("Writting to file...")
path = forumUrl+'/'
filename = datetime.now().strftime("%Y%m%d-%H%M%S")+'.json' #YYMMDD-HHMMSS format

if not os.path.exists(path):
	os.mkdir(path)

with open(path+filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

print("Data wrote to '"+path+filename+"'!")
