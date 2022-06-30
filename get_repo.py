import pandas as pd


def get_groups():
    data = pd.read_csv('repos_bb.csv', sep='\t')
    project_name = list(data['Project Name'])
    repo_link = list(data['Bitbucket Clone URL'])
    return dict(zip(project_name, repo_link))

