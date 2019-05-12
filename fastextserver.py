#!/usr/bin/python

from sets import Set
from flask import request
from flask import Flask
from gevent.pywsgi import WSGIServer
import numpy as np
import json,sys
from gensim.models import FastText

import gensim.downloader as api
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

print "Fastext server initializing"
try:
    model = api.load('fasttext-wiki-news-subwords-300')
except Exception,e:
    print e
    sys.exit(1)            
print "Fastext initialized"

def ConvertVectorSetToVecAverageBased(vectorSet, ignore = []):
    if len(ignore) == 0:
        return np.mean(vectorSet, axis = 0)
    else:
        return np.dot(np.transpose(vectorSet),ignore)/sum(ignore)


@app.route('/ftwv', methods=['POST'])
def ftwv():
    d = request.get_json(silent=True)
    phrase_ = d['phrase']
    print phrase_
    phrase =  phrase_.split(" ")
    vw_phrase = []
    for word in phrase:
        try:
            vw_phrase.append(model.word_vec(word))
        except Exception,e:
            continue
    if len(vw_phrase) == 0:
        return json.dumps(300*[0])
    v_phrase = ConvertVectorSetToVecAverageBased(vw_phrase)
    return json.dumps(v_phrase.tolist()) 

if __name__ == '__main__':
    http_server = WSGIServer(('', int(sys.argv[1])), app)
    http_server.serve_forever()
                          
                     


#if __name__ == '__main__':
#    t = TextMatch()
    #print t.textMatch([{'chunk': 'Who', 'surfacelength': 3, 'class': 'entity', 'surfacestart': 0}, {'chunk': 'the parent organisation', 'surfacelength': 23, 'class': 'relation', 'surfacestart': 7}, {'chunk': 'Barack Obama', 'surfacelength': 12, 'class': 'entity', 'surfacestart': 34}, {'chunk': 'is', 'surfacelength': 2, 'class': 'relation', 'surfacestart': 4}])
#    print t.textMatch([{"chunk": "India", "surfacelength": 5, "class": "entity", "surfacestart": 0}])
