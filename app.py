#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

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

#def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access. 
    #req_dict = json.loads(request.data)
    #entity_type = ""
    #entity_value = ""
    # Accessing the fields on the POST request boduy of API.ai invocation of the webhook
    #intent = req_dict["result"]["metadata"]["intentName"]

    #entity_key_val = req_dict["result"]["parameters"]
    #for key in entity_key_val:
	    #entity_value = entity_key_val[key]
	    #entity_type = key 
    
    # constructing the resposne string.
    #speech = "Hey, Got your request, Responding from webhook " + "The Intent is: " + intent + ": The entity type is: " + entity_type + ": The entity value is: " + entity_value  
    #res = makeWebhookResult(speech)
    #return res

def settingVariables(req):
	result = req.get('result')
	parameters = result.get('parameters')
	crop = parameters.get('crop')
    todayDate = parameters.get('date')
	
    speech = "Your crop is" + crop + "Today's date is" + date
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
