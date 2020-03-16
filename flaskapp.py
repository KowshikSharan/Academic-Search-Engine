from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from elasticsearch import Elasticsearch
# Name of the index to be used
esindex='acmindex2'

def Search(title):
    es = Elasticsearch()
    suggestarray = []
    suggestion=""
    suggestflag=False
    # This query is used to retrieve suggestions from elasticsearch. I make use of only the top suggestion.
    suggestquery = es.search(index=esindex,body={
        "suggest": {
            "mytermsuggester": {
                "text": title,
                "term": {
                    "field": "title"
                }
            }
        }
    })
    print("suggestquery: ",suggestquery['suggest']['mytermsuggester'])
    for hit in suggestquery['suggest']['mytermsuggester']:
        i=0
        if hit['options']!=[]:
            suggestion = hit['options'][0]['text']
        else:
            pass
        
    if suggestion == "":
        suggestion = title
    else:
        suggestflag=True
    # This is the search query. it currently searches titles, but can be modified to search any other field. 
    res = es.search(index=esindex, size=15,body={
    "query": {
        "match": {
            "title": suggestion
                }
            },
     "sort":{
         "pagerank":"desc"
     }
        })
    hits = res['hits']['total']['value']
    meta = {'meta':{
        'hits':hits,
        'suggestion':suggestion,
        'suggestflag':suggestflag
    }}
    sourcearray=[]
    i=0
    for hit in res['hits']['hits']:
        sourcearray.append(hit['_source']) 
        print(sourcearray[i])
        i+=1
    sourcearray.append(meta)
    print("Got %d Hits:" % res['hits']['total']['value'])
    # for hit in res['hits']['hits']:
    #     # print (hit['_source']) 
    #     # print ("Score:%d"%hit['_score'])
    #     print(i)
    #     i+=1
    #     print ('**********************') 
    return(sourcearray)


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/search")
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getSearchResults():
    print("request:",request)
    res = Search(request.args.get('title'))  
    return (jsonify(res))

if __name__ == '__main__':
    app.run(debug=True)