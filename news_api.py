from eventregistry import *

er = EventRegistry(apiKey = "952dc3ea-86c5-42b0-8d24-f6564a0fc5c9")
print "\n\n"

def lookup(subject = "Chicago Cubs"):
        q = QueryArticlesIter(conceptUri = er.getConceptUri(subject), lang = "eng")
        
        for article in q.execQuery(er):
                if article["lang"] == "eng" or article["lang"] == None:
                        titleinfo = str(article["title"] + " ----------- From " + article["source"]["title"])
                        return article, titleinfo
