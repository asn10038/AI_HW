"""
NOTE: Grader code will go here. Any modifications here will not be submitted.
"""
def xss_verify(vuln_type, password):
    if vuln_type == 'reflected_low' and password == "Me want cookie!":
        print("XSS Reflected Low: PASS password is -- " + str(password))
    elif vuln_type == 'reflected_low' and password != "Me want cookie!":
        print("XSS Reflected Low: FAILED password is -- " + str(password))

    if vuln_type == 'reflected_medium' and password == "Me want cookie!":
        print("XSS Reflected medium: PASS password is -- " + str(password))
    elif vuln_type == 'reflected_medium' and password != "Me want cookie!":
        print("XSS Reflected medium: FAILED password is -- " + str(password))

    if vuln_type == 'reflected_high' and password == "Me want cookie!":
        print("XSS Reflected high: PASS password is -- " + str(password))
    elif vuln_type == 'reflected_high' and password != "Me want cookie!":
        print("XSS Reflected high: FAILED password is -- " + str(password))

    if vuln_type == 'stored_low' and password == "Me eat cookie!":
        print("XSS Stored low: PASS password is -- " + str(password))
    elif vuln_type == 'stored_low' and password != "Me eat cookie!":
        print("XSS Stored low: FAILED password is -- " + str(password))

    if vuln_type == 'stored_medium' and password == "Me eat cookie!":
        print("XSS Stored Medium: PASS password is -- " + str(password))
    elif vuln_type == 'stored_medium' and password != "Me eat cookie!":
        print("XSS Stored Medium: FAILED password is -- " + str(password))

    if vuln_type == 'stored_high' and password == "Me eat cookie!":
        print("XSS Stored High: PASS password is -- " + str(password))
    elif vuln_type == 'stored_high' and password != "Me eat cookie!":
        print("XSS Stored High: FAILED password is -- " + str(password))

    if vuln_type == 'DOM_low' and password == "Om nom nom nom!":
        print("XSS DOM Low: PASS password is -- " + str(password))
    elif vuln_type == 'DOM_low' and password != "Om nom nom nom!":
        print("XSS DOM Low: FAILED password is -- " + str(password))

    if vuln_type == 'DOM_medium' and password == "Om nom nom nom!":
        print("XSS DOM Medium: PASS password is -- " + str(password))
    elif vuln_type == 'DOM_medium' and password != "Om nom nom nom!":
        print("XSS DOM Medium: FAILED password is -- " + str(password))

    if vuln_type == 'DOM_high' and password == "Om nom nom nom!":
        print("XSS DOM High: PASS password is -- " + str(password))
    elif vuln_type == 'DOM_high' and password != "Om nom nom nom!":
        print("XSS DOM High: FAILED password is -- " + str(password))

    return

def sql_verify(level, user_pass_list):
    pass

def command_injection_verify(level, flag):
    pass

def csrf_verify(level, secret_msg, comments):
    pass