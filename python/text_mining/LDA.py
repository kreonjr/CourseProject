import nltk
import pandas as pd
#! pip install --upgrade gensim
import gensim
import gensim.corpora as corpora
from ast import literal_eval #to convert file from a string as we are reading from .tsv

df=pd.read_csv('project_clean_text.tsv',sep='\t',converters={'clean_text': literal_eval})
#,converters={'clean_text': pd.eval})
#df

words=df['clean_text'][0] # picking only first document's cleaned text for trial
#creating sub lists from the big list cause gensim seems to want the input that way
final=[]
for i in range(0, len(words), 10):
    final.append(words[i:i + 10])
#final

id2word=corpora.Dictionary(final) # creating a dictionary from the list of lists
#print(id2word.token2id) #to see the dictionary
# Term Document Frequency
corpus = [id2word.doc2bow(doc, allow_update=True) for doc in final]

# human readbale form of the term document freq
#[[(id2word[id], freq) for id, freq in cp] for cp in mycorpus]

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=10
                                           )
from pprint import pprint
pprint(lda_model.print_topics())
#doc_lda = lda_model[corpus] #not sure what this does
