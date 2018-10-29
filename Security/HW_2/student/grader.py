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
    if level != 'low':
        print("FAIL SQL VERIFY")
    answer = [['admin', '7en8aiDoh!'], ['dricci', '12345'], ['amason', 'gandalf']]
    for ind, item in enumerate(user_pass_list):
        if item[0] != answer[ind][0] or item[1] != answer[ind][1]:
            print("FAIL SQL VERIFY")
            return
    print("PASS SQL VERIFY")

def command_injection_verify(level, flag):
    if level == 'low':
        if flag == 'Come with me if you want to live':
            print("Command Injection Low: PASS")
        else:
            print("Command Injection Low: FAIL -- " + flag )

    if level == 'medium':
        if flag == "Looks like you'll live":
            print("Command Injection Medium: PASS")
        else:
            print("Command Injection Medium: FAIL -- " + flag)

    if level == 'high':
        if flag == "You are invincible!":
            print("Command Injection High: PASS")
        else:
            print("Command Injection Medium: FAIL -- " + flag)


def csrf_verify(level, secret_msg, comments):
    pass
