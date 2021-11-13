import nltk
import pandas as pd
from nltk.corpus import stopwords
#nltk.download('stopwords')
from nltk.tokenize import wordpunct_tokenize
#from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

df=pd.read_csv('project_text.tsv',sep='\t')
df['file_text']=df['file_text'].str.lower() #lowercase
df['file_textlen']=df['file_text'].apply(len)
df['file_text1']=df['file_text'].str.replace('[^\w\s]',' ') #removing punctuations and replace with space to keep the text in links intact
df['file_textlen1']=df['file_text1'].apply(len)
df['file_text2']=df['file_text1'].str.replace('[\d]',' ') #removing digits and replace with space to prevent forming new words like b23ac67k will become back
df['file_textlen2']=df['file_text2'].apply(len)
df['clean_text']=df['file_text2'].apply(wordpunct_tokenize) #tokenizer to split into words
df['clean_textlen']=df['clean_text'].apply(len)
stop_words=stopwords.words('english')
df['clean_text1']=df['clean_text'].apply(lambda x: [i for i in x if i not in stop_words]) #removing stop words
df['clean_textlen1']=df['clean_text1'].apply(len)
ps=PorterStemmer()
#ps.stem('clusters')
df['clean_text2']=df['clean_text1'].apply(lambda x:[ps.stem(i) for i in x] ) #lemmatized

#df

Newdf=df[['project_url','file_text','clean_text2']]
Newdf.rename(columns={'clean_text2': 'clean_text'},inplace=True)
Newdf.set_index('project_url',inplace=True)
#print(Newdf)
Newdf.to_csv('project_clean_text.tsv', sep='\t')


#extra cleaning if needed
#df['file_text2']=df['file_text2'].str.replace('  ','') #removing double spaces may not be needed
#df['file_text3']=df['file_text2'].str.replace('http\w+\s+','') #removed words which start with http
# # df['clean_text2']=df['clean_text1'].apply(lambda x:list(dict.fromkeys(x))) #remove duplicates
# # df['clean_textlen2']=df['clean_text2'].apply(len)
# remove non english words -- but didn't work that well
# nltk.download('words')
# words = set(nltk.corpus.words.words())
# words
# df['clean_text2']=df['clean_text1'].apply(lambda x: [i for i in x if i not in words])
# df['clean_textlen2']=df['clean_text2'].apply(len)
# lemmatizer = WordNetLemmatizer()
# lemmatizer.lemmatize("clustering")
