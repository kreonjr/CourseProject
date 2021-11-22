import json
import pandas as pd

df=pd.read_csv('AlgOutput.tsv',sep='\t')
#data['Topics']
#pd.Series(data.Topics.values,index=data.project_url).to_dict()
topic_dict={} #Dictionary to hold all the topics
for i in range(len(df)):
    url_dict={} #dictionary to hold one url at a time
    url_dict['url']=df['project_url'][i]
    url_dict['tags']=json.loads(df['Topics'][i].replace("'", '"'))
    topic_dict[i]=url_dict

#topic_dict

fileout=open('firebase-output.json','w')
json.dump(topic_dict,fileout)
fileout.close()
