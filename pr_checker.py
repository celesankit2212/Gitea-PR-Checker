import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from lxml import html

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

# put range of PRs
for i in range(202, 242):
    res = requests.get('https://gitea-working.testrail-staging.com/Gurock/automation-testrail/pulls/'+str(i),
                       auth=HTTPBasicAuth('<your username>', '<your password>'), headers=HEADERS)
    if res.status_code != 200:
        print("The status code is ", res.status_code)
    soup_data = BeautifulSoup(res.text, 'html.parser')
    title_text = soup_data.title
    print("Working on Title : " + str(title_text).replace('<title>', '').replace('</title>', '') + "\n")
    tree = html.fromstring(res.content)
    try:
        pr_raised_by = tree.xpath("//span[@id='pull-desc']/a/text()")[0]
        print(f"Current PR#{i} raised by : " + str(pr_raised_by) + "\n")
        try:
            branch_update = tree.xpath("//button[@data-do='update']/span/text()")[0]
            print(f"PR# {i} needs to be updated as received '"+str(branch_update)+"' from PR")
        except Exception as error:
            print(f"As Error {error} Received no PR update for PR# :".replace(
                'As Error list index out of range ', '') + str(i) + "\nmeans no update branch required\n")
            try:
                assignee = tree.xpath(
                    "//div[@class='review-item' and .//span[contains(@class,'yellow')]]/div/span/a/text()")[0]
                time_opened = tree.xpath(
                    "//div[@class='review-item' and .//span[contains(@class,'yellow')]]/div/span/span/text()")[0]

                print("PR in review with : " + str(assignee) + "\nfrom : " + str(time_opened))
            except Exception as error:
                print(f"Error {error} Received other request for PR# : ".replace(
                    'Error list index out of range ', '') + str(i) + "\nmeans PR not in review")
    except IndexError:
        print("PR seems to be closed or merged")

    print("\n\n-------------------------------------------------------")
    continue
