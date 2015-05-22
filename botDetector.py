#!/bin/python3
import urllib.request
import json

GROUPME_API = "https://api.groupme.com/v3"
user_token = input("Please enter your API Token: ")
bot_id = input("Please enter an existing bot's Id: ")

connection = get_push_connection()
clientId = connection["clientId"]

# create handshake with groupme server to recieve new messages
def get_push_connection():
    # data required by groupme for initial handshake
    handshake_data = json.dumps([
                        {
                            "channel":"/meta/handshake",
                            "version":"1.0",
                            "supportedConnectionTypes":["long-polling"],
                            "id":"1"
                        }])
    # encode data into bytes and send to groupme
    data = handshake_data.encode('utf-8')
    request = urllib.request.Request("https://push.groupme.com/faye",
            data, {"Content-Type":"application/json"})
    response = urllib.request.urlopen(request)

    # convert response to usable object format
    response_string = response.readall().decode('utf-8')
    response_object = json.loads(response_string)
    # json.loads will return array with length 1, strip array
    return response_object[0]

# fetches resource at URL, converts JSON to useful Object
def make_request(base_url, additional_url, token):

    # Hit url, get raw response
    url = base_url + additional_url + "?token=" + token
    response = urllib.request.urlopen(url)

    # Convert raw response to usable JSON object
    response_as_string = response.readall().decode('utf-8')
    obj = json.loads(response_as_string)
    return obj["response"]
