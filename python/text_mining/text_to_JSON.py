import json
import pandas as pd

data=pd.read_csv('AlgOutput.csv',header=None)
Topic=data[1].unique() #picking unique topic values from file
Tdict={} #Dictionary to hold all the topics, key-topic;values-sub dictionaries
#Topic=['Intelligent Browsing','Intelligent Learning Platform','System Extension','Leaderboard Competition','Free Topics']
FTopic=[] #List to hold the free topics

for t in Topic:
    llist=[] #list to hold multiple dictionaries for different links within one topic
    filein=open('AlgOutput.csv','r')
    for line in filein:
        ldict={} #Dictionary to hold the links, key - link;value - topic coverage
        lineNew=line.strip() #removing endline character
        words=lineNew.split(',') #splitting lines into words
        if t == words[1]: #index 1 is where Topic name is stored
            print(words[1])
            if words[1]=='Free Topics':
                if words[2] not in FTopic:
                    FTopic.append(words[2])
            else:
                ldict['url']=words[0]
                ldict['relevance']=words[3]
                llist.append(ldict)
    Tdict[t]=llist
print(FTopic)
Fdict={} #dictionary of subtopics under free topics, key - subtopic, value- sub dictionaries
for ft in FTopic:
    fllist=[] #list to hold multiple dictionaries for different links within one Free topic
    filein=open('AlgOutput.csv','r')
    for line in filein:
        fldict={} #Dictionary to hold the links for subtopics under Free topics, key - link, value - topic coverage
        lineNew=line.strip()
        words=lineNew.split(',')
        if ft==words[2]: #index 2 is where SubTopic name is stored
            fldict['url']=words[0]
            fldict['relevance']=words[3]
            fllist.append(fldict)
    Fdict[ft]=fllist
Tdict['Free Topics']=Fdict

print(Tdict)
#     print(lineNew)
#     print(words)

fileout=open('firebase-output.json','w')
json.dump(Tdict,fileout)
fileout.close()
