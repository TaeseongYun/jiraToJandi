import csv
import os

JIRA_SERVER = 0
JIRA_ID = 1
JIRA_TOKEN = 2
JANDI_WEB_HOOK_URL = 3

def getJiraAuthInfomation():
    f = open(os.getcwd()+'/jira-automation/auth.csv', 'r', encoding='utf-8')
    auths = csv.reader(f)
    auth = []
    for row in auths:
        auth.append(row)
    
    jiraServer = auth[JIRA_SERVER][0]
    username = auth[JIRA_ID][0]
    token = auth[JIRA_TOKEN][0]
    jandiWEBHookUrl = auth[JANDI_WEB_HOOK_URL][0]
    return (jiraServer, username, token, jandiWEBHookUrl)
