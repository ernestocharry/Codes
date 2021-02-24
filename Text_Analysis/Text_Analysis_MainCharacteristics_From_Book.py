# Getting the main characteristics of the .txt books from a folder
# Autor: Félix Ernesto Charry Pastrana
# email: charrypastranaernesto@gmail.com
# Date started: 2021 02 15
'''
This code will find the distribution of the length.
'''
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

def FuntionFrequencyDistribution(NombreLista, MaxPalabrasRepetidas, Guardar, AditionalName=''):
    fdist = FreqDist(NombreLista)
    Max_Repeted_Words = MaxPalabrasRepetidas

    if(Guardar == True):
        FileName_FreqDis = 'FreqDist_' + Book_Name + '_'
        FileName_FreqDis = FileName_FreqDis + str(MaxPalabrasRepetidas) + '_'
        FileName_FreqDis = FileName_FreqDis + AditionalName +'.png'

        plt.ion()
        fdist.plot(Max_Repeted_Words,cumulative=False)
        plt.title(Book_Name+' '+AditionalName+' '+str(MaxPalabrasRepetidas))
        plt.savefig(Folder_Graphs+FileName_FreqDis, bbox_inches = "tight")
        plt.ioff()
    else:
        fdist.plot(Max_Repeted_Words,cumulative=False)

    plt.show()

    return;

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
      if t.parent.name not in blacklist:
        output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext

blacklist = [   '[document]',   'noscript', 'header',   'html', 'meta', 'head','input', 'script'   ]

epubFolder = '/Users/Feliche/Documents/AmazonBestSellers/'
all_epubs  = glob.glob(epubFolder+"*.epub")

Main = pd.DataFrame(columns=['Name'])
TAG  = pd.DataFrame()
Max_Counts_TAG = 20
Y = pd.DataFrame()

#for j in range(0, len(all_epubs)):
for j in range(0, 30):
    print(j)
    Text = epub2text(all_epubs[j])
    Text = ''.join(Text)

    Text = re.sub('\n', ' ', Text.lower())
    tokenized_sent=sent_tokenize(Text)

    # En pdSentencesLength se guardará las oraciones y su longitud
    pdSentencesLength = pd.DataFrame({'Sentences':tokenized_sent})
    pdSentencesLength['Length'] = pdSentencesLength['Sentences'].apply(lambda x: len(word_tokenize(x)))

    # Audiobooks
    #Name_of_Book = re.findall(r"/+[\w]+[.]+epub",all_epubs[j])[0][1:]
    Name_of_Book = all_epubs[j]
    Main.loc[j, 'Name'] = Name_of_Book
    Main.loc[j, 'length_words_total']=pdSentencesLength['Length'].sum()
    Main.loc[j, 'number_of_sentences_total'] = float(pd.DataFrame(pdSentencesLength.describe()).loc['count'])
    Main.loc[j, 'words_per_sentences_mean'] = round(float(pd.DataFrame(pdSentencesLength.describe()).loc['mean']),2)
    Main.loc[j, 'words_per_sentences_std'] = round(float(pd.DataFrame(pdSentencesLength.describe()).loc['std']),2)
    Main.loc[j, 'words_per_sentences_min'] = float(pd.DataFrame(pdSentencesLength.describe()).loc['min'])
    Main.loc[j, 'words_per_sentences_max'] = float(pd.DataFrame(pdSentencesLength.describe()).loc['max'])

    # Part Of Speech Tagging -------------------------------------------------------
    # The primary target of Part-of-Speech(POS) tagging is to identify the
    # grammatical group of a given word.
    # Whether it is a NOUN, PRONOUN, ADJECTIVE, VERB, ADVERBS, etc.
    # based on the context. POS Tagging looks for relationships within the sentence
    # and assigns a corresponding tag to the word.


    All_tag = nltk.pos_tag(word_tokenize(Text))
    # Verb: past tense and past participle
    Verb    = [a for (a, b) in All_tag if b in ['VBD', 'VBN'] ]
    Total_verb_past = len(Verb)

    # Verb: past tense and past participle
    Verb_present    = [a for (a, b) in All_tag if b in ['VBG', 'VBP', 'VBZ'] ]
    Total_verb_present = len(Verb_present)

    Foreign_Words = [a for (a, b) in All_tag if b == 'FW' ]
    Noun    = [a for (a, b) in All_tag if b in ['NN', 'NNS', 'NNP', 'NNPS'] ]


    All_tag = nltk.pos_tag(word_tokenize(Text), tagset='universal')
    Total_Verb = len([a for (a, b) in All_tag if b == 'VERB'])
    Num     = [a for (a, b) in All_tag if b == 'NUM']
    Pron    = [a for (a, b) in All_tag if b == 'PRON']
    Punct   = [a for (a, b) in All_tag if b == '.']

    #---------------------------------------------------------------------------
    Main.loc[j, 'Percentaje_Verb_Past']     = round(Total_verb_past*100/Total_Verb,0)
    Main.loc[j, 'Percentaje_Verb_Present']  = round(Total_verb_present*100/Total_Verb,0)
    Main.loc[j, 'Percentaje_Verb_Future']   = 100 - Main.loc[j, 'Percentaje_Verb_Past'] - Main.loc[j, 'Percentaje_Verb_Present']
    #---------------------------------------------------------------------------

    lem = WordNetLemmatizer()       # Lemmatization

    Verb_Lemma = []
    for i in range(0,len(Verb)):
        Verb_Lemma.append(lem.lemmatize(Verb[i],'v'))

    X0 = pd.DataFrame(Max_Counts_TAG*[Name_of_Book], columns=['Name'])

    fdist = FreqDist(Verb_Lemma)
    Total_No = len(Verb_Lemma)
    X1 = (pd.DataFrame(fdist.most_common(Max_Counts_TAG), columns = ['Verb', 'Verb_Counts']))
    X1['Verb_Counts_Percentaje'] = X1['Verb_Counts']*100/Total_No

    fdist = FreqDist(Noun)
    Total_No = len(Noun)
    X2 = (pd.DataFrame(fdist.most_common(Max_Counts_TAG), columns = ['Noun', 'Noun_Counts']))
    X2['Noun_Counts_Percentaje'] = X2['Noun_Counts']*100/Total_No

    fdist = FreqDist(Pron)
    Total_No = len(Pron)
    X3 = (pd.DataFrame(fdist.most_common(Max_Counts_TAG), columns = ['Pron', 'Pron_Counts']))
    X3['Pron_Counts_Percentaje'] = X3['Pron_Counts']*100/Total_No

    X = pd.concat([X0, X1, X2, X3], axis=1)
    X.fillna(0, inplace=True)

    Y = Y.append(X, ignore_index=True)



print('\n ----------------------------------------------------------------')
#print(pdFrequencyReference.iloc[91])
print(Main)
print(Main.columns)
print('\n ----------------------------------------------------------------')
print(Y.columns)
print('\n')

File1 = '/Users/Feliche/Documents/Codes/Text_Analysis/Main.csv'
File2 = '/Users/Feliche/Documents/Codes/Text_Analysis/Y.csv'
Main.to_csv(File1)
Y.to_csv(File2)
