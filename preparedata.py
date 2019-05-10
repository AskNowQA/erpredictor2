import sys, urllib2,json
from elasticsearch import Elasticsearch
from fuzzywuzzy import fuzz

f = open('lcquad.json')
s = f.read()
d = json.loads(s)
f.close()

es = Elasticsearch()

entpredarr = []

for item in d:
    for ent in item['entity mapping']:
        inputjson = {'phrase': ent['label']}
        req = urllib2.Request('http://localhost:8888/ftwv')
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(inputjson))
        response = json.loads(response.read())

        esresult = es.search(index="dbentityindex11", body={"query":{"multi_match":{"query":ent['label'],"fields":["wikidataLabel", "dbpediaLabel^1.5"]}},"size":1})
        topresult = esresult['hits']['hits']
        if len(topresult) == 1:
            topresult = topresult[0]
            if 'dbpediaLabel' in topresult['_source']:
                entpredarr.append({'label':ent['label'],'embedding':response,'class':'entity', 'esscore': float(topresult['_score']), 'fuzzratio': fuzz.ratio(ent['label'], topresult['_source']['dbpediaLabel']),'fuzzpartialratio': fuzz.partial_ratio(ent['label'], topresult['_source']['dbpediaLabel']), 'fuzztokensortratio': fuzz.token_sort_ratio(ent['label'], topresult['_source']['dbpediaLabel']), 'eslabel': topresult['_source']['dbpediaLabel']})
            if 'wikidataLabel' in topresult['_source']:
                entpredarr.append({'label':ent['label'],'embedding':response,'class':'entity', 'esscore': float(topresult['_score']), 'fuzzratio': fuzz.ratio(ent['label'], topresult['_source']['wikidataLabel']),'fuzzpartialratio': fuzz.partial_ratio(ent['label'], topresult['_source']['wikidataLabel']), 'fuzztokensortratio': fuzz.token_sort_ratio(ent['label'], topresult['_source']['wikidataLabel']), 'eslabel': topresult['_source']['wikidataLabel']})
        else:
            entpredarr.append({'label':ent['label'],'embedding':response,'class':'entity', 'esscore': 0, 'fuzzratio': 0,'fuzzpartialratio': 0, 'fuzztokensortratio': 0, 'eslabel': ''})

        if ent['label'].lower() != ent['label']:
            inputjson = {'phrase': ent['label'].lower()}       
            req = urllib2.Request('http://localhost:8888/ftwv')
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(inputjson))
            response = json.loads(response.read())

            esresult = es.search(index="dbentityindex11", body={"query":{"multi_match":{"query":ent['label'].lower(),"fields":["wikidataLabel", "dbpediaLabel^1.5"]}},"size":1})
            topresult = esresult['hits']['hits']
            if len(topresult) == 1:
                topresult = topresult[0]
                if 'dbpediaLabel' in topresult['_source']:
                    entpredarr.append({'label':ent['label'].lower(),'embedding':response,'class':'entity', 'esscore': float(topresult['_score']), 'fuzzratio': fuzz.ratio(ent['label'].lower(), topresult['_source']['dbpediaLabel']),'fuzzpartialratio': fuzz.partial_ratio(ent['label'].lower(), topresult['_source']['dbpediaLabel']), 'fuzztokensortratio': fuzz.token_sort_ratio(ent['label'].lower(), topresult['_source']['dbpediaLabel']), 'eslabel': topresult['_source']['dbpediaLabel']})
                if 'wikidataLabel' in topresult['_source']:
                    entpredarr.append({'label':ent['label'].lower(),'embedding':response,'class':'entity', 'esscore': float(topresult['_score']), 'fuzzratio': fuzz.ratio(ent['label'].lower(), topresult['_source']['wikidataLabel']),'fuzzpartialratio': fuzz.partial_ratio(ent['label'].lower(), topresult['_source']['wikidataLabel']), 'fuzztokensortratio': fuzz.token_sort_ratio(ent['label'].lower(), topresult['_source']['wikidataLabel']), 'eslabel': topresult['_source']['wikidataLabel']})
            else:
                entpredarr.append({'label':ent['label'].lower(),'embedding':response,'class':'entity', 'esscore': 0, 'fuzzratio': 0,'fuzzpartialratio': 0, 'fuzztokensortratio': 0, 'eslabel': ''})

    for pred in item['predicate mapping']:
        inputjson = {'phrase': pred['label']}
        req = urllib2.Request('http://localhost:8888/ftwv')
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(inputjson))
        response = json.loads(response.read())

        esresult = es.search(index="dbentityindex11", body={"query":{"multi_match":{"query":pred['label'],"fields":["wikidataLabel", "dbpediaLabel^1.5"]}},"size":1})
        topresult = esresult['hits']['hits']
        if len(topresult) == 1:
            topresult = topresult[0]
            if 'dbpediaLabel' in topresult['_source']:
                entpredarr.append({'label':pred['label'],'embedding':response,'class':'entity', 'esscore': float(topresult['_score']), 'fuzzratio': fuzz.ratio(pred['label'], topresult['_source']['dbpediaLabel']),'fuzzpartialratio': fuzz.partial_ratio(pred['label'], topresult['_source']['dbpediaLabel']), 'fuzztokensortratio': fuzz.token_sort_ratio(pred['label'], topresult['_source']['dbpediaLabel']), 'eslabel': topresult['_source']['dbpediaLabel']})
            if 'wikidataLabel' in topresult['_source']:
                entpredarr.append({'label':pred['label'],'embedding':response,'class':'entity', 'esscore': float(topresult['_score']), 'fuzzratio': fuzz.ratio(pred['label'], topresult['_source']['wikidataLabel']),'fuzzpartialratio': fuzz.partial_ratio(pred['label'], topresult['_source']['wikidataLabel']), 'fuzztokensortratio': fuzz.token_sort_ratio(pred['label'], topresult['_source']['wikidataLabel']), 'eslabel': topresult['_source']['wikidataLabel']})
        else:
            entpredarr.append({'label':pred['label'],'embedding':response,'class':'entity', 'esscore': 0, 'fuzzratio': 0,'fuzzpartialratio': 0, 'fuzztokensortratio': 0, 'eslabel': ''})


        if pred['label'].lower() != pred['label']:
            inputjson = {'phrase': pred['label'].lower()}
            req = urllib2.Request('http://localhost:8888/ftwv')
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(inputjson))
            response = json.loads(response.read())
            esresult = es.search(index="dbentityindex11", body={"query":{"multi_match":{"query":pred['label'].lower(),"fields":["wikidataLabel", "dbpediaLabel^1.5"]}},"size":1})
            topresult = esresult['hits']['hits']
            if len(topresult) == 1:
                topresult = topresult[0]
                if 'dbpediaLabel' in topresult['_source']:
                    entpredarr.append({'label':pred['label'].lower(),'embedding':response,'class':'entity', 'esscore': float(topresult['_score']), 'fuzzratio': fuzz.ratio(pred['label'].lower(), topresult['_source']['dbpediaLabel']),'fuzzpartialratio': fuzz.partial_ratio(pred['label'].lower(), topresult['_source']['dbpediaLabel']), 'fuzztokensortratio': fuzz.token_sort_ratio(pred['label'].lower(), topresult['_source']['dbpediaLabel']), 'eslabel': topresult['_source']['dbpediaLabel']})
                if 'wikidataLabel' in topresult['_source']:
                    entpredarr.append({'label':pred['label'].lower(),'embedding':response,'class':'entity', 'esscore': float(topresult['_score']), 'fuzzratio': fuzz.ratio(pred['label'].lower(), topresult['_source']['wikidataLabel']),'fuzzpartialratio': fuzz.partial_ratio(pred['label'].lower(), topresult['_source']['wikidataLabel']), 'fuzztokensortratio': fuzz.token_sort_ratio(pred['label'].lower(), topresult['_source']['wikidataLabel']), 'eslabel': topresult['_source']['wikidataLabel']})
            else:
                entpredarr.append({'label':pred['label'].lower(),'embedding':response,'class':'entity', 'esscore': 0, 'fuzzratio': 0,'fuzzpartialratio': 0, 'fuzztokensortratio': 0, 'eslabel': ''})
       
f = open('traintest.json','w')
f.write(json.dumps(entpredarr))
f.close() 
