#!/usr/bin/env python
import json
import sys
from datetime import datetime
from elasticsearch import Elasticsearch



# This script get input variables, put them in json and send it to ElasticSearch.
# Currently the ElasticSearch details are hardcoded. Also the data model.


# bubble name ==> the bubble name is a key.It will let the user the option to use a snapshot.
# ==> Or maybe the key has to be the id. (the vSphere id that we keep in Artifactory)
# =====> Decided - will not update existing records. Instead the result will be aggregated by 
#        the bubble name and only the most latest record will be shown. (sort by creation date).
#        So can use automatic id in ElasticSearch.
# =====> Update: Decided to use two models - 
#			1. Keep all data with automatic index. This data will be used in the future. (Because Kibana doesn't support top_hits aggregation).
#			2. Keep the data that we want to show in another index. Here the key will be the bubble name.
# run by
# deploy version
# deploy build #
# bubble machines: [{name: name, ext ip: 1.1.1.1, int ip: 1.1.1.1},{...}]

# createJson
def createJson(bubbleName,user,vs_id):
    data = {}
    data['bubble_name'] = bubbleName
    data['run_by'] = user
    data['vs_id'] = vs_id  # vSphere id
    data['deploy_version'] = "1.1"
    data['deploy_build'] = "2222"
    data['created'] = str(datetime.utcnow().isoformat())
    data['machines'] = str("DC:    ext_ip = 127.0.0.1,  int_ip= 1.0.0.1\r\nApp:  ext_ip= 127.0.0.2,  int_ip= 1.0.0.2\r\nDB:    ext_ip= 127.0.0.3,  int_ip='1.0.0.3")
    print data
    json_data = json.dumps(data)
    print "json_data = " + json_data
    return json_data



# sendToElasticSearch
def sendToElasticSearch(json_data, bubbleName):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    # First send is for collecting all data. Use automatic index.
    es.index(index='bubbles_list', doc_type='type1', body=json.loads(json_data))
    # Secnd send is for currect report. The key is the bubble name so will update existing records.
    es.index(index='bubbles_current_report', doc_type='type1', id=bubbleName, body=json.loads(json_data))

    #call the seach just as example
    #searchExample(es)

# searchExample(es)
# this function is not updated !!!!!
def searchExample(es):
    es.indices.refresh(index="test1_indx")
    body1 = {"query": {"query_string" : {"fields" : ["last_name", "first_name"], "query" : "yyyxxxx OR aaaaa"}}, "size": 2000}
    res = es.search(index="test1_indx", body=body1)
    #res = es.search(index="test1_indx", body={"query": {"match_all": {}}, "size": 2000})
    # show the results
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("%(first_name)s %(last_name)s: %(created)s" % hit["_source"])

    # print with line numbers
    for num, name in enumerate(res['hits']['hits'], start=1):
        #print("{} - {}".format(num,name))
        print("{} - id = {} - first name = {}".format(num,name['_id'], name['_source']['first_name']))

# Function main - Get args and call other functions
if __name__ == "__main__":
    bubbleName = sys.argv[1]
    user = sys.argv[2]
    vs_id = sys.argv[3]
    json_data = createJson(bubbleName,user,vs_id)
    sendToElasticSearch(json_data,bubbleName)
