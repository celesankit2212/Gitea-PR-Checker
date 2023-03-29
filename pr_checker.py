import turtle
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from lxml import html
import pandas as pd
import openpyxl
import random
from turtle import textinput


headers = requests.utils.default_headers()

headers.update(
    {
        'User-Agent': f'My User Agent {random.randint(5, 20)}.0',
    }
)

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
title = []
pr_urls = []
current_pr_status = []
pr_raiser = []
branch_update_request = []
reviewer = []
raised_review_from = []
having_conflicts = []
collaborators = ['AnkitM', 'Preetipt', 'SagarSatishSonwalkar', 'RameshR', 'ArchanaMurthy']
pr_merge_ankit = pr_merge_preeti = pr_merge_ramesh = pr_merge_archana = pr_merge_sagar = 0
pr_open_ankit = pr_open_preeti = pr_open_ramesh = pr_open_archana = pr_open_sagar = 0
username = textinput("Username", "Please provide your Gitea username !!")
password = textinput("Password", "Please provide your Gitea password !!")
last_pr = textinput("Last PR Number Raised", "Please provide last PR number raised")
required_values = {'username': str(username), 'password': str(password), 'last_pr': last_pr}
tr = turtle.Turtle()
wn = turtle.Screen()
wn.addshape('report_processing.gif')
tr.shape('report_processing.gif')
# put range of PRs
for pr_number in range(202, int(required_values.get('last_pr'))):
    res = requests.get('https://gitea-working.testrail-staging.com/Gurock/automation-testrail/pulls/'+str(pr_number),
                       auth=HTTPBasicAuth(
                           required_values.get('username'),
                           required_values.get('password')), headers=headers)
    if res.status_code != 200:
        print("The status code is ", res.status_code)
    url = res.url
    soup_data = BeautifulSoup(res.text, 'html.parser')
    title_text = soup_data.title
    tree = html.fromstring(res.content)
    celestial_pr = tree.xpath("//code[2]/a/text()")[0]
    pr_status = tree.xpath("//div[contains(@class,'title')]/div[contains(@class, 'large label')]/text()")[0]
    if 'Celestial_New_Automation_Enhancement' in celestial_pr and 'Closed' not in pr_status:
        print("Working on Title : PR" + str(title_text).replace('<title>', '').replace('</title>', '').replace(
            '-  automation-testrail - Gitea: Git with a cup of tea', '') + "\n")
        title.append("PR" + str(title_text).replace('<title>', '').replace('</title>', '').replace(
            '-  automation-testrail - Gitea: Git with a cup of tea', ''))
        pr_urls.append(url)
        current_pr_status.append(pr_status)
        print("Status of PR#" + str(pr_number) + " is : " + str(pr_status))
        try:
            pr_raised_by = tree.xpath("//span[@id='pull-desc']/a/text()")[0]
            pr_raiser.append(pr_raised_by)
            print(f"Current PR#{pr_number} raised by : " + str(pr_raised_by) + "\n")
            if 'AnkitM' in pr_raised_by:
                pr_open_ankit = pr_open_ankit + 1
            elif 'Preetipt' in pr_raised_by:
                pr_open_preeti = pr_open_preeti + 1
            elif 'SagarSatishSonwalkar' in pr_raised_by:
                pr_open_sagar = pr_open_sagar + 1
            elif 'RameshR' in pr_raised_by:
                pr_open_ramesh = pr_open_ramesh + 1
            elif 'ArchanaMurthy' in pr_raised_by:
                pr_open_archana = pr_open_archana + 1
            try:
                branch_update = tree.xpath("//button[@data-do='update']/span/text()")[0]
                branch_update_request.append("True")
                having_conflicts.append("NA")
                reviewer.append("NA")
                raised_review_from.append("NA")
                print(f"PR# {pr_number} needs to be updated as received '"+str(
                    branch_update).replace('\t', '').replace('\n', '')+"' from PR")
            except Exception as error:
                branch_update_request.append("False")
                print(f"As Error {error} Received no PR update for PR# :".replace(
                    'As Error list index out of range ', '') + str(pr_number) + "\nmeans no update branch required\n")
                try:
                    conflict = tree.xpath("//div[contains(@class,'merge-section')]/div/text()")[1].replace(
                        '\t', '').replace('\n', '')
                    if 'conflicting' in conflict:
                        print(f"PR# {pr_number} needs to checked with conflicts as received '" + str(
                            conflict) + "' from PR")
                        having_conflicts.append("True")
                        reviewer.append("NA")
                        raised_review_from.append("NA")
                    else:
                        having_conflicts.append("False")
                        print(f"PR# {pr_number} having No conflicts as received '" + str(conflict) + "' from PR")
                        try:
                            assignee = tree.xpath(
                                "//div[@class='review-item' and .//span[contains(@class,'yellow')]]/div/span/a/text()")[0]
                            time_opened = tree.xpath(
                                "//div[@class='review-item' and .//span[contains(@class,'yellow')]]/div/span/span/text()")[
                                0]
                            reviewer.append(assignee)
                            raised_review_from.append(time_opened)
                            print("PR in review with : " + str(assignee) + "\nfrom : " + str(time_opened))
                        except Exception as error:
                            reviewer.append("NA")
                            raised_review_from.append("NA")
                            print(f"Error {error} Received other request for PR# : ".replace(
                                'Error list index out of range ', '') + str(pr_number) + "\nmeans PR not in review")
                except IndexError:
                    having_conflicts.append("False")
                    try:
                        assignee = tree.xpath(
                            "//div[@class='review-item' and .//span[contains(@class,'yellow')]]/div/span/a/text()")[0]
                        time_opened = tree.xpath(
                            "//div[@class='review-item' and .//span[contains(@class,'yellow')]]/div/span/span/text()")[0]
                        if 'julia' in assignee:
                            assignee = assignee + " (External Review)"
                        else:
                            assignee = assignee + " (Internal Review)"
                        reviewer.append(assignee)
                        raised_review_from.append(time_opened)
                        print("PR in review with : " + str(assignee) + "\nfrom : " + str(time_opened))
                    except Exception as error:
                        reviewer.append("NA")
                        raised_review_from.append("NA")
                        print(f"Error {error} Received other request for PR# : ".replace(
                            'Error list index out of range ', '') + str(pr_number) + "\nmeans PR not in review")
        except IndexError:
            try:
                pr_by = tree.xpath("//div[contains(@class, 'comment first')]//div[contains(@class, 'comment-header')]/div[./div[contains(.,'Collaborator') or contains(.,'Owner')]]/preceding-sibling::div//a[@class='author']/text()")[0]
                effort_type = tree.xpath("//div[contains(@class, 'comment first')]//div[contains(@class, 'comment-header')]/div[./div[contains(.,'Collaborator') or contains(.,'Owner')]]/div[1]/text()")[0].replace('\t', '').replace('\n', '')
                if 'Merged' in pr_status:
                    pr_raiser.append(str(effort_type) + " - " + str(pr_by))
                    if 'AnkitM' in pr_by:
                        pr_merge_ankit = pr_merge_ankit + 1
                    elif 'Preetipt' in pr_by:
                        pr_merge_preeti = pr_merge_preeti + 1
                    elif 'SagarSatishSonwalkar' in pr_by:
                        pr_merge_sagar = pr_merge_sagar + 1
                    elif 'RameshR' in pr_by:
                        pr_merge_ramesh = pr_merge_ramesh + 1
                    elif 'ArchanaMurthy' in pr_by:
                        pr_merge_archana = pr_merge_archana + 1
                else:
                    pr_raiser.append("NA")
            except IndexError:
                pr_raiser.append("NA")
            branch_update_request.append("NA")
            having_conflicts.append("NA")
            reviewer.append("NA")
            raised_review_from.append("NA")
            print("PR seems to be closed or merged")

        print("\n\n-------------------------------------------------------")
    else:
        continue

# dictionary of lists
dictionary_frame = {'Title': title, 'PR_Links': pr_urls, 'Current PR Status': current_pr_status, 'Raised By': pr_raiser,
                    'Branch Update Required': branch_update_request, 'Having Conflicts': having_conflicts,
                    'Reviewer': reviewer, 'Raised to Reviewer from': raised_review_from}

collaborators_frame = {'Collaborator': collaborators,
                       'Open PRs': [pr_open_ankit, pr_open_preeti, pr_open_sagar, pr_open_ramesh, pr_open_archana],
                       'Merged PRs': [pr_merge_ankit, pr_merge_preeti, pr_merge_sagar, pr_merge_ramesh, pr_merge_archana],
                       'Total PRs': [pr_open_ankit + pr_merge_ankit,
                                     pr_open_preeti + pr_merge_preeti,
                                     pr_open_sagar + pr_merge_sagar,
                                     pr_open_ramesh + pr_merge_ramesh,
                                     pr_open_archana + pr_merge_archana]}

dataframe = pd.DataFrame(dictionary_frame)
dataframe_collab = pd.DataFrame(collaborators_frame)
# saving the dataframe
dataframe.to_csv('Report_New.csv', index=False)
dataframe_collab.to_csv('Report_Collab.csv', index=False)
dataframe.to_excel('Report_Check.xlsx', sheet_name='Current PR Status', index=False)
dataframe_collab.to_excel('Report_Collab.xlsx', sheet_name='Collaborators Status', index=False)

with pd.ExcelWriter('Report_Final.xlsx') as writer:
    dataframe.to_excel(writer, sheet_name='Current PR Status', index=False)
    dataframe_collab.to_excel(writer, sheet_name='Collaborators Status', index=False)
