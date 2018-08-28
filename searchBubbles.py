#!/usr/bin/env python
import json
import sys
from datetime import datetime
from elasticsearch import Elasticsearch


# searchBubbles()
def searchBubbles():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    json_body = """
		{
		  "query": {
		    "match_all": {}
		  },
		  "size": 1,
		  "sort": [
		    {
		      "created": {
		        "order": "desc"
		      }
		    }
		  ]
		}
    """

    #print json_body
    res = es.search(index="bubbles_list", body=json_body)
    #res = es.search(index="bubbles_list", body={"query": {"match_all": {}}, "size": 2000})

    # print the results
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("%(bubble_name)s %(created)s" % hit["_source"])

    # print with line numbers
    for num, name in enumerate(res['hits']['hits'], start=1):
        #print("{} - {}".format(num,name))
        print("{} - id = {} - bubble name = {}".format(num,name['_id'], name['_source']['bubble_name']))

# Function main - Get args and call other functions
if __name__ == "__main__":
    searchBubbles()
