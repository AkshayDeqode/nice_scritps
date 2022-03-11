from importlib.metadata import metadata
import pprint
import gitlab
from atlassian import Bitbucket
from dotenv import load_dotenv
import os

load_dotenv()

bitbucket = Bitbucket(
    url=os.getenv("BITBUCKET_URL"),
    username=os.getenv("BITBUCKET_USERNAME"),
    password=os.getenv("BITBUCKET_PASSWORD")
)

gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), os.getenv("GITLAB_TOKEN"))  #Added
gl.auth()

###********Getting users from Bitbucket********###
def get_bb_users():
    users = bitbucket.get_users()

    refined = {}

    for value in users["values"]:  #Replace data by commit2
        temp = {value["name"].lower(): [value["emailAddress"].lower(), value["displayName"].lower()]}
        refined.update(temp)
    
    return refined

###********Getting users from Gitlab********###
def get_gl_users():
    
    users = gl.users.list()

    refined = {}

    for user in users:    #Replace data by commit_1
        user_data = user.attributes
        # print(user_data['username'])
        if user_data['username'] not in ["root", "ghost"]:
            temp = {user_data["username"].lower(): [user_data["email"].lower(), user_data["name"].lower()]}
            refined.update(temp)
    return refined


print("Bitbucket Users")
bb_users = get_bb_users()
print(bb_users)
print("Gitlab Users")
gl_users = get_gl_users()
print(gl_users)


extra_users = set(bb_users.keys()) - set(gl_users.keys())
if extra_users:
    print("Users {} are not available on gitlab".format(", ".join(extra_users)))
       
