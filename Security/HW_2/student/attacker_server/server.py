"""You are welcome to use any part of the Python Standard Library in addition to Flask."""
from flask import Flask, render_template, abort, request, make_response
import base64
from http.cookies import SimpleCookie
import sys
sys.path.append("..")
import grader

app = Flask(__name__)

@app.route('/xss/<vuln_type>')
def steal_cookie(vuln_type):
    """
    Use this to exfiltrate a stolen cookie from the vulnerable server.
    """
    received_cookie = request.args.get('cookie', default='') # Reads the `cookie` parameter

    # grader.xss_verify(vuln_type, password) # Remember to decode the password.

    return password

# NOTE: You are free to add additional routes/endpoints to the attacker server to mount any attack of your choosing.
if __name__ == '__main__':
    app.run(port=1338)
