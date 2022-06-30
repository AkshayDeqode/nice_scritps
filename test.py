from optparse import Values
from traceback import print_tb
import gitlab
from atlassian import Bitbucket
from pprint import pprint
import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import time
load_dotenv()

bitbucket = Bitbucket(
    url=os.getenv("BITBUCKET_URL"),
    username=os.getenv("BITBUCKET_USERNAME"),
    password=os.getenv("BITBUCKET_PASSWORD"),
)

bb_logs = {}
projects_v1 = bitbucket.project_list()

gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), os.getenv("GITLAB_TOKEN"))
gl.auth()
gl_logs = {}

report =  {"name": [], "id":[],"repo_url":[],"ssh_repo_url":[]}
group = gl.groups.get(id=3443,lazy=True)
projects = group.projects.list()
for item in projects:
    print(item)


















# with open('datafile.txt', 'r') as f:
#     for line in f:
#         group = gl.groups.get(line)
#         project_lst=group.projects.list(as_list=False)
#         for item in project_lst:
#             # print(item)
#             report["name"].append(item.name)
#             report["id"].append(item.id)
#             report["repo_url"].append(item.http_url_to_repo)
#             report["ssh_repo_url"].append(item.ssh_url_to_repo)
# report = pd.DataFrame(report)
# print(report)
# if not os.path.exists('/home/ec2-user/cs-migration-setup/final_scripts/nice_scritps/data/data_url'):
#     os.mkdir('/home/ec2-user/cs-migration-setup/final_scripts/nice_scritps/data/data_url')
#     os.chdir("/home/ec2-user/cs-migration-setup/final_scripts/nice_scritps/data/data_url")
#     report.to_csv("/home/ec2-user/cs-migration-setup/final_scripts/nice_scritps/data/data_url/data_url.csv", mode="a", header=False, index=False)
# else:
#     print("create file")



