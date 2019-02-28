#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from builtins import str
from builtins import bytes
from builtins import object

import requests as rq
import base64
import pprint
import json
import os
import random
import datetime
from datetime import date

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template


# Flask app should start in global layout

app = Flask(__name__)
	
@app.route('/hello')
def hello():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access. 
    req_dict = json.loads(request.data)
    
    parameters = req_dict["result"]["parameters"]
    
    date = parameters["date"][5:10]
    crop = parameters["crop"]

    # constructing the resposne string.
    speech = integrate()
    res = makeWebhookResult(speech)
    return res

#AWHERE
class AWhereAPI(object):
    def __init__(self):
        """
        Initializes the AWhereAPI class, which is used to perform HTTP requests 
        to the aWhere V2 API.
        elf.        Docs:
            http://developer.awhere.com/api/reference
        """
        
        self.THIS_DT = '02-27'
        self.api_key = 'r4AGIfSxMlQNkUPxQGgLx7kpIKovQCMI'
        self.api_secret = 'S9nipeJJ6AVLmRdG'
        self.base_64_encoded_secret_key = self.encode_secret_and_key(
            self.api_key, self.api_secret)
        self.auth_token = self.get_oauth_token(self.base_64_encoded_secret_key)
	
    def encode_secret_and_key(self, key, secret):
        """
        Docs:
            http://developer.awhere.com/api/authentication
        Returns:
            Returns the base64-encoded {key}:{secret} combination, seperated by a colon.
        """
        # Base64 Encode the Secret and Key
        key_secret = '%s:%s' % (key, secret)
        #print('\nKey and Secret before Base64 Encoding: %s' % key_secret)

        encoded_key_secret = base64.b64encode(
            bytes(key_secret, 'utf-8')).decode('ascii')

        #print('Key and Secret after Base64 Encoding: %s' % encoded_key_secret)
        return encoded_key_secret

    def get_oauth_token(self, encoded_key_secret):
        """
        Demonstrates how to make a HTTP POST request to obtain an OAuth Token
        Docs: 
            http://developer.awhere.com/api/authentication
        Returns: 
            The access token provided by the aWhere API
        """
        auth_url = 'https://api.awhere.com/oauth/token'

        auth_headers = {
            "Authorization": "Basic %s" % encoded_key_secret,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = "grant_type=client_credentials"

        response = rq.post(auth_url,
                           headers=auth_headers,
                           data=body)

        # .json method is a requests lib method that decodes the response
        return response.json()['access_token']


    def get_agronomic_url_today(self):
	
        response = rq.get("https://api.awhere.com/v2/agronomics/fields/field4/agronomicnorms/05-01,07-12/?limit=1&offset=72",
                          headers=auth_headers)
	
        responseJSON = response.json()


        # Display the count of dailyNorms the user has on their account
        dailyNorms = responseJSON["dailyNorms"]
        todayDailyNorm = dailyNorms[0]

        accGDD = todayDailyNorm["accumulatedGdd"]["average"]
        return accGDD

#FUNCTION TO CALL AWHERE
def integrate():
    awhere = AWhereAPI()
    return awhere.get_agronomic_url_today()


def makeWebhookResult(speech):
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "source": "Build conversational interface for your app in 10 minutes."
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
