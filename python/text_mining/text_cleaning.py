import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

nltk.download('stopwords')

df=pd.read_csv('../collect_data/project_text.tsv',sep='\t')
df['file_text']=df['file_text'].str.lower() #lowercase
df['file_textlen']=df['file_text'].apply(len)
df['file_text1']=df['file_text'].str.replace('[^\w\s]','') #removing punctuations
df['file_textlen1']=df['file_text1'].apply(len)
df['file_text2']=df['file_text1'].str.replace('[\d]','') #removing digits
#df['file_text2']=df['file_text2'].str.replace('  ','') #removing double spaces may not be needed
df['file_textlen2']=df['file_text2'].apply(len)
df['clean_text']=df['file_text2'].apply(wordpunct_tokenize) #tokenizer to split into words
df['clean_textlen']=df['clean_text'].apply(len)
stop_words=stopwords.words('english')
df['clean_text1']=df['clean_text'].apply(lambda x: [i for i in x if i not in stop_words]) #removing stop words
df['clean_textlen1']=df['clean_text1'].apply(len)
# df['clean_text2']=df['clean_text1'].apply(lambda x:list(dict.fromkeys(x))) #remove duplicates
# df['clean_textlen2']=df['clean_text2'].apply(len)

#print(df)

Newdf=df[['project_url','file_text','clean_text1']]
Newdf.rename(columns={'clean_text1': 'clean_text'},inplace=True)
Newdf.set_index('project_url',inplace=True)
#print(Newdf)
Newdf.to_csv('project_clean_text.tsv', sep='\t')
