from traceback import print_tb
import gitlab
from atlassian import Bitbucket
from dotenv import load_dotenv
from numpy import diff
import pandas as pd
import os


load_dotenv()

bitbucket = Bitbucket(
    url=os.getenv("BITBUCKET_URL"),
    username=os.getenv("BITBUCKET_USERNAME"),
    password=os.getenv("BITBUCKET_PASSWORD")
)

bb_tags={}

bb_projects = bitbucket.project_list()

for project in bb_projects:
    repositories = bitbucket.repo_list(project["key"])
    for repo in repositories:
        tags=bitbucket.get_tags(project['key'], repository_slug= repo['slug'])
        for tag in tags:
            bb_tags[repo['slug']] = bb_tags.get(repo['slug'], [])
            bb_tags[repo['slug']].append(tag['displayId'])


gl_tags={}

gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), os.getenv("GITLAB_TOKEN"))
gl.auth()

gg_projects = gl.projects.list()
for g_project in gg_projects:
    tags = g_project.tags.list()
    for tag in tags:
        gl_tags[g_project.name] = gl_tags.get(g_project.name, [])
        gl_tags[g_project.name].append(tag.name)

# print(gl_tags)
bb_difference_dict = {}
gl_difference_dict = {}

for repo, bb_tags_list in bb_tags.items():
    gl_tags_list = gl_tags.get(repo, [])

    gl_difference = list(set(bb_tags_list) - set(gl_tags_list))
    bb_difference = list(set(gl_tags_list) - set(bb_tags_list))

    if bb_difference:
        bb_difference_dict[repo] = bb_difference
    if gl_difference:
        gl_difference_dict[repo] = gl_difference

print("Not present of BB ", bb_difference_dict)
print("Not present on GL ", gl_difference_dict)


