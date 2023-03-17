import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from lxml import html
import pandas as pd
import openpyxl

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
title = []
pr_raiser = []
branch_update_request = []
reviewer = []
raised_review_from = []
# put range of PRs
for i in range(202, 242):
    res = requests.get('https://gitea-working.testrail-staging.com/Gurock/automation-testrail/pulls/'+str(i),
                       auth=HTTPBasicAuth('<your username>', '<your password>'), headers=HEADERS)
    if res.status_code != 200:
        print("The status code is ", res.status_code)
    soup_data = BeautifulSoup(res.text, 'html.parser')
    title_text = soup_data.title
    print("Working on Title : PR" + str(title_text).replace('<title>', '').replace('</title>', '').replace(
        '-  automation-testrail - Gitea: Git with a cup of tea', '') + "\n")
    title.append("PR" + str(title_text).replace('<title>', '').replace('</title>', '').replace(
        '-  automation-testrail - Gitea: Git with a cup of tea', ''))
    tree = html.fromstring(res.content)
    try:
        pr_raised_by = tree.xpath("//span[@id='pull-desc']/a/text()")[0]
        pr_raiser.append(pr_raised_by)
        print(f"Current PR#{i} raised by : " + str(pr_raised_by) + "\n")
        try:
            branch_update = tree.xpath("//button[@data-do='update']/span/text()")[0]
            branch_update_request.append("True")
            reviewer.append("NA")
            raised_review_from.append("NA")
            print(f"PR# {i} needs to be updated as received '"+str(branch_update)+"' from PR")
        except Exception as error:
            branch_update_request.append("False")
            print(f"As Error {error} Received no PR update for PR# :".replace(
                'As Error list index out of range ', '') + str(i) + "\nmeans no update branch required\n")
            try:
                assignee = tree.xpath(
                    "//div[@class='review-item' and .//span[contains(@class,'yellow')]]/div/span/a/text()")[0]
                time_opened = tree.xpath(
                    "//div[@class='review-item' and .//span[contains(@class,'yellow')]]/div/span/span/text()")[0]
                reviewer.append(assignee)
                raised_review_from.append(time_opened)
                print("PR in review with : " + str(assignee) + "\nfrom : " + str(time_opened))
            except Exception as error:
                reviewer.append("NA")
                raised_review_from.append("NA")
                print(f"Error {error} Received other request for PR# : ".replace(
                    'Error list index out of range ', '') + str(i) + "\nmeans PR not in review")
    except IndexError:
        pr_raiser.append("NA")
        branch_update_request.append("NA")
        reviewer.append("NA")
        raised_review_from.append("NA")
        print("PR seems to be closed or merged")

    print("\n\n-------------------------------------------------------")
    continue

# dictionary of lists
dictionary_frame = {'Title': title, 'Raised By': pr_raiser, 'Branch Update Required': branch_update_request,
                    'Reviewer': reviewer, 'Raised to Reviewer from': raised_review_from}

dataframe = pd.DataFrame(dictionary_frame)

# saving the dataframe
dataframe.to_csv('Report.csv', index=False)
dataframe.to_excel('Report.xlsx', sheet_name='Current PR Status', index=False)
