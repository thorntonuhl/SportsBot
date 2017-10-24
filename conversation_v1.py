import json
from watson_developer_cloud import ConversationV1
from news_api import *

#########################
# message
#########################

with open('credentials.json') as js:
    credentials = json.load(js)
    
conversation = ConversationV1(username=str(credentials['username']), password=str(credentials['password']), version='2017-04-21')

workspace_id = '8576b6f8-005a-4eae-9859-52c798ab7214'

article = {}
watson_response = {}

typed = ''
response_message = ''
initial_message = "Hi, I'm Billy, The Cheeky Chatbot! I'll look things up for you!\n"

def conv_att():
    typed = ''
    response_message = ''
    while typed != 'QUIT':
        if response_message != '':
            typed = raw_input(response_message)
        else:
            typed = raw_input(initial_message)
        print "\n"
        watson_response = conversation.message(workspace_id=workspace_id, message_input={'text': typed})
        response_message = watson_response['output']['text'][0]
        try:
            lookup_str = watson_response["entities"][0]["value"]
        except:
            lookup_str = typed
        article, res = lookup(lookup_str)
        response_message += "\n\n" + res + "\n"

conv_att()
