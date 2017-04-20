from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

index = "myindex"
docType ='tweet'
document = {
    'author': 'erol',
    'text': 'Elasticsearch: first example',
    'timestamp': datetime.now()
}

# save index
res = es.index(index=index, doc_type=docType  ,id=1, body=document)
print(res['created'])

# get index by id and doc_type
res = es.get(index=index, doc_type='tweet', id=1)
print(res['_source'])

# return all records
es.indices.refresh(index=index)
res = es.search(index=index, body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])