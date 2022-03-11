from importlib.metadata import requires
import json
from optparse import Values
import requests
from requests.auth import HTTPBasicAuth
import gitlab
from atlassian import Bitbucket
from pprint import pprint
import ast
import deepdiff
from dotenv import load_dotenv
import os
from datetime import datetime 

load_dotenv()

bitbucket = Bitbucket(
    url=os.getenv("BITBUCKET_URL"),
    username=os.getenv("BITBUCKET_USERNAME"),
    password=os.getenv("BITBUCKET_PASSWORD")
)

bb_files = {}
bb_projects = bitbucket.project_list()
# print(projects)
# import pdb;pdb.set_trace()

# import pdb;pdb.set_trace()

for project in bb_projects:
    # print(project)
    proj_key = project["key"]
    repos = bitbucket.repo_list(proj_key)
    for repo in repos:
        repo_name=repo['name']
        bb_files[repo_name] = {}
        branches = bitbucket.get_branches(proj_key, repo.get("name"), details=False)
        for branch in branches:
            branch_name=branch['displayId']
            # print(branch_name)
            url="http://localhost:7990/rest/api/1.0/projects/{}/repos/{}/files?at={}".format(proj_key,repo_name,branch_name)
            request = requests.get(url,auth=HTTPBasicAuth(os.getenv("BITBUCKET_USERNAME"), os.getenv("BITBUCKET_PASSWORD")))
            data = request.json()
            bb_files[repo_name][branch['displayId']] = data['values']



gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), os.getenv("GITLAB_TOKEN"))

gl.auth()
projects = gl.projects.list()

git_files = {}
final_git_files ={}

for project in projects:
    branches = project.branches.list()
    files_list = {}
    git_files[project.attributes['name']]={}
    for branch in branches:
        git_files[project.attributes['name']][branch.name]=[]
        items = project.repository_tree(path="", recursive=True, all=True, ref=branch.name)
        for item in items:
            # print(item)
            if item["type"] != "tree":
                if branch.name not in files_list:
                    files_list[branch.name] = []
                files_list[branch.name].append(item["path"])
                files_list[branch.name] = sorted(files_list[branch.name])
        # print(files_list[branch.name])
        git_files[project.attributes['name']][branch.name]=files_list[branch.name]
        # git_files.update({project.attributes["name"]: sorted(files_list.items(), key = lambda x: x[0])})

# print("Showing bitbucket Files")
# print(bb_files)



# print("Showing Gitlab Files")
# print(git_files)