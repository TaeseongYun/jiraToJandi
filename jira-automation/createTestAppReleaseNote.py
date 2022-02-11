from jira import JIRA
import sys
import os
import json

import auth as user
import requests

### 해결된 버전 정보
appVersion = sys.argv[1]
changeVersion = sys.argv[2]

if len(sys.argv) > 3:
    print("Insufficient arguments")
    sys.exit()

auth = user.getJiraAuthInfomation()
jandi_web_hook_url = auth[user.JANDI_WEB_HOOK_URL]

### JQL 수행, 해결된 버전이 입력값과 같은 모든 JIRA 이슈 가져오기
jira = JIRA(server=auth[user.JIRA_SERVER], basic_auth=(auth[user.JIRA_ID], auth[user.JIRA_TOKEN]))
jql = "resolution = Unresolved AND cf[10821] = '" + changeVersion + "' order by updated" # ex) "project is not EMPTY"
issues = jira.search_issues(jql, maxResults=10000)

### JIRA 이슈 검색결과 키 값 리스트로 구성
changedKey = []
updateDescriptions = []

for i in issues:
    issue = jira.issue(i, fields='summary')
    changedKey.append(issue.key)
    title = "-" + issue.fields.summary + " 해결하였습니다"
    title = title.replace("[And]", "").replace("And/", "").replace("[AND]", "").replace("AND/", "").replace("And_", "").replace("AND_", "")
    updateDescriptions.append(title)

### 템플릿에 맞게 인자 대입
templateFile = open(os.getcwd()+'/jira-automation/template/testApp-release-template.md', 'r', encoding='utf-8')
template = templateFile.read()
template = template.replace("%(APPVERSION)", appVersion)
template = template.replace("%(VERSION)", changeVersion)
template = template.replace("%(ISSUES)","[" +  ", ".join(changedKey) + "]")
template = template.replace("%(DESCRIPTION)", "\n".join(updateDescriptions))

### 릴리즈 노트 잔디로 전송
headers = {'Accept' : 'application/vnd.tosslab.jandi-v2+json', 'Content-Type' : 'application/json'}


releaseNoteContent = {
"body" : "새로운 릴리즈 노트가 생성되었습니다.",
"connectColor" : "#FFED49",
"connectInfo" : [{
"title" : changeVersion + " 릴리즈 노트",
"description" : template
}]
}

releaseNote = json.dumps(releaseNoteContent)

response = requests.post(jandi_web_hook_url, headers=headers, data=releaseNote)
print(response.status_code)
