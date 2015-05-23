#!/bin/python3
import urllib.request
import json
import time

GROUPME_API = "https://api.groupme.com/v3"
PUSH_SERVER_URL = "https://push.groupme.com/faye"

# groupme keeps track of # of calls apparently
current_call_number = 1

def main():
    user_token = input("Please enter your API Token: ")
    bot_id = input("Please enter an existing bot's Id: ")
    group_id = input("Please enter a group Id: ")

    connection = get_push_connection()
    client_id = connection["clientId"]

    subscribe_to_group(client_id, group_id, user_token)

# create handshake with groupme server to recieve new messages
def get_push_connection():
    global current_call_number
    # data required by groupme for initial handshake
    handshake_data = [
                        {
                            "channel":"/meta/handshake",
                            "version":"1.0",
                            "supportedConnectionTypes":["long-polling"],
                            "id":str(current_call_number)
                        }
                     ]

    response = make_request_sending_json(PUSH_SERVER_URL, handshake_data)
    current_call_number += 1

    # request will return array with length 1, strip array
    return response[0]


def subscribe_to_group(client, group, token):
        global current_call_number

        data = [
                      {
                        "channel":"/meta/subscribe",
                        "clientId":client,
                        "subscription":"/group/" + group,
                        "id":current_call_number,
                        "ext":
                          {
                            "access_token":token,
                            "timestamp":time.time()
                          }
                      }
                    ]

        response = make_request_sending_json(PUSH_SERVER_URL, data)
        current_call_number += 1
        return response[0]


# fetches resource at URL, converts JSON response to useful Object
def make_request(base_url, additional_url, token):

    # Hit url, get raw response
    url = base_url + additional_url + "?token=" + token
    response = urllib.request.urlopen(url)

    # Convert raw response to usable JSON object
    response_as_string = response.readall().decode('utf-8')
    obj = json.loads(response_as_string)
    return obj["response"]

# Like make_request, but also sends json data.
def make_request_sending_json(url, data):
    # encode data into format the request can use
    data = json.dumps(data);
    data = data.encode('utf-8')
    request = urllib.request.Request(url, data,
                            {"Content-Type":"application/json"})
    response = urllib.request.urlopen(request)

    # convert response into usable object format
    response = response.readall().decode('utf-8')
    response = json.loads(response)
    return response

# only true if the program was called via the command line.
if __name__ == "__main__":
    main()
