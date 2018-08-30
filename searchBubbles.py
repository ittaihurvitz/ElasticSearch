#!/usr/bin/env python
import json
from elasticsearch import Elasticsearch


# searchBubbles()
def searchBubbles():
    # Connect to the server
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    # Define the query and aggregations
    json_body = """
		{
		    "query": {
		    	"match_all": {}
			},
	    	"aggs": {
	    		"bubble_run_by": {
	        		"terms": {
	        			"field": "run_by",
	        			"size": 10
	        		},
	        		"aggs": {
			    		"top_record_agg": {
			        		"top_hits": {
			            		"size": 1
			        		}
			    		}	        		
	        		}
	    		}
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

    # Run the query
    res = es.search(index="bubbles_list", body=json_body)

    # for debugging can run theis:
    #res = es.search(index="bubbles_list", body={"query": {"match_all": {}}, "size": 2000})

    # Print the results (for debug)
    print("Got %d Hits. But the report is:" % res['hits']['total'])
    for bucket in res['aggregations']['bubble_run_by']['buckets']:
    	for hit in bucket['top_record_agg']['hits']['hits']:
    		#print hit
    		print("Bubble name: %(bubble_name)s  Ran by: %(run_by)s  Version: %(vs_id)s" % hit["_source"])
    	
	# Save the results (for debug)
	with open('data.json', 'w') as outfile:
	    json.dump(res, outfile)

# Function main - Get args and call other functions
if __name__ == "__main__":
    searchBubbles()
