import os
import re
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import WordNetLemmatizer
import threading
import time

done = False
def animate():
    bar = [
        " [=     ]",
        " [ =    ]",
        " [  =   ]",
        " [   =  ]",
        " [    = ]",
        " [     =]",
        " [    = ]",
        " [   =  ]",
        " [  =   ]",
        " [ =    ]",
    ]
    i = 0

    while not done:
        print("Cleaning Text Data", bar[i % len(bar)], end="\r")
        time.sleep(.2)
        i += 1

t = threading.Thread(target=animate)
t.start()

# Set current working directory to the folder the script is in
script_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
os.chdir(script_dir)

#pulling in list of high usage words
highusage_words=[]
fh=open('highusage_words.txt','r')
for line in fh:
    line=line.strip()
    highusage_words.append(line)
fh.close()

df=pd.read_csv('../collect_data/project_text.tsv',sep='\t')

df['file_text']=df['file_text'].str.lower() #lowercase
df['file_textlen']=df['file_text'].apply(len)

df['file_text1']=df['file_text'].str.replace('[^\w\s]',' ',regex=True) #removing punctuations and replace with space to keep the text in links intact
df['file_text2']=df['file_text1'].str.replace('[\d]',' ',regex=True) #removing digits and replace with space to prevent forming new words like b23ac67k will become back
df['file_textlen1']=df['file_text2'].apply(len)

df['clean_text']=df['file_text2'].apply(wordpunct_tokenize) #tokenizer to split into words
df['clean_textlen']=df['clean_text'].apply(len)

lemmatizer = WordNetLemmatizer()

df['clean_text1']=df['clean_text'].apply(lambda x:[lemmatizer.lemmatize(i) for i in x] ) #lemmatize

stop_words=stopwords.words('english')
df['clean_text2']=df['clean_text1'].apply(lambda x: [i for i in x if i not in stop_words]) #removing stop words
df['clean_textlen2']=df['clean_text2'].apply(len)

df['clean_text3']=df['clean_text2'].apply(lambda x: [i for i in x if len(i) >2]) #removing any word that is less than 3 letters
df['clean_textlen3']=df['clean_text3'].apply(len)

df['clean_text4']=df['clean_text3'].apply(lambda x: [i for i in x if i not in highusage_words]) #removing high usage words
df['clean_textlen4']=df['clean_text4'].apply(len)

# Remove underscores at the ends of tokens. This changes "twitter_" to "twitter".
df['clean_text5']=df['clean_text4'].apply(lambda x: [re.sub(r'_$', '', i) for i in x])
df['clean_textlen5']=df['clean_text5'].apply(len)

#df

Newdf=df[['project_url','file_text','clean_text5']]
Newdf.rename(columns={'clean_text5': 'clean_text'},inplace=True)
Newdf.set_index('project_url',inplace=True)

Newdf.to_csv('project_clean_text.tsv', sep='\t')

done = True