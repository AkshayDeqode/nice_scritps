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

bb_json = []

#####*****BitBucket--Code*****#####

projects = bitbucket.project_list()
users = bitbucket.get_users()
print()

#####*****Gitlab--Code*****#####

gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), os.getenv("GITLAB_TOKEN"))  #Added
gl.auth()


for user_data in users["values"]:

    try:
        user = gl.users.create({'email': user_data["emailAddress"],
                                'force_random_password': True,
                                'username': user_data["name"],
                                'name': user_data["displayName"]})
        print(user)
    except:
        print("User with email : {} already present".format(user_data["emailAddress"]))
