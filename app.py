#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
from future import standard_library
standard_library.install_aliases()

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

#FUNCTION TO CALL AWHERE (added crop and date to hello to confirm if the parameters are returned in dialoflow)
def integrate():
    awhere = AWhereAPI()
    #return awhere.get_agronomic_url_today()
    return 'hello' + crop + date


def makeWebhookResult(speech):
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "source": "Build conversational interface for your app in 10 minutes."
    }
