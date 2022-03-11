from encodings import utf_8
import requests
from requests.auth import HTTPBasicAuth
import json
from atlassian import bamboo
from dotenv import load_dotenv
from pprint import pprint
import os
import ast

load_dotenv()

# import pdb;pdb.set_trace()

bamboo = bamboo.Bamboo(
    url=os.getenv("BAMBOO_URL"),
    username=os.getenv("BAMBOO_USERNAME"),
    password=os.getenv("BAMBOO_PASSWORD")
)



def bamboo_project():
    projects = []
    # projectkey = []
    bamboo_proj=bamboo.projects()
    for proj in bamboo_proj:
        plans= bamboo.project_plans(proj['key'])
        # projectkey.append(plans)
        for plan in plans:
            plan_info = bamboo.get_plan(plan['planKey']['key'])
            project_key = plan_info['projectKey']
            projects.append(project_key)
    return projects

def bamboo_plan():
    project_plan=[]
    bamboo_plan=bamboo.plans()
    for plan in bamboo_plan:
        plan= plan['link']['href'].split("/")[-1]
        project_plan.append(plan)
    return project_plan

        
projects = bamboo_project()
project_plan = bamboo_plan()

# print(projects)
# print(vplan)
projects_dict = {}
for project in projects:
    # project_variable = []
    request =  f"http://localhost:8085/rest/api/latest/project/{project}/variables"
    variables_plan= requests.get(request ,auth= HTTPBasicAuth(os.getenv("BAMBOO_USERNAME"),os.getenv("BAMBOO_PASSWORD")))
    for variables in variables_plan:
        decode=variables.decode('utf-8')
        decoded_list=ast.literal_eval(decode)
        if not decoded_list:
            print("No variable in project: {}".format(project))
        for values in decoded_list:
            projects_dict[project] = projects_dict.get(project, {})
            projects_dict[project].update({values['name']:values['value']})
print(projects_dict)

plan_dict = {}
# import pdb;pdb.set_trace()
for plan in project_plan:
    # plan_values=[]
    request =  f"http://localhost:8085/rest/api/latest/plan/{plan}/variables"
    variables_plan= requests.get(request ,auth= HTTPBasicAuth(os.getenv("BAMBOO_USERNAME"),os.getenv("BAMBOO_PASSWORD")))
    for variables in variables_plan:
        decode_value =variables.decode('utf-8')
        decoded_list=ast.literal_eval(decode_value)
        if not decoded_list:
            print("No variable in project plan: {}".format(plan))
        for values in decoded_list:
            plan_dict[plan] = plan_dict.get(plan, {})
            plan_dict[plan].update({values['name']:values['value']})
    # pprint(plan_values)
print(plan_dict)

def bamboo_users():
    bamboo_u = []
    request = "http://localhost:8085/rest/api/latest/permissions/global/available-users?ignore"
    users= requests.get(request, auth=HTTPBasicAuth(os.getestagesnv("BAMBOO_USERNAME"),os.getenv("BAMBOO_PASSWORD")))
    for i in json.loads(users.text)["results"]: 
        bamboo_u.append(i)
    return bamboo_u
ava_users = bamboo_users()
pprint(ava_users)



def bamboo_g():
    bamboo_group= bamboo.get_groups()
    group_details=[]
    group_name=bamboo_group['results']
    for gname in group_name:
        names=gname['name']
        user_from_group = bamboo.get_users_from_group(names)
        results= user_from_group['results']
        for name in results:
            group_details.append({names: {"name": name['name'],"fullName": name['fullName'], "email": name['email']}})
        

    return group_details
a= bamboo_g()
pprint(a)


for plan in project_plan:
    yaml_data=[]
    for project in projects:
        request =  f"http://localhost:8085/rest/api/latest/plan/{plan}/specs?format=YAML"
        variables_plan= requests.get(request ,auth= HTTPBasicAuth(os.getenv("BAMBOO_USERNAME"),os.getenv("BAMBOO_PASSWORD")))
        f =  open("{}.yaml".format(plan), "wb")
        for job_details in variables_plan:
            f.write(job_details)
