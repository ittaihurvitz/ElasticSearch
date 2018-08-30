# This code sceeded to update the mapping called "type1" under index "bubble_list
# it updated the field "bubble_name" to have "fielddata": true

import requests

url     = 'http://localhost:9200/bubbles_list/_mapping/type1'
payload = '{  "properties": {"run_by": {"type": "text", "fielddata": true }}}'
headers = {'Content-Type': 'application/json'}
res = requests.put(url, data=payload, headers=headers)
print res
