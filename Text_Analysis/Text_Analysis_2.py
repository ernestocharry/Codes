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

File1 = '/Users/Feliche/Documents/Codes/Text_Analysis/Main.csv'
File2 = '/Users/Feliche/Documents/Codes/Text_Analysis/Y.csv'
File3 = '/Users/Feliche/Documents/Codes/Text_Analysis/InfoAudiolibrosAmazon-BestSellers.csv'

Main = pd.read_csv(File1)
Y = pd.read_csv(File2)
InfoBest = pd.read_csv(File3, skiprows=[0,1])

print(InfoBest.columns)

def check(sentence, words):
    res = [all([k in s for k in words]) for s in sentence]
    return [sentence[i] for i in range(0, len(res)) if res[i]]

for i in range(0, len(InfoBest)):
    print(i)
    Text1 =  InfoBest['TÍTULO'][i].lower().split()
    print(Text1)
    Main['name_2']  = Main['Name'].apply(lambda x: check(x.lower().split(), Text1))
