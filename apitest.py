import aylien_news_api
from aylien_news_api.rest import ApiException

# Configure API key authorization: app_id
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = 'e6ddf398'
# Configure API key authorization: app_key
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'db5180ad10ac1324aadd57451fded0a8'

# create an instance of the API class
api_instance = aylien_news_api.DefaultApi()

opts = {
  'title': 'new england patriots',
  #'sort_by': 'social_shares_count.facebook',
  'sort_by':'relevance',
  'language': ['en'],
  'published_at_start': 'NOW-1DAYS',
  'published_at_end': 'NOW',
  'per_page': 1
}

try:
    # List stories
    api_response = api_instance.list_stories(**opts)
    print("API called successfully. Returned data: ")
    print("========================================")
    for story in api_response.stories:
      print(story.body + " / " + story.source.name)
except ApiException as e:
    print("Exception when calling DefaultApi->list_stories: %s\n" % e)
