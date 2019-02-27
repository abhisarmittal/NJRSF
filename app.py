#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future.standard_library import install_aliases
install_aliases()
from builtins import str
from builtins import bytes
from future import standard_library
standard_library.install_aliases()
from builtins import object
import requests as rq
import base64
import pprint
import json
import random
import datetime

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

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
    aWhere = AWhereAPI('02-25', '12-31')
    aWhere.get_agronomic_url_today()
	
    # constructing the resposne string.
    speech = "Hey, Got your request, Responding from webhook " + "The Intent is: " + intent + ": The entity type is: " + entity_type + ": The entity value is: " + entity_value  
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

#AWHERE INTEGRATION

class AWhereAPI(object):
    def __init__(self, this_dt, end_dt):
        """
        Initializes the AWhereAPI class, which is used to perform HTTP requests 
        to the aWhere V2 API.
        elf.        Docs:
            http://developer.awhere.com/api/reference
        """
        self.END_DT = end_dt
        self.THIS_DT = this_dt
        #self.END_DT = datetime.datetime.today().strftime('%m-%d')
        self.START_DT = '02-10'
        self.START_YEAR = '2015'
        self.END_YEAR = '2018'
        self.THIS_YEAR = '2019'
        self._fields_url = 'https://api.awhere.com/v2/fields'
        self._weather_url = 'https://api.awhere.com/v2/weather/fields'
        #self._agronomic_url = 'https://api.awhere.com/v2/agronomics/fields/field3/agronomicnorms/08-01,12-31/years/2010,2014'
        self._agronomic_url_today = 'https://api.awhere.com/v2/agronomics/fields/field4/agronomicnorms'
        #self._forecasts_url_today = 'https://api.awhere.com/v2/weather/fields/field1/forecasts/2019-02-21'
        self._forecasts_url = 'https://api.awhere.com/v2/weather/fields/field1/forecasts'
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
        response = rq.get(
            self._agronomic_url_today + '/' + self.START_DT + ',' +
            self.END_DT + '/years/' + self.START_YEAR + ',' +
            self.END_YEAR,
            headers=auth_headers)

        responseJSON = response.json()

        # Display the count of dailyNorms the user has on their account
        dailyNormCount = len(responseJSON["dailyNorms"])
        dailyNorms = responseJSON["dailyNorms"]
        todayDailyNorm = dailyNorms[dailyNormCount - 1]

        accGDD = todayDailyNorm["accumulatedGdd"]["average"]
        pet = todayDailyNorm["pet"]["average"]
        potentialRatio = todayDailyNorm["ppet"]["average"]
        precipitation = pet * potentialRatio
        waterRequirements = pet - precipitation
        todaysDate = self.END_DT
	
        response2 = rq.get(
            self._forecasts_url + '/' + self.THIS_DT, headers=auth_headers)
        response2JSON = response2.json()

        forecast = response2JSON['forecast']
        condition = forecast[0]['conditionsText']
        if condition.find('No Rain') >= 0:
            rainy = False

        if accGDD < 1:
            resultGrowthStage = "emergence"

        elif accGDD > 1:
            resultGrowthStage = "open flower"

        if (potentialRatio < 1) & (not rainy):
            return 'Today\'s date is ' + todaysDate + '. Your water requirements for your cotton crops are: ' + str(waterRequirements) + ' and your crop growth stage is ' + resultGrowthStage
        else:
            return 'Today\'s date is ' + todaysDate + '. Your crop growth stage is ' + resultGrowthStage + '. Do not water your crops.'
