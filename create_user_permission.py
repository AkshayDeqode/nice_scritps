from math import perm
import gitlab
from atlassian import Bitbucket
from dotenv import load_dotenv
import os
from gitlab.const import MAINTAINER_ACCESS, DEVELOPER_ACCESS, GUEST_ACCESS
from gitlab.exceptions import GitlabCreateError


load_dotenv()

roles = {
    "PROJECT_ADMIN": MAINTAINER_ACCESS,
    "PROJECT_WRITE": DEVELOPER_ACCESS,
    "PROJECT_READ": GUEST_ACCESS
}

project_repo={}

bitbucket = Bitbucket(
    url=os.getenv("BITBUCKET_URL"),
    username=os.getenv("BITBUCKET_USERNAME"),
    password=os.getenv("BITBUCKET_PASSWORD")
)

emails = {}

projects = bitbucket.project_list()
for project in projects:
    project_key = project['key']
    repository=bitbucket.repo_list(project_key)
    for repo in repository:
        repo_name=repo['name']
    permisions= bitbucket.project_users(project_key, limit=99999, filter_str=None)
    for permision in permisions:
        emails[permision['user']['emailAddress']] = None
        project_repo[repo_name] = project_repo.get(repo_name, {})
        project_repo[repo_name].update({permision['user']['emailAddress']: permision['permission']})


gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), os.getenv("GITLAB_TOKEN"))  #Added
gl.auth()

users = gl.users.list()
for user in users:
    if user.email in emails:
        emails[user.email] = user.id

for project, users in project_repo.items():
    gl_projects = gl.projects.list()
    for gl_project in gl_projects:
        if gl_project.attributes["name"] == project:
            for user, permision in users.items():
                try:
                    member = gl_project.members.create({'user_id': emails[user], 'access_level': roles[permision]})
                except GitlabCreateError:
                    member = gl_project.members.get(emails[user]) 
                    member.access_level = roles[permision]
                    member.save()
                    print("Access Updated")
                except Exception as e:
                    print(str(e))
                    break