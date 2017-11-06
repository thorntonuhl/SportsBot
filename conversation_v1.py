import json
from watson_developer_cloud import ConversationV1
#from news_api import *
from ay_news_api import *
import pdb

#########################
# message
#########################

with open('credentials.json') as js:
    credentials = json.load(js)
    
conversation = ConversationV1(username=str(credentials['username']), password=str(credentials['password']), version='2017-04-21')

workspace_id = '4821b731-49db-4497-9376-5fc787771924'

story = {"body" : ''}
watson_response = {}

typed = ''
response_message = ''
initial_message = "Hi, I'm Billy, The Cheeky Chatbot! I'll look things up for you!\n\n\n"

print '\n\n'

def conv_att():
    typed = ''
    response_message = ''
    while typed.lower() != 'quit':
        if response_message == '':
            typed = raw_input(initial_message)
        else:
            typed = raw_input(response_message)
            
        print "\n"
        
        if "more" in typed.lower():
            response_message = story.body
        elif "source" in typed.lower():
            try:
                response_message = story.source.name
            except:
                response_message = "Source Unavailable."
        elif "author" in typed.lower():
            try:
                response_message = story.author.name
            except:
                response_message = "Author Unavailable."
        elif "description" in typed.lower():
            try:
                response_message = res
            except:
                response_message = "Description Unavailable."
        else:
            watson_response = conversation.message(workspace_id=workspace_id, message_input={'text': typed})
            response_message = ''#watson_response['output']['text'][0]
            #print watson_response
            entities = []
            try:
                lookup_str = watson_response["entities"][0]["value"]
                for i in range(0,len(watson_response['entities'])):
                    entities.append(watson_response["entities"][i]["value"])
                try:
                    subject = watson_response["intents"][0]["value"]
                except:
                    subject = ''
            except:
                lookup_str = typed
                subject = ''
            story, res = ay_lookup(lookup_str, subject, entities)
            response_message += res
        response_message += "\n\n\n"

conv_att()
