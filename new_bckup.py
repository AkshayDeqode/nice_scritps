from optparse import Values
from traceback import print_tb
import gitlab
from atlassian import Bitbucket
from pprint import pprint
import numpy as np
import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import get_repo
import time
load_dotenv()

bitbucket = Bitbucket(
    url=os.getenv("BITBUCKET_URL"),
    username=os.getenv("BITBUCKET_USERNAME"),
    password=os.getenv("BITBUCKET_PASSWORD"),
)

bb_logs = {}
projects = bitbucket.project_list()

gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), os.getenv("GITLAB_TOKEN"))
gl.auth()
gl_logs = {}


bitbucket_proj = bitbucket.project(os.getenv("GITLAB_PROJECT"))

b_repo = bitbucket.repo_list(bitbucket_proj["key"])

bb_branches = bitbucket.get_branches(bitbucket_proj['key'], os.getenv("GITLAB_PROJECT_REPO"), details=False)


def find_repositories():
    found_repos = list()
    not_found_repos = list()
    repos = get_repo.get_groups()
    for repo_name, repo_link  in repos.items():
        if repo_link is np.nan:
            print(f"Error: repo link not found: {repo_name}")
            not_found_repos.append(repo_name)
        else:
            start_string = '/repos/'
            end_string = '/browse'

            start_index = repo_link.find(start_string) + len(start_string)
            end_index = repo_link.find(end_string)

            # print(repo_name, repo_link[start_index:end_index])
            try:
                gl_repos_probable_urls = [x.attributes['web_url'].rsplit('/', 1)[-1].lower() for x in gl.projects.list(max_retries=-1, search=repo_link[start_index:end_index], all = True)]
                if repo_link[start_index:end_index] in gl_repos_probable_urls:
                    found_repos.append(repo_name)
                else:
                    not_found_repos.append(repo_name)
                    # if gl_repo.attributes['name'].lower() == repo_name.lower():
                    #     found_repos.append(gl_repo.attributes['id'])
                
            except:
                print(f"no repo exist for Repository: {repo_name}")
            

    # Creating two files to document the found repositories and 404 repositories
    with open('found_repos.txt','w') as f:
        for item in found_repos:
            f.write("%s\n" % item)

    with open('not_found_repos.txt','w') as f:
        for item in not_found_repos:
            f.write("%s\n" % item)

find_repositories()


# try:
#     gl_repo = gl.projects.list(max_retries=-1, search=os.getenv("GITLAB_PROJECT_REPO"))[0]
# except:
#     print("no repo exist")

# branch_report = {"project": [],"repository": [], "status":[]}
# for branch in bb_branches:
#     bb_dict = {}
#     gl_dict = {}
#     try:
#         gl_branch = gl_repo.branches.get(branch.get("displayId"), obey_rate_limit=False)
#     except:
#         print("no branch exist:", branch.get("displayId"))
#         branch_report["status"].append("fail")
#         branch_report["project"].append(os.getenv("GITLAB_PROJECT"))
#         branch_report["repository"].append(os.getenv("GITLAB_PROJECT_REPO"))       
#         continue

#     bb_commits = bitbucket.get_commits(bitbucket_proj["key"],os.getenv("GITLAB_PROJECT_REPO"),hash_newest=branch.get("latestCommit"),limit=99999)
#     for data in bb_commits:
#         try:
#             bb_commit_id = data["id"]
#             bb_message = data["message"].replace("\n", "")
#             bb_author = data.get("author").get("displayName")
#             bb_email = data.get("author").get("emailAddress")
#             bb_dict[bb_commit_id] = [bb_message,bb_author,bb_email]
#         except Exception as e:
#             print(e, "bb")

#     gl_branch_commits= gl_repo.commits.list(obey_rate_limit=False, all=True,max_retries=-1, query_parameters={"ref_name": gl_branch.name, "all": True})
#     for g_commit in gl_branch_commits:
#         try:
#             gl_commit_id = g_commit.id
#             gl_message = g_commit.message.replace("\n", "").lower()
#             gl_author = g_commit.author_name.lower()
#             gl_email = g_commit.committer_email
#             gl_dict[gl_commit_id] = [gl_message, gl_author,gl_email]
#         except Exception as e:
#             print(e, "gg")

#     is_branch_failed = False
#     report = {"branch": [], "status":[]}
#     for key in bb_dict:
#         if key not in gl_dict:
#             report["status"].append("fail")
#             report["branch"].append(gl_branch.name)
#             is_branch_failed = True
#             break
    
#     if not is_branch_failed:
#         report["status"].append("success")
#         report["branch"].append(gl_branch.name)


#     report = pd.DataFrame(report)

#     if not os.path.exists('/home/ec2-user/cs-migration-setup/final_scripts/'+str(os.getenv("GITLAB_PROJECT"))):
#         os.mkdir('/home/ec2-user/cs-migration-setup/final_scripts/'+str(os.getenv("GITLAB_PROJECT")))
#         os.chdir("/home/ec2-user/cs-migration-setup/final_scripts/"+str(os.getenv("GITLAB_PROJECT")))
#         if os.path.exists("/home/ec2-user/cs-migration-setup/final_scripts/"+str(os.getenv("GITLAB_PROJECT"))+str("/commit_status.")+str(os.getenv("GITLAB_PROJECT"))+str(".")+str(os.getenv("GITLAB_PROJECT_REPO"))+".csv"):
#             report.to_csv("/home/ec2-user/cs-migration-setup/final_scripts/"+str(os.getenv("GITLAB_PROJECT"))+str("/commit_status.")+str(os.getenv("GITLAB_PROJECT"))+str(".")+str(os.getenv("GITLAB_PROJECT_REPO"))+".csv", mode="a", header=False, index=False)
#         else:
#             report.to_csv("/home/ec2-user/cs-migration-setup/final_scripts/"+str(os.getenv("GITLAB_PROJECT"))+str("/commit_status.")+str(os.getenv("GITLAB_PROJECT"))+str(".")+str(os.getenv("GITLAB_PROJECT_REPO"))+".csv", index=False)
#     else:
#         os.chdir("/home/ec2-user/cs-migration-setup/final_scripts/"+str(os.getenv("GITLAB_PROJECT")))
#         if os.path.exists("/home/ec2-user/cs-migration-setup/final_scripts/"+str(os.getenv("GITLAB_PROJECT"))+str("/commit_status.")+str(os.getenv("GITLAB_PROJECT"))+str(".")+str(os.getenv("GITLAB_PROJECT_REPO"))+".csv"):
#             report.to_csv("/home/ec2-user/cs-migration-setup/final_scripts/"+str(os.getenv("GITLAB_PROJECT"))+str("/commit_status.")+str(os.getenv("GITLAB_PROJECT"))+str(".")+str(os.getenv("GITLAB_PROJECT_REPO"))+".csv", mode="a", header=False, index=False)
#         else:
#             report.to_csv("/home/ec2-user/cs-migration-setup/final_scripts/"+str(os.getenv("GITLAB_PROJECT"))+str("/commit_status.")+str(os.getenv("GITLAB_PROJECT"))+str(".")+str(os.getenv("GITLAB_PROJECT_REPO"))+".csv", index=False)