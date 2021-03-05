import nltk # Natural Languaje TollKit nltk.download() Download all!
import matplotlib.pyplot as plt
import glob # To know all the txt files in a folder
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import re # Removing \n
import pandas as pd
from nltk.corpus import stopwords

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.probability import FreqDist

base= '/Users/Feliche/Documents/Codes/Text_Analysis/'
base= '/Users/charrypastrana/Documents/Codes/Text_Analysis/'

File1 = base+'Main.csv'
File2 = base+'Y.csv'
File3 = base+'InfoAudiolibrosAmazon-BestSellers.csv'

Main = pd.read_csv(File1)
Y = pd.read_csv(File2)
InfoBest = pd.read_csv(File3, skiprows=[0,1])

print(Main.columns)
print(InfoBest.columns)
Main['title_to_merge'] = Main['title'].str.replace(' ', '').str.lower().str[0:10]
InfoBest['title_to_merge'] = InfoBest['TÍTULO'].str.replace(' ', '').str.lower().str[0:10]

Both = pd.merge(Main, InfoBest, how = 'inner', on='title_to_merge')

print(Both)

FileBoth = base +'Both.csv'
Both.to_csv(FileBoth, index=False)


'''
def check(sentence, words):
    res = [all([k in s for k in words]) for s in sentence]
    return [sentence[i] for i in range(0, len(res)) if res[i]]

for i in range(0, len(InfoBest)):
    print(i)
    Text1 =  InfoBest['TÍTULO'][i].lower().split()
    print(Text1)
    Main['name_2']  = Main['Name'].apply(lambda x: check(x.lower().split(), Text1))
'''
