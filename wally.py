from requests import get
import json , subprocess , getpass
from random import *

APP_ID = "YOUR_UNSPLASH_APP_API_ID"
URL = "https://api.unsplash.com/search/photos/"
FILE_NAME = "/home/"+getpass.getuser()+"/Pictures/wally.jpg"
PAYLOAD = {"per_page":10,"page":1 }

def fetchImage(app_id , url ,query, payload):
  r = get(url+"?query="+query,params=payload ,headers={'Authorization': 'Client-ID '+app_id})
  r = r.json()
  randomNumber = randint(0, len(r["results"]))
  print("random number is ",randomNumber)
  print(json.dumps(r , indent=2))
  r = r["results"][randomNumber]["links"]["download_location"]
  print(r)
  r = get(r,headers={'Authorization': 'Client-ID '+app_id})
  r = r.json()
  r = r["url"]
  return r
  
  

def saveImage(file_name , url):
  print("save image to "+file_name)
  # open in binary mode
  with open(file_name, "wb") as file:
    # get request
    response = get(url)
    # write to file
    file.write(response.content)

def setWallpaper(file_name):
  print ("wallpaper set from "+file_name)
  result = subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri" ,"'file://"+file_name+"'"] , stdout=subprocess.PIPE)
  print (result.stdout)

subprocess.call(["notify-send" , "Wally", "fetching image"])
imageUrl  = fetchImage(APP_ID , URL , "code",PAYLOAD)
saveImage(FILE_NAME , imageUrl)
setWallpaper(FILE_NAME)
subprocess.call(["notify-send" , "Wally", "wallpaper set :D"])
