import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from lxml import html

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

# put range of PRs
for i in range(202, 238):
    res = requests.get('https://gitea-working.testrail-staging.com/Gurock/automation-testrail/pulls/'+str(i),
                       auth=HTTPBasicAuth('AnkitM', 'Ai987$%tM'), headers=HEADERS)
    print("The status code is ", res.status_code)
    soup_data = BeautifulSoup(res.text, 'html.parser')
    print(soup_data.title)
    tree = html.fromstring(res.content)
    try:
        assignee = tree.xpath("//div[@class='ui assignees list']//span[contains(@class,'yellow')]/../a/text()")[-1]
        try:
            branch_update = tree.xpath("//button[@data-do='update']")
            print(f"PR# {i} needs to be updated")
        except Exception as error:
            print(f"As Error {error} Received for PR# : " + str(i) + "means no update branch required")
        print("PR in review with : "+str(assignee).replace('\t', '').replace('\n', ''))
    except Exception as error:
        print(f"Error {error} Received for PR# regarding assignee: " + str(i))
    print("\n\n-------------------------------------------------------")
    continue
