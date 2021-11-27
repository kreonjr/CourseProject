# Take cleaned text of CS 410 course projects and generate an LDA topic model.
# Output the dominant project for each topic to tab-separated and JSON files.
# The Team Topic Thunder web app will consume the JSON.
#
# NOTE: To generate LDA topic model, use the same settings as the optimal model
# in the model_eval/topic_model_eval Jupyter notebook.
# Alternatively, can just load the saved model from the saved_model subfolder.

from nltk.tokenize import wordpunct_tokenize
import pandas as pd
import json
#! pip install --upgrade gensim
import gensim
import gensim.corpora as corpora
from ast import literal_eval #to convert file from a string as we are reading from .tsv

df=pd.read_csv('project_clean_text.tsv',sep='\t',converters={'clean_text': literal_eval})
#,converters={'clean_text': pd.eval})
#df

#Creating a mega list of each mega document's cleaned up tokens
megalist=[]
for i in range (len(df)):
    megalist.append(df['clean_text'][i])
# megalist
# len(megalist)

dictionary=corpora.Dictionary(megalist) # creating a dictionary from the list of lists

# Term Document Frequency
doc_term_matrix = [dictionary.doc2bow(doc, allow_update=True) for doc in megalist]

lda_model = gensim.models.ldamodel.LdaModel(corpus=doc_term_matrix,
                                           id2word=dictionary,
                                           num_topics=12,
                                           random_state=100,
                                           passes=10,
                                           iterations=50,
                                           alpha='auto'
                                           )

topic_word_dict={} #dictionary to capture the word distribution per topic
topics = lda_model.print_topics(num_words=10)
for topic in topics:
    #print(topic)
    topic_word_dict[topic[0]]=topic[1]
#topic_word_dict

doc_topic_dist_dict={} #dictionary to capture the topic distribution per mega document
count=0
for i in lda_model[doc_term_matrix]:
    #print('doc:',count,i)
    doc_topic_dist_dict[count]=i
    count+=1
#doc_topic_dist_dict

doc_topic_dist_final_dict={} #dictionary to capture the highest probability topic per mega document
for url in range(len(df)):
    distribution=doc_topic_dist_dict[url]
    prob_dict={}
    for i in distribution:
        prob_dict[i[0]]=(i[1])
    doc_topic_dist_final_dict[url]=max(prob_dict, key=prob_dict.get)
#doc_topic_dist_final_dict

doc_topic_final_dict={} #dictionary to capture the words from the highest probability topic per mega document
for url in range(len(df)):
    doc_topic_final_dict[url]=topic_word_dict[doc_topic_dist_final_dict[url]]
#doc_topic_final_dict

df['Topics']=df['clean_text'] #creating a new column as a clone of an existing one just as a placeholder
for url in range(len(df)):
    df['Topics'][url]=doc_topic_final_dict[url] #assigning each row of the new column the captured words from the topic with hihgest prob

#cleaning up the new column and tokenize
df['Topics1']=df['Topics'].str.replace('[^\w\s]',' ')
df['Topics2']=df['Topics1'].str.replace('[\d]',' ')
df['Topics3']=df['Topics2'].apply(wordpunct_tokenize)

Newdf=df[['project_url','file_text','clean_text','Topics3']]
Newdf.rename(columns={'Topics3': 'Topics'},inplace=True)
Newdf.set_index('project_url',inplace=True)
#print(Newdf)
Newdf.to_csv('AlgOutput.tsv', sep='\t')

# Finally, generate JSON for the web app to consume.

algoutput_df=pd.read_csv('AlgOutput.tsv',sep='\t')
#data['Topics']
#pd.Series(data.Topics.values,index=data.project_url).to_dict()
topic_dict={} #Dictionary to hold all the topics
for i in range(len(df)):
    url_dict={} #dictionary to hold one url at a time
    url_dict['url']=algoutput_df['project_url'][i]
    url_dict['tags']=json.loads(algoutput_df['Topics'][i].replace("'", '"'))
    topic_dict[i]=url_dict

#topic_dict

fileout=open('firebase-output.json','w')
json.dump(topic_dict,fileout)
fileout.close()

