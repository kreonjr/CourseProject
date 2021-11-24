import pandas as pd
from nltk.corpus import stopwords
#nltk.download('stopwords')
#from nltk.tokenize import sent_tokenize
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import WordNetLemmatizer
#from nltk.stem import PorterStemmer

#pulling in list of high usage words
highusage_words=[]
fh=open('highusage_words.txt','r')
for line in fh:
    line=line.strip()
    highusage_words.append(line)
#print(highusage_words)

df=pd.read_csv('../collect_data/project_text.tsv',sep='\t')

df['file_text']=df['file_text'].str.lower() #lowercase
df['file_textlen']=df['file_text'].apply(len)

df['file_text1']=df['file_text'].str.replace('[^\w\s]',' ') #removing punctuations and replace with space to keep the text in links intact
df['file_text2']=df['file_text1'].str.replace('[\d]',' ') #removing digits and replace with space to prevent forming new words like b23ac67k will become back
df['file_textlen1']=df['file_text2'].apply(len)

df['clean_text']=df['file_text2'].apply(wordpunct_tokenize) #tokenizer to split into words
df['clean_textlen']=df['clean_text'].apply(len)

lemmatizer = WordNetLemmatizer()
# lemmatizer.lemmatize("clustering")
df['clean_text1']=df['clean_text'].apply(lambda x:[lemmatizer.lemmatize(i) for i in x] ) #lemmatize

stop_words=stopwords.words('english')
df['clean_text2']=df['clean_text1'].apply(lambda x: [i for i in x if i not in stop_words]) #removing stop words
df['clean_textlen2']=df['clean_text2'].apply(len)

df['clean_text3']=df['clean_text2'].apply(lambda x: [i for i in x if len(i) >2]) #removing any word that is less than 3 letters
df['clean_textlen3']=df['clean_text3'].apply(len)

df['clean_text4']=df['clean_text3'].apply(lambda x: [i for i in x if i not in highusage_words]) #removing high usage words
df['clean_textlen4']=df['clean_text4'].apply(len)

#df

Newdf=df[['project_url','file_text','clean_text4']]
Newdf.rename(columns={'clean_text4': 'clean_text'},inplace=True)
Newdf.set_index('project_url',inplace=True)
#print(Newdf)
Newdf.to_csv('project_clean_text.tsv', sep='\t')


#extra cleaning if needed
#df['file_text2']=df['file_text2'].str.replace('  ','') #removing double spaces may not be needed
# # df['clean_text2']=df['clean_text1'].apply(lambda x:list(dict.fromkeys(x))) #remove duplicates
# # df['clean_textlen2']=df['clean_text2'].apply(len)
# remove non english words -- but didn't work that well
# nltk.download('words')
# words = set(nltk.corpus.words.words())
# words
# df['clean_text2']=df['clean_text1'].apply(lambda x: [i for i in x if i not in words])
# df['clean_textlen2']=df['clean_text2'].apply(len)

#ps=PorterStemmer()
#ps.stem('clusters')
#df['clean_text3']=df['clean_text2'].apply(lambda x:[ps.stem(i) for i in x] ) #stemming
# df['clean_textlen2']=df['clean_text2'].apply(len)
# df['new']=df['file_text2'].apply(lambda x:nltk.pos_tag(x))
# df
