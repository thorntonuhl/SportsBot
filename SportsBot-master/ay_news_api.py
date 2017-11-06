import aylien_news_api
from aylien_news_api.rest import ApiException
import re
import pdb

def ay_lookup(keyword, subject = '',entities = []):
    # Configure API key authorization: app_id
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = 'e6ddf398'
    # Configure API key authorization: app_key
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'db5180ad10ac1324aadd57451fded0a8'

    # create an instance of the API class
    api_instance = aylien_news_api.DefaultApi()

    opts = {
      'title': keyword,
      'body': keyword,
      'sort_by': 'relevance',
      'language': ['en'],
      'published_at_start': 'NOW-2DAYS',
      'published_at_end': 'NOW',
      'entities_body_text' : entities
    }
    if subject != '':
        opts['text'] = subject
    try:
        api_response = api_instance.list_stories(**opts)
        api_response.stories
        for i in range(0, len(api_response.stories)):
            story = api_response.stories[i]
            if "Sign up for one of our email newsletters." not in story.body:
                try:
                    body_clauses = story.body.replace("\n"," ").split('. ')
                except:
                    body_clauses = []
                lst = body_clauses
                try:
                    summary = story.summary['sentences']
                except:
                    summary = []
                st = ''
                counter1 = 0
                counter2 = 0
                while counter2 < len(body_clauses) and st == '':
                    try:
                        st = summary[counter1]
                        intitial = counter1
                        counter1 += 1
                        initial = counter1
                    except:
                        st = body_clauses[counter2]+"."
                        initial = counter2
                        counter2 += 1
                    top = initial + 1
                    st = st.replace('\n',' ')
                    if len(st) > 40:
                        st = st.split('. ')[0]+"."
                    if initial != counter2:
                        lst = summary
                    while bad_string(st) and top < len(lst):
                        if lst[initial:top] != []:
                            st = lst[initial:top].join('. ') + "."
                        top += 1
                    if 'photo' in st.lower() or 'file' in st.lower() or st[0] == st[0].lower() or '(' in st or ')' in st:
                        st = ''
                    st = st.replace('..','.')
                if len(st) > 10:
                    return story, st
    except ApiException as e:
        print("Exception when calling DefaultApi->list_stories: %s\n" % e)
        return {},''

def bad_string(st):
    try:
        if (re.match("( ...\.)", st[len(st)-5:]) != None or
            re.match("(^*.\.)", st[len(st)-10:]) != None or
            re.match("( .\.)", st[len(st)-3:]) != None or
            re.match("( ..\.)", st[len(st)-4:]) != None):
            return True
        elif len(st) < 10:
            return True
        elif "vs." in st[len(st)-4:]:
            return True
        else:
            return False
    except:
        return True
