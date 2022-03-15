from importlib.metadata import requires
import gitlab
from atlassian import Bitbucket
from pprint import pprint
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime 

load_dotenv()

bitbucket = Bitbucket(
    url=os.getenv("BITBUCKET_URL"),
    username=os.getenv("BITBUCKET_USERNAME"),
    password=os.getenv("BITBUCKET_PASSWORD")
)

bb_logs = {}

projects = bitbucket.project_list()

for project in projects:
    proj_key = project["key"]

    repos = bitbucket.repo_list(proj_key)
    for repo in repos:
        branches = bitbucket.get_branches(proj_key, repo.get("name"), details=False)
        for branch in branches:
            bitbucket.set_default_branch(proj_key, repo.get("name"), branch.get("displayId"))
            branch_commits = bitbucket.get_commits(proj_key, repo.get("name"))
            for commit in branch_commits:
                message = commit["message"].replace("\n", "")
                bb_logs[commit.get("id")] = [message, commit.get("author").get("displayName"),commit.get('author').get('emailAddress'), commit.get('authorTimestamp') ]
        bitbucket.set_default_branch(proj_key, repo.get("name"), 'master')

# #####*****Gitlab--Code*****#####

gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), os.getenv("GITLAB_TOKEN"))  #Added
gl.auth()
gl_logs = {}

projects = gl.projects.list()
for project in projects:

    branches= project.branches.list()
    for branch in branches:
        commits = project.commits.list(ref_name=branch.name)
        for commit in commits:
            commit = commit.__dict__["_attrs"]
            message = commit["message"].replace("\n", "")
            if "+00:00" in commit['committed_date']:
                gitlab_utc = datetime.strptime(commit['committed_date'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
            else:
                gitlab_utc = datetime.strptime(commit['committed_date'], '%Y-%m-%dT%H:%M:%S.%f+05:30')
            gitlab_timestamp = int(datetime.timestamp(gitlab_utc)*1000)
            gl_logs[commit["id"]] = [message, commit["author_name"].lower(), commit['committer_email'],gitlab_timestamp]


# #####*****Gitlab--Code*****#####

report={"commit_id":[], "commit_message":[], "difference_location":[]}
for key,value in bb_logs.items():
    if gl_logs.get(key,value[0])  != bb_logs.get(key,value[0]):
        report["commit_id"].append(key)
        report["commit_message"].append(value[0])
        report["difference_location"].append("Gitlab")
report=pd.DataFrame(report)

if len(report):  
    print(report)
else:
    print("NO DIFFERENCES FOUND")