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
import gensim
import gensim.corpora as corpora

# Convert file from a string as we are reading from .tsv
from ast import literal_eval 
df=pd.read_csv('project_clean_text.tsv',sep='\t',converters={'clean_text': literal_eval})

# Creating a mega list of each mega document's cleaned up tokens
megalist=[]
for i in range (len(df)):
    megalist.append(df['clean_text'][i])

# Creating a dictionary from the list of lists
dictionary=corpora.Dictionary(megalist) 

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

# Dictionary to capture the word distribution per topic
topic_word_dict={} 
topics = lda_model.print_topics(num_words=10)
for topic in topics:
    topic_word_dict[topic[0]]=topic[1]

# Dictionary to capture the topic distribution per mega document
doc_topic_dist_dict={} 
count=0
for i in lda_model[doc_term_matrix]:
    doc_topic_dist_dict[count]=i
    count+=1

# Dictionary to capture the highest probability topic per mega document
doc_topic_dist_final_dict={} 
for url in range(len(df)):
    distribution=doc_topic_dist_dict[url]
    prob_dict={}
    for i in distribution:
        prob_dict[i[0]]=(i[1])
    doc_topic_dist_final_dict[url]=max(prob_dict, key=prob_dict.get)

# Dictionary to capture the words from the highest probability topic per mega document
doc_topic_final_dict={} 
for url in range(len(df)):
    doc_topic_final_dict[url]=topic_word_dict[doc_topic_dist_final_dict[url]]

# Creating a new column as a clone of an existing one just as a placeholder
df['Topics']=df['clean_text'] 
for url in range(len(df)):
    # Assigning each row of the new column the captured words from the topic with hihgest prob
    df['Topics'][url]=doc_topic_final_dict[url] 

# Cleaning up the new column and tokenize
df['Topics1']=df['Topics'].str.replace('[^\w\s]',' ')
df['Topics2']=df['Topics1'].str.replace('[\d]',' ')
df['Topics3']=df['Topics2'].apply(wordpunct_tokenize)

Newdf=df[['project_url','file_text','clean_text','Topics3']]
Newdf.rename(columns={'Topics3': 'Topics'},inplace=True)
Newdf.set_index('project_url',inplace=True)
Newdf.to_csv('AlgOutput.tsv', sep='\t')

# Finally, generate JSON for the web app to consume.
algoutput_df=pd.read_csv('AlgOutput.tsv',sep='\t')

#Dictionary to hold all the topics
topic_dict={} 
for i in range(len(df)):
    # Dictionary to hold one url at a time
    url_dict={} 
    url_dict['url']=algoutput_df['project_url'][i]
    url_dict['tags']=json.loads(algoutput_df['Topics'][i].replace("'", '"'))
    topic_dict[i]=url_dict

fileout=open('firebase-output.json','w')
json.dump(topic_dict,fileout)
fileout.close()

