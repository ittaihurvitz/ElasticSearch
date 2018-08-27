import json
# make sure ES is up and running
import requests
res = requests.get('http://localhost:9200')
print(res.content)

#connect to our cluster
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#print es.search(index="sw", body={"query": {"match": {'name':'Organa'}}})
#exit()

#index some test data
#es.index(index='test-index', doc_type='test', id=1, body={'test': 'test'})

##es.index(index='sw', doc_type='people', id=1, body={
##	"name": "Luke Skywalker",
##	"height": "172",
##	"mass": "77",
##	"hair_color": "blond",
##	"birth_year": "19BBY",
##	"gender": "male",
##})

##r = requests.get('http://localhost:9200')
##i = 1
###while (r.status_code == 200 and i<25):
##while i<25:
##    if i != 17:
##       r = requests.get('http://swapi.co/api/people/'+ str(i))
##       es.index(index='sw2', doc_type='people', id=i,     body=json.loads(r.content))
##    i=i+1

##for i in range(25, 35):
##    r = requests.get('http://swapi.co/api/people/'+ str(i))
##    es.index(index='sw2', doc_type='people', id=i,     body=json.loads(r.content))

    
##myJson = """
##{
##  "name": "test3 testing",
##  "url": "https://swapi.co/api/people/1/",
##  "height": "200",
##  "mass": "77",
##  "hair_color": "blond",
##  "skin_color": "fair",
##  "eye_color": "blue",
##  "birth_year": "19BBY",
##  "gender": "test",
##  "homeworld": "https://swapi.co/api/planets/1/",
##  "created": "2014-12-09T13:50:51.644000Z",
##  "edited": "2014-12-20T21:17:56.891000Z"
##}
##"""
##es.index(index='sw2', doc_type='people', id=102, body=json.loads(myJson))


#get the data
#print es.get(index='sw', doc_type='people', id=18)
#print es.get(index='test-index', doc_type='test', id=1)

#print es.search(index="sw", body={"query": {"match": {'gender':'male'}}})
#print es.search(index="sw", body={"query": {"match": {'name':'Skywalker'}}})

myJson = """
{
  "strange": "1234",
  "first_name": "test1",
  "last_name": "testing1",
  "created": "2017-10-09T13:50:51.644000Z",
  "edited": "2017-11-20T21:17:56.891000Z"
}
"""
es.index(index='test1_indx', doc_type='type1', body=json.loads(myJson))

print es.search(index="test1_indx", body={"query": {"match": {'first_name':'test2'}}})
