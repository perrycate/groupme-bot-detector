#!/bin/python3
import urllib.request
import json

GROUPME_API = "https://api.groupme.com/v3"

# fetches resource at URL, converts JSON to useful Object
def make_request(base_url, additional_url, token):

    # Hit url, get raw response
    url = base_url + additional_url + "?token=" + token
    response = urllib.request.urlopen(url)

    # Convert raw response to usable JSON object
    response_as_string = response.readall().decode('utf-8')
    obj = json.loads(response_as_string)
    return obj["response"]
