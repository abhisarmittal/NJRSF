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

    #print('Request:')
    #print(json.dumps(req, indent=4))
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
    #today_date = parameters["today-date"]
    crop = parameters["crop"]

    #aWhere = AWhereAPI(today_date, date)
    #aWhere.get_agronomic_url_today()

    # constructing the resposne string.
    speech = "GDD for" + crop + "as of" + date 
    res = makeWebhookResult(speech)
    return res


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

#AWHERE:

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

        encoded_key_secret = base64.b64encode(bytes(key_secret,
                                                    'utf-8')).decode('ascii')

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

        response = rq.post(auth_url, headers=auth_headers, data=body)

        # .json method is a requests lib method that decodes the response
        return response.json()['access_token']

    def number_of_days(self):
        startDate = date(2018, int(self.START_DT[0:2]), int(self.START_DT[3:5]))
        endDate = date(2018, int(self.END_DT[0:2]), int(self.END_DT[3:5]))
        numOfDays = endDate - startDate
        return str(numOfDays)[0:str(numOfDays).find(' ')+1]

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

        # Perform the HTTP request to obtain the Agronomic Norms for the Field
        response = rq.get(self._agronomic_url, headers=auth_headers)

        responseJSON = response.json()
        dailyNorms = responseJSON["dailyNorms"]
        todayDailyNorm = dailyNorms[dailyNormCount - 1]

        accGDD = todayDailyNorm["accumulatedGdd"]["average"]
        pet = todayDailyNorm["pet"]["average"]
        potentialRatio = todayDailyNorm["ppet"]["average"]
        precipitation = pet * potentialRatio
        waterRequirements = pet - precipitation
        todaysDate = self.END_DT
	
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
            return 'Today\'s date is ' + todaysDate + '. Your water requirements for your cotton crops are: ' + str(waterRequirements) + ' and your crop growth stage is ' + resultGrowthStage
        else:
            return 'Today\'s date is ' + todaysDate + '. Your crop growth stage is ' + resultGrowthStage + '. Do not water your crops.'
