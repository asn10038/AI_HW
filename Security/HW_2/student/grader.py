"""
NOTE: Grader code will go here. Any modifications here will not be submitted.
"""
def xss_verify(vuln_type, password):
    if vuln_type == 'reflected':
        if password == "Me want cookie!":
            print("XSS Reflected Low: PASS password is -- " + str(password))
        else:
            print("XSS Reflected Low: FAILED password is -- " + str(password))
    return

def sql_verify(level, user_pass_list):
    pass

def command_injection_verify(level, flag):
    pass

def csrf_verify(level, secret_msg, comments):
    pass
