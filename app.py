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
import sys
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
    sys.stdout.flush()

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

def makeWebhookResult(speech):
    print("Response:")
    sys.stdout.flush()
    print(speech)
    sys.stdout.flush()

    return {
        "speech": speech,
        "displayText": speech,
        "source": "Build conversational interface for your app in 10 minutes."
    }

#FUNCTION TO CALL AWHERE
def integrate():
    awhere = AWhereAPI('12-31', 'cotton')
    return awhere.get_agronomic_url_today()

#AWHERE
class AWhereAPI(object):
    def __init__(self, end_dt, crop):
        """
        Initializes the AWhereAPI class, which is used to perform HTTP requests 
        to the aWhere V2 API.
        elf.        Docs:
            http://developer.awhere.com/api/reference
        """
        
        self.THIS_DT = datetime.datetime.today().strftime('%m-%d')
        self.END_DT = end_dt
        self.START_DT = '05-01'
        self.START_YEAR = '2015'
        self.END_YEAR = '2018'
        self.THIS_YEAR = '2019'
        self.CROP = crop
        self.FIELD = 'field4'
        self.NUM_OF_DAYS = self.number_of_days()
        self._fields_url = 'https://api.awhere.com/v2/fields'
        self._weather_url = 'https://api.awhere.com/v2/weather/fields'
        self._agronomic_url = 'https://api.awhere.com/v2/agronomics/fields/' + self.FIELD + '/agronomicnorms/' + self.START_DT + ',' + self.END_DT + '/?limit=1&offset=' + self.NUM_OF_DAYS
        self._forecasts_url = 'https://api.awhere.com/v2/weather/fields/' + self.FIELD + '/forecasts/' + self.THIS_DT
        self.api_key = 'r4AGIfSxMlQNkUPxQGgLx7kpIKovQCMI'
        self.api_secret = 'S9nipeJJ6AVLmRdG'
        self.base_64_encoded_secret_key = self.encode_secret_and_key(self.api_key, self.api_secret)
        self.auth_token = self.get_oauth_token(self.base_64_encoded_secret_key)

    def number_of_days(self):
        startDate = date(2018, int(self.START_DT[0:2]), int(self.START_DT[3:5]))
        endDate = date(2018, int(self.END_DT[0:2]), int(self.END_DT[3:5]))
        numOfDays = endDate - startDate
        numOfDaysStr = str(numOfDays)[0:str(numOfDays).find(' ')+1]
        print('\nnumber_of_days:: numOfDaysStr: %s' % numOfDaysStr)
        sys.stdout.flush()
        return numOfDaysStr

    def encode_secret_and_key(self, key, secret):
        """
        Docs:
            http://developer.awhere.com/api/authentication
        Returns:
            Returns the base64-encoded {key}:{secret} combination, seperated by a colon.
        """
        # Base64 Encode the Secret and Key
        key_secret = '%s:%s' % (key, secret)
        print('\nKey and Secret before Base64 Encoding: %s' % key_secret)
        sys.stdout.flush()
        encoded_key_secret = base64.b64encode(bytes(key_secret,
                                                    'utf-8')).decode('ascii')
        print('Key and Secret after Base64 Encoding: %s' % encoded_key_secret)
        sys.stdout.flush()
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
        print('\nget_oauth_token:: Headers: %s' % auth_headers)
        sys.stdout.flush()
        print('\nget_oauth_token:: Body: %s' % body)
        sys.stdout.flush()
        response = rq.post(auth_url, headers=auth_headers, data=body)
        # .json method is a requests lib method that decodes the response
        responseJSON = response.json()
        print('\nget_oauth_token:: ResponseJSON: %s' % responseJSON)
        sys.stdout.flush()
        return responseJSON['access_token']

    def get_agronomic_url_today(self):
        """
        Performs a HTTP GET request to obtain Agronomic Norms
        Docs: 
            1. Agronomic: https://developer.awhere.com/api/reference/agronomics/norms
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": "Bearer %s" % self.auth_token,
        }
        print('\nget_agronomic_url_today:: Headers: %s' % auth_headers)
        sys.stdout.flush()
        # Perform the HTTP request to obtain the Agronomic Norms for the Field
        response = rq.get(self._agronomic_url, headers=auth_headers)
        responseJSON = response.json()
        print('\nget_agronomic_url_today:: ResponseJSON: %s' % responseJSON)
        sys.stdout.flush()
        todayDailyNorm = responseJSON["dailyNorms"][0]
        accGDD = todayDailyNorm["accumulatedGdd"]["average"]
        pet = todayDailyNorm["pet"]["average"]
        potentialRatio = todayDailyNorm["ppet"]["average"]
        precipitation = pet * potentialRatio
        waterRequirements = pet - precipitation
        print('\nget_agronomic_url_today:: precipitation: %f' % precipitation)
        sys.stdout.flush()
        print('\nget_agronomic_url_today:: waterRequirements: %f' % waterRequirements)
        sys.stdout.flush()
        #response2 = rq.get(self._forecasts_url, headers=auth_headers)
        #response2JSON = response2.json()
        rainy=False
        #forecast = response2JSON['forecast']
        #condition = forecast[0]['conditionsText']
        #if condition.find('No Rain') >= 0:
            #rainy = False
        if accGDD < 1:
            resultGrowthStage = "emergence"
        elif accGDD > 1:
            resultGrowthStage = "open flower"
        if (potentialRatio < 1) & (not rainy):
            return 'Today\'s date is ' + self.END_DT + '. Your water requirements for your cotton crops are: ' + str(waterRequirements) + ' and your crop growth stage is ' + resultGrowthStage
        else:
            return 'Today\'s date is ' + self.END_DT + '. Your crop growth stage is ' + resultGrowthStage + '. Do not water your crops.'

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0', threaded=True)
