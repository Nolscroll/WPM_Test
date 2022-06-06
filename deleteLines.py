import json

with open("quotes.json", "r") as infile:
    jsonDict = json.load(infile)

newList = []
for i in jsonDict["quotes"]:
    if len(i["quote"].strip()) <= 79:
        newList.append(i)

newJson = {"quotes" : newList}
with open('singleLineQuotes.json', 'w') as outfile:
    json.dump(newJson, outfile)