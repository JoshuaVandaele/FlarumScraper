import webbrowser
import os
import json


forum = "bruh"
snapshot = "moment"

while not os.path.exists(forum):
	print("Which forum's history do you wish to sort?")
	for item in os.listdir():
		if os.path.isdir(item):
			print("- "+item)
	forum = input("> ")

while not os.path.exists(forum+"/"+snapshot):
	print("Which of these snapshots do you wish to use?")
	for item in os.listdir(forum):
		if os.path.isdir(forum+"/"+item): #If the item is a directory
			print("- "+item)
	snapshot = input("> ")

directory = forum+"/"+snapshot+"/"

print("Loading the files into memory, please wait..")

files = {}
for item in os.listdir(directory):
	if not os.path.isdir(directory+item): #If it's not a directory
		with open(directory+item, encoding="utf8") as file:
			print("Loading "+item+"..")
			files[item] = json.load(file)
			print("Done!")


threads = {}
posts = {}
users = {}

users["0"] = {"username":"[Deleted User]"}

# users
for arraycontent in files["users.json"]["data"]: #List of arrays
	if arraycontent["type"] == "users":
		key = str(arraycontent["id"])
		users[key] = {}
		users[key]["username"] = arraycontent["attributes"]["username"]

#posts
for arraycontent in files["posts.json"]["data"]:
	if arraycontent["type"] == "posts":
		key = str(arraycontent["id"]) # Post ID
		posts[key] = {}

		if "contentHtml" in arraycontent["attributes"]:
			posts[key]["contentHtml"] = arraycontent["attributes"]["contentHtml"]
		else:
			posts[key]["contentHtml"] = "POST HAS BEEN DELETED"
		posts[key]["createdAt"] = arraycontent["attributes"]["createdAt"]

		if not "user" in arraycontent["relationships"]: #Deleted user
			posts[key]["userID"] = 0
		else:
			posts[key]["userID"] = arraycontent["relationships"]["user"]["data"]["id"]

		posts[key]["likes"] = []
		for data in arraycontent["relationships"]["likes"]["data"]:
			posts[key]["likes"].append(data["id"])

		posts[key]["threadID"] = arraycontent["relationships"]["discussion"]["data"]["id"] or -1
		posts[key]["username"] = users[str(posts[key]["userID"])]["username"] or "[Deleted User]"

#discussions
for arraycontent in files["discussions.json"]["data"]: #List of arrays
	if arraycontent["type"] == "discussions":
		key = str(arraycontent["id"]) # Post ID
		postID = arraycontent["relationships"]["firstPost"]["data"]["id"]
		threads[key] = {}
		threads[key]["title"] = arraycontent["attributes"]["title"]
		threads[key]["comments"] = {}
		threads[key]["postID"] = postID
		threads[key]["slug"] = arraycontent["attributes"]["slug"]
		threads[key]["tags"] = []
		for data in arraycontent["relationships"]["tags"]["data"]:
			threads[key]["tags"].append(data["id"])

#Put everything together to get threads
for postID,arraycontent in posts.items():
		threadID = posts[postID]["threadID"]
		if threadID in threads:
			if (not threads[threadID]["postID"] == postID):
				threads[threadID]["comments"][postID] = arraycontent
			else:
				threads[threadID]["contentHtml"] = posts[postID]["contentHtml"]
				threads[threadID]["username"] = posts[postID]["username"]
				threads[threadID]["createdAt"] = posts[postID]["createdAt"]
				threads[threadID]["likes"] = posts[postID]["likes"]
				threads[threadID]["userID"] = posts[postID]["userID"]

"""
users
{
	ID: {"username":""}
}

posts
{
	contentHtml
	createdAt
	likes
	userID
	threadID
}

threads
THREADID: { #DONE
	title:"", #DONE
	userID:"", #DONE
	username:"", #DONE
	contentHtml:"", #DONE
	createdAt:"", #DONE
	postID:"", #DONE
	slug:"",
	comments: {
		postID:{
			userID:"", #DONE
			username:"", #DONE
			contentHtml:"", #DONE
			createdAt:"", #DONE
			likes: [] #DONE
		}
	},
	likes: [], #DONE
	tags:[] #DONE
}
"""


if not os.path.exists(directory+"SortedThreads/"):
	os.mkdir(directory+"SortedThreads/")

c = 0
for threadID,threadData in threads.items():
	print("Storing threads. ("+str(c)+"/"+str(len(threads))+")",end="\r")
	with open(directory+"SortedThreads/"+threadData["slug"]+".json", "w") as f:
		json.dump(threadData,f)
	c+=1
print("\nDone!")
