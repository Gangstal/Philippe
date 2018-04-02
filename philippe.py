import urllib.request
import praw

try:
    file = open("conf/userdata.txt")
    data = file.read().split("\n")
    name   = data[0]
    pwd    = data[1]
    cid    = data[2]
    secret = data[3]
    file.close()

except FileNotFoundError:
    import os
    os.makedirs("conf")
    file = open("conf/userdata.txt", "w")
    
    name = input("Enter your username: ")
    pwd = input("Enter your password: ")
    cid = input("Enter your client id: ")
    secret = input("Enter your client secret: ")
    file.writelines(name+"\n"+pwd+"\n"+cid+"\n"+secret)
    file.close()

filters = [".png", ".jpeg"]

reddit = praw.Reddit(user_agent='Comment Extraction (by /u/)'+name,
                     client_id=cid, client_secret=secret,
                     username=name, password=pwd)

subreddits = "avocadosgonewild"  #Add more subs with "+"   ex: avocadosgonewild+bananasgonewild

# n is the amount of post you wish to download.
# n must be an integer
# if n is equal to 0, the programm will download until interrupte
def scanPosts(n = 0):
    print(n)
    print("Creating stream...")
    stream = reddit.subreddit(subreddits).top('all')
    i=0
    print("Receiving posts...")
    for post in stream:
        url = post.url.replace("https", "http")
        post_type = postIsPicture(url)
        if post_type != 0:
            if post_type == RAW_IMGUR:
                url+=".png"
            try:
                urllib.request.urlretrieve(url,""+subreddits+"/"+str(i)+".jpeg")
                i+=1
            except urllib.error.HTTPError:
                print("Oopsie doopsie, failed to download picture at URL "+url)
        if i==n:
            break

PICTURE = 1
RAW_IMGUR = 2

def postIsPicture(url):
    for f in filters:
        if f in url:
            return PICTURE
    if "/imgur.com/" in url:
        return RAW_IMGUR
    return 0

