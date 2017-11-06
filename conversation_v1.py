import json
from watson_developer_cloud import ConversationV1
from ay_news_api import *

from flask import Flask,render_template,request
app = Flask(__name__)

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

res = ''
subject = ''

def conv_att(input_text):
        if "subject" in input_text.lower():
            try:
                return subject
            except:
                return "Subject Unavailable."
        elif "more" in input_text.lower():
            try:
                return story.body
            except:
                return "Story Unavailable."
        elif "source" in input_text.lower():
            try:
                return story.source.name
            except:
                return "Source Unavailable."
        elif "author" in input_text.lower():
            try:
                return story.author.name
            except:
                return "Author Unavailable."
        elif "description" in input_text.lower():
            if res != '':
                return res
            else:
                return "Description Unavailable."
        else:
            watson_response = conversation.message(workspace_id=workspace_id, message_input={'text': input_text})
            response_message = ''
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
                lookup_str = input_text
                subject = ''
            response = None
            counter = 2
            while response == None:
                response = ay_lookup(lookup_str, subject, entities, '0,'+str(counter))
                counter += 2
            story = response[0]
            res = response[1]
        return res
        
app.run()
