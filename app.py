# import flask modules
from flask import Flask, make_response, request, jsonify

# build the flask app
app = Flask(__name__)

# definition of the results function
def results():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')

    if action == "gdd":
        # your action statements here
        # do whatever you want
        # return response in dialogflow response format
        # i am going to use Dialogflow JSON reponse format
        # first build result json

        result = {} # an empty dictionary

        # fulfillment text is the default response that is returned to the dialogflow request
        result["fulfillmentText"] = "testing gdd"
