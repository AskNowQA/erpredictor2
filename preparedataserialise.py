import sys,os,json,torch

f = open('traintest.json')
s = f.read()
d = json.loads(s)

alldata = []

for item in d:
    if item['class']=='entity':
        xy = item['embedding'] + [item['esscore']] + [item['fuzzratio']] + [item['fuzzpartialratio']] + [item['fuzztokensortratio']] + [0]
        alldata.append(xy)
    else:
        xy = item['embedding'] + [item['esscore']] + [item['fuzzratio']] + [item['fuzzpartialratio']] + [item['fuzztokensortratio']] + [1]
        print "pred"
        alldata.append(xy)

tensor = torch.FloatTensor(alldata)
torch.save(tensor,'traintest.pt')
