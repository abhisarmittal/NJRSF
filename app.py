#!/usr/bin/python
# -*- coding: utf-8 -*

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
    
    parameterDate = parameters["date"][5:10]
    parameterCrop = parameters["crop"]
    parameterLang = req_dict["lang"]

    # checking for faults in parameters
    startDt = date(2018, 5, 1)
    endDt = date(2018, int(parameterDate[0:2]), int(parameterDate[3:5]))
    if startDt>endDt:
        if parameterLang == "en":
            speech = 'Growing season did not start yet!'
        if parameterLang == "hi":
            speech = 'बढ़ता मौसम अभी तक शुरू नहीं हुआ था!'
        if parameterLang == "es":
            speech = 'La temporada de crecimiento no comenzó todavía!'
        if parameterLang == "fr":
            speech = 'Saison de croissance n a pas encore commencé!'

    # constructing the resposne string.
    else:
        speech = integrate(parameterDate, parameterCrop, parameterLang)
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
def integrate(date, crop, lang):
    awhere = AWhereAPI(date, crop, lang)
    return awhere.get_agronomic_url_today()

#AWHERE
class AWhereAPI(object):
    def __init__(self, end_dt, crop, lang):
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
        self.LANG = lang
        if self.CROP == 'cotton':
            self.FIELD = 'field4'
        elif self.CROP == 'corn':
            self.FIELD = 'field1'
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

    def construct_response(self, potentialRatio, rainy, waterRequirements, resultGrowthStage, accGDD, pet, ppet):
        if (potentialRatio < 1) & (not rainy):
            if (self.LANG == 'en'):
                return 'Today\'s date is ' + self.END_DT + '. PET is ' + str(pet) + 'and PPET is ' + str(ppet) + '. So, the water requirements for your ' + self.CROP + ' crops are: ' + str(waterRequirements) + ' mm. Accumulated GDD is ' + str(accGDD) + '. So, your crops\' growth stage is ' + resultGrowthStage + '.'
            elif (self.LANG == 'hi'):
                return 'आज की तारीख ' + self.END_DT + 'है। PET ' + str(pet) + ' है और PPET ' + str(ppet) + ' है। इसलिए, ' + self.CROP + ' की फसल के लिए आपकी पानी की जरूरतें ' + str(waterRequirements) + ' मिलीमीटर हैं। Accumulated GDD ' + str(accGDD) + ' है। इसलिए,फसल वृद्धि अवस्था '+ resultGrowthStage + 'है।'
            elif (self.LANG == 'es'):
                return 'La fecha de hoy es ' + self.END_DT + '. PET es ' + str(pet) + ' y PPET es ' + str(ppet) + '. Asi que, las necesidades de agua de sus cultivos de ' + self.CROP + ' son de ' + str(waterRequirements) + ' milímetros. Accumulated GDD es ' + str(accGDD) + '. Asi que, la etapa de crecimiento de los cultivos es ' + resultGrowthStage + '.'
            elif (self.LANG == 'fr'):
                return 'La date d\'aujourd\'hui est ' + self.END_DT + '. PET est ' + str(pet) + ' et PPET est ' + str(ppet) + '. Alors, les besoins en eau de vos cultures de ' + self.CROP + ' sont de ' + str(waterRequirements) + ' millimètres. Accumulated GDD est ' + str(accGDD) + '. Alors, le stade de croissance de la culture est ' + resultGrowthStage + '.'
        else:
            if (self.LANG == 'en'):
                return 'Today\'s date is ' + self.END_DT + '. Your ' + self.CROP + ' crops\' growth stage is ' + resultGrowthStage + '. Do not water your crops.'
            elif (self.LANG == 'hi'):
                return 'आज की तारीख ' + self.END_DT + 'है। ' + self.CROP + ' की फसल फसल वृद्धि अवस्था ' + resultGrowthStage + ' है। अपनी फसलों को पानी न दें।'
            elif (self.LANG == 'es'):
                return 'La fecha de hoy es ' + self.END_DT + '. La etapa de crecimiento de sus cultivos de ' + self.CROP + ' es ' + resultGrowthStage + '. No riegues tus cultivos.'
            elif (self.LANG == 'fr'):
                return 'La date d\'aujourd\'hui est ' + self.END_DT + '. Le stade de croissance de vos cultures de ' + self.CROP + ' est ' + resultGrowthStage + '. N\'arrosez pas vos cultures.'

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
        waterRequirements = float("{0:.2f}".format(pet - precipitation))
        print('\nget_agronomic_url_today:: precipitation: %f' % precipitation)
        sys.stdout.flush()
        print('\nget_agronomic_url_today:: waterRequirements: %f' % waterRequirements)
        sys.stdout.flush()
	
        response2 = rq.get(self._forecasts_url, headers=auth_headers)
        response2JSON = response2.json()
        print('\nget_agronomic_url_today:: Response2JSON: %s' % response2JSON)
	
        forecast = response2JSON['forecast']
        condition = forecast[0]['conditionsText']
        print('\nget_agronomic_url_today:: Condition: %s' % condition)
        rainy=True
        if condition.find('No Rain') >= 0:
            rainy = False
        if not self.THIS_DT == self.END_DT:
            rainy = False
	
        #if crop is cotton
        if self.CROP == 'cotton':
            if accGDD>=0 and accGDD <28:
                resultGrowthStage = 'planted'
            elif accGDD >= 28 and accGDD < 306:
                resultGrowthStage = "emergence"
            elif accGDD >= 306 and accGDD < 528:
                resultGrowthStage = "first-square"
            elif accGDD >= 528 and accGDD < 1194:
                resultGrowthStage = "first-flower"
            elif accGDD >= 1194 and accGDD < 1444:
                resultGrowthStage = "open-bolli"
            elif accGDD >= 1444:
                resultGrowthStage = "harvest"

        #if crop is corn
        if self.CROP == 'corn':
            if accGDD>=0 and accGDD <65:
                resultGrowthStage = 'planted'
            elif accGDD >= 65 and accGDD < 740:
                resultGrowthStage = "emergence"
            elif accGDD >= 740 and accGDD < 1135:
                resultGrowthStage = "rapid growth"
            elif accGDD >= 1135 and accGDD < 1660:
                resultGrowthStage = "pollination"
            elif accGDD >= 1660 and accGDD < 2700:
                resultGrowthStage = "grain fill"
            elif accGDD >= 2700:
                resultGrowthStage = "harvest"

        return self.construct_response(potentialRatio, rainy, waterRequirements, resultGrowthStage, accGDD, pet, precipitation)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0', threaded=True)
