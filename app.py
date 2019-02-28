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
        self.END_DT = '12-31'
        self.START_DT = '05-01'
        self.START_YEAR = '2015'
        self.END_YEAR = '2018'
        self.THIS_YEAR = '2019'
        self.FIELD = 'field4'
        self.NUM_OF_DAYS = self.number_of_days()
        self._fields_url = 'https://api.awhere.com/v2/fields'
        self._weather_url = 'https://api.awhere.com/v2/weather/fields'
        self._agronomic_url = 'https://api.awhere.com/v2/agronomics/fields/' + self.FIELD + '/agronomicnorms/' + self.START_DT + ',' + self.END_DT + '/?limit=1&offset=' + self.NUM_OF_DAYS
        self._forecasts_url = 'https://api.awhere.com/v2/weather/fields/' + self.FIELD + '/forecasts/' + self.THIS_DT
        self.api_key = 'r4AGIfSxMlQNkUPxQGgLx7kpIKovQCMI'
        self.api_secret = 'S9nipeJJ6AVLmRdG'
        
    def get_agronomic_url_today(self):
        return self.THIS_DT

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
