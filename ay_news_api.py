import aylien_news_api
from aylien_news_api.rest import ApiException
import re
import pdb

def ay_lookup(keyword, subject = '',entities = [],timeframe = '0,2'):
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
      'entities_body_text' : entities
    }
    if subject != '':
        opts['text'] = subject
    first = timeframe.split(',')[0]
    second = timeframe.split(',')[1]
    if first == '0':
        first = 'NOW'
    else:
        first = 'NOW-'+first+'DAYS'
    second = 'NOW-'+second+'DAYS'
    opts['published_at_start'] = second
    opts['published_at_end'] = first
    try:
        api_response = api_instance.list_stories(**opts)
        api_response.stories
        for i in range(0, len(api_response.stories)):
            story = api_response.stories[i]
            if "Sign up for one of our email newsletters." not in story.body:
                try:
                    body_clauses = clean_st(story.body.replace("\n"," ")).split('.')
                    while '' in body_clauses:
                        body_clauses.remove('')
                except:
                    body_clauses = []
                try:
                    summary = story.summary['sentences']
                except:
                    summary = []
                summarycounter = 0
                bodycounter = 0
                st = ''
                body_clauses = fix_clauses(body_clauses)
                while '' in body_clauses:
                    body_clauses.remove('')
                while bodycounter < len(body_clauses) and st == '':
                    try:
                        st = summary[summarycounter]
                        initial = summarycounter
                        summarycounter += 1
                        lst = body_clauses
                    except:
                        st = body_clauses[bodycounter]+"."
                        initial = bodycounter
                        bodycounter += 1
                        lst = summary
                    top = initial + 1
                    st = clean_st(st)
                    while bad_string(st) and top < len(lst):
                        if lst[initial:top] != []:
                            st = lst[initial:top].join('.') + '.'
                        top += 1
                    if 'photo' in st.lower() or 'file' in st.lower() or st[0] == st[0].lower() or '(' in st or ')' in st:
                        st = ''
                    st = clean_st(st)
                if len(st) > 10 and bad_string(st) != True:
                    return story, st
    except ApiException as e:
        print("Exception when calling DefaultApi->list_stories: %s\n" % e)
        return {},''

def bad_string(st):
    try:
        if regex_check(clean_st(st)) == False:
            return True
        elif len(st) < 15:
            return True
        else:
            return False
    except:
        return True

def regex_check(st):
    if st[-1] == '.':
        st = st[:-1]
    t = ' '+st
    if re.match("(?! .)", t[len(t)-2:]) == None:
        return False
    if re.match("(?! ..)", t[len(t)-3:]) == None:
        return False
    if re.match("(?! ...)", t[len(t)-4:]) == None:
        return False
    return True


def clean_st(st):
    if st == '':
        return st
    try:
        if 'About ' in st[:6]:
            st = st[6:]
    except:
        pass
    st = st.replace('\n',' ')
    while st != '' and st[0] == ' ':
        st = st[1:]
    while st != '' and st[-1] == ' ':
        st = st[:len(st)-1]
    while '  ' in st:
        st = st.replace('  ',' ')
    while '..' in st:
        st = st.replace('..','.')
    return st

def fix_clauses(clauses):
    clauses[-1] = clauses[-1][:-1]
    if len(clauses) < 2:
        return clauses
    else:
        current = 0
        extra = current + 1
        while extra < len(clauses):
            if len(clauses[current]) < 20 or len(clauses[extra]) < 20 or not bad_string(clauses[current]):
                clauses[current] = clauses[current] + '. ' + clauses[extra]
                clauses.remove(clauses[extra])
            else:
                current += 1
                extra = current + 1
        return clauses
