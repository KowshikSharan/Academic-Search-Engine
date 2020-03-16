# This indexer is used to index https://lfs.aminer.cn/lab-datasets/citation/citation-network1.zip .
# This is a citation network for acm with over 630,000 titles

from datetime import datetime
from elasticsearch import Elasticsearch
import json
import networkx as nx 
dg = nx.DiGraph()
es = Elasticsearch()
# Mention the name of the index to be created. 
esindex="acmindex2"
# Mention the index range, if you do not want to index the entire file. 
start=600000
end=610000
startTime = datetime.now()
print("Start time:",startTime)
inputacm = open('outputacm.txt','r', encoding="utf8")
lines = inputacm.readlines()
graphobj = {
    "index":None,
    "citations": []
}
for line in lines:
    if line.startswith("#index"):
        line = line.replace("\n","")
        graphobj['index'] = line.replace("#index","")
    
    elif line.startswith("#%"):
        line = line.replace("\n","")
        graphobj['citations'].append(line.replace("#%",""))
    elif line.startswith("\n"):
        for cite in graphobj['citations']:
            dg.add_edge(graphobj['index'],cite)
        graphobj = {
        "index":None,
        "citations": []
        }
# used default pagerank alpha values in networkx
pr = nx.pagerank(dg,alpha=0.9)
print("just 54:",dg.out_degree('54'))

jsonobj = {
    "title":None,
    "author": [],
    "year": None,
    "journal": None,
    "index": None,
    "abstract": None,
    "citations": [],
    "pagerank": None,
    "citedby": None
}
# preprocessing text from the citation network for indexing
for line in lines:
    if line.startswith("#*"):
        line = line.replace("\n","")
        jsonobj['title'] = line.replace("#*","")
    
    elif line.startswith("#@"):
        line = line.replace("\n","")
        jsonobj['author'] = line.replace("#@","").split(",")
    
    elif line.startswith("#t"):
        line = line.replace("\n","")
        jsonobj['year'] = line.replace("#t","")

    elif line.startswith("#c"):
        line = line.replace("\n","")
        jsonobj['journal'] = line.replace("#c","")
   
    elif line.startswith("#index"):
        line = line.replace("\n","")
        jsonobj['index'] = line.replace("#index","")
        if isinstance(dg.in_degree(jsonobj['index']),int):
            jsonobj['citedby'] = dg.in_degree(jsonobj['index'])
        else:
            jsonobj['citedby'] =0
        # print("cited by: ",jsonobj['citedby'])
        try:
            jsonobj['pagerank'] = pr[jsonobj['index']]
        except:
            pass
    
    elif line.startswith("#%"):
        line = line.replace("\n","")
        jsonobj['citations'].append(line.replace("#%",""))

    elif line.startswith("#!"):
        line = line.replace("\n","")
        jsonobj['abstract'] = line.replace("#!","")
    
    elif line.startswith("\n"):
        if(int(jsonobj['index'])>=start and int(jsonobj['index'])<end):
            res = es.index(index=esindex, id=jsonobj['index'], body=jsonobj)
            print("document indexed: ", jsonobj['index'])
        else:
            pass
        jsonobj = {
        "title":None,
        "author": [],
        "year": None,
        "journal": None,
        "index": None,
        "abstract": None,
        "citations": [],
        "pagerank": None,
        "citedby": None
        }

    else:
        pass
es.indices.refresh(index=esindex)
print("Start time: ",startTime)
endTime = datetime.now()
print("End time: ",endTime)
# test search query
res = es.search(index=esindex, body={"query": {
    "match": {
"title": "information"
     }
    }
    })
# print(res['hits']['hits'])
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print (hit['_source']) 
#     print ("Score:%d"%hit['_score'])
#     print ('**********************') 
