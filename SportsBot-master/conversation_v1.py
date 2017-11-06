import json
from watson_developer_cloud import ConversationV1
#from news_api import *
from ay_news_api import *
import pdb

from flask import Flask,render_template,request
app = Flask(__name__)


#def hello_world():
 #   return 'Hello, World!'



#########################
# message
#########################

with open('credentials.json') as js:
    credentials = json.load(js)
    
conversation = ConversationV1(username=str(credentials['username']), password=str(credentials['password']), version='2017-04-21')

workspace_id = '4821b731-49db-4497-9376-5fc787771924'

story = {"body" : ''}
watson_response = {}


@app.route('/')
def input_display():
    input_text = request.args.get('input')

    if input_text == None or input_text == '':
        return render_template('sports_bot.html', name='I\'m the sports bot. How can I help?')
    
    else:
        output = conv_att(input_text)
        return render_template('sports_bot.html', name=output)


typed = ''
res = ''
subject = ''

def conv_att(input_text):
        if "subject" in typed.lower():
            try:
                return subject
            except:
                return "Subject Unavailable."
        elif "more" in typed.lower():
            try:
                return story.body
            except:
                return "Story Unavailable."
        elif "source" in typed.lower():
            try:
                return story.source.name
            except:
                return "Source Unavailable."
        elif "author" in typed.lower():
            try:
                return story.author.name
            except:
                return "Author Unavailable."
        elif "description" in typed.lower():
            if res != '':
                return res
            else:
                return "Description Unavailable."
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
        return res
        

#conv_att()
app.run()
