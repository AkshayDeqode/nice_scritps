from importlib.metadata import requires
import gitlab
from atlassian import Bitbucket
from pprint import pprint
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

bb_json = {}

projects = bitbucket.project_list()
# print(projects)

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
                # if not commit.get("id") in bb_json:
                #     message = commit["message"]
                #     if "/" in commit["message"]:
                #         message = commit["message"].split("/")[1].split("\n")[0]
                bb_json[commit.get("id")] = [message, commit.get("author").get("displayName"),commit.get('author').get('emailAddress'), commit.get('authorTimestamp') ]
                #bb_json[commit.get("id")].extend([message, commit["author"]["displayName"].lower(), commit['author']['emailAddress'], commit['authorTimestamp'] ])
        bitbucket.set_default_branch(proj_key, repo.get("name"), 'master')


# print("\n","Bitbucket Logs")
pprint(bb_json)



# #####*****Gitlab--Code*****#####

gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), os.getenv("GITLAB_TOKEN"))  #Added
gl.auth()
gl_logs = {}

projects = gl.projects.list()
for project in projects:
    # print(project.name)

    branches= project.branches.list()
    for branch in branches:
        commits = project.commits.list(ref_name=branch.name)
        # print(commits)
        for commit in commits:
            commit = commit.__dict__["_attrs"]
            message = commit["message"].replace("\n", "")
            if "+00:00" in commit['committed_date']:
                gitlab_utc = datetime.strptime(commit['committed_date'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
            else:
                gitlab_utc = datetime.strptime(commit['committed_date'], '%Y-%m-%dT%H:%M:%S.%f+05:30')
            gitlab_timestamp = int(datetime.timestamp(gitlab_utc)*1000)
            # if "/" in commit["message"]:
            #     message = commit["message"].split("/")[1].split("\n")[0]
            gl_logs[commit["id"]] = [message, commit["author_name"].lower(), commit['committer_email'],gitlab_timestamp]

print("\n","Gitlab Logs")
pprint(gl_logs)

# #####*****Gitlab--Code*****#####


if gl_logs == bb_json:
    print("All the data is same on both server")
else:
    print("Data is not same on both server")
    print("Showing the difference")

    diff = deepdiff.DeepDiff(gl_logs, bb_json)


    print("\n \n")
    print("\n \n")
    print(diff, "This is not available")
