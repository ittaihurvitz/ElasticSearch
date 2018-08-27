#!/usr/bin/env python
import json
import sys
from datetime import datetime
from elasticsearch import Elasticsearch



# This script get input variables, put them in json and send it to ElasticSearch.
# Currently the ElasticSearch details are hardcoded. Also the data model.


# createJson
def createJson(bubbleName,user):
    data = {}
    data['first_name'] = bubbleName
    data['last_name'] = user
    data['created'] = str(datetime.utcnow().isoformat())
    data['edited'] = str(datetime.utcnow().isoformat())
    data['new date'] = str(datetime.utcnow().isoformat())
    data['new date2'] = str(datetime.utcnow().isoformat())
    data['new date3'] = str(datetime.utcnow().isoformat()) + 'Z'
    data['new date4'] = str(datetime.utcnow().isoformat())
    print data
    json_data = json.dumps(data)
    print "json_data = " + json_data
    return json_data



# sendToElasticSearch
def sendToElasticSearch(json_data):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    es.index(index='test1_indx', doc_type='type1', body=json.loads(json_data))
    #call the seach just as example
    searchExample(es)

# searchExample(es)
def searchExample(es):
    es.indices.refresh(index="test1_indx")
    res = es.search(index="test1_indx", body={"query": {"match_all": {}}, "size": 2000})
    # show the results
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("%(first_name)s %(last_name)s: %(created)s" % hit["_source"])

# Function main - Get args and call other functions
if __name__ == "__main__":
    bubbleName = sys.argv[1]
    user = sys.argv[2]
    json_data = createJson(bubbleName,user)
    sendToElasticSearch(json_data)
