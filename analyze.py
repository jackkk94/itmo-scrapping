from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError 
import csv

from wordcloud import WordCloud
import matplotlib.pyplot as plt

import nltk
from nltk.probability import FreqDist

from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk import word_tokenize

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def getTagsByText(text):
    text_tokens = word_tokenize(text)
    words=[word.lower() for word in text_tokens  if word.isalpha()]
    for word in words:
        if word in stopwords.words("russian") or word in stopwords.words("english"):
            words.remove(word)

    data = nltk.Text(words)
    return FreqDist(data)


with open('parsed.csv', mode="r",  errors='replace') as File:  
    file = csv.reader(File, delimiter = ";", lineterminator="\n")
    count = 0
    for row in file:
        count+=1
        if(count>2):
            tags = getTagsByText(row[5])
            text_raw = " ".join(tags)
            wordcloud = WordCloud().generate(text_raw)
            wordcloud.to_file('./tags/raw_'+str(count)+'.png')
