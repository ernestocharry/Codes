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

Folder_Main     = '/Users/Feliche/Documents/Codes/'
Folder_Main     = '/Users/charrypastrana/Documents/Codes/'
Folder_Main     = Folder_Main + 'Text_Analysis/'

Folder_Books    = Folder_Main + 'Audiolibros/'
Folder_Graphs   = Folder_Main + 'Graphs/'

all_books  = glob.glob(Folder_Books+"*.txt")
Longitud_Folder_Books = len(Folder_Books)
print('\n Se analizaran ',len(all_books),' libros from the folder',Folder_Books)

LongitudMax = 800
print('\n La longitud máxima de las oraciones analizadas será ', LongitudMax)

pdFrequencyReference = pd.DataFrame({'Length':range(1,LongitudMax+1)})

# Audiobooks
Main = pd.DataFrame(columns=['Name'])
TAG  = pd.DataFrame()
Max_Counts_TAG = 20

import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.probability import FreqDist

Y = pd.DataFrame()
for j in range(0, len(all_books)):
    Book_Name = all_books[j][Longitud_Folder_Books:len(all_books[j])]
    print('\n ----------------------------------------------------------------')
    print('\n j: ', j,'\t Book Analized: ', Book_Name)

    File_Name   = open(all_books[j],'r')
    Text        = File_Name.read()
    Text = re.sub('\n', ' ', Text)
    tokenized_sent=sent_tokenize(Text)

    # En pdSentencesLength se guardará las oraciones y su longitud
    pdSentencesLength = pd.DataFrame({'Sentences':tokenized_sent})
    pdSentencesLength['Length'] = pdSentencesLength['Sentences'].apply(lambda x: len(word_tokenize(x)))

    # Audiobooks
    Name_of_Book = re.findall(r"/+[\w]+[.]+txt",all_books[j])[0][1:]
    Main.loc[j, 'Name'] = Name_of_Book
    Main.loc[j, 'length_words_total']=pdSentencesLength['Length'].sum()
    Main.loc[j, 'number_of_sentences_total'] = float(pd.DataFrame(pdSentencesLength.describe()).loc['count'])
    Main.loc[j, 'words_per_sentences_mean'] = float(pd.DataFrame(pdSentencesLength.describe()).loc['mean'])
    Main.loc[j, 'words_per_sentences_std'] = float(pd.DataFrame(pdSentencesLength.describe()).loc['std'])
    Main.loc[j, 'words_per_sentences_min'] = float(pd.DataFrame(pdSentencesLength.describe()).loc['min'])
    Main.loc[j, 'words_per_sentences_max'] = float(pd.DataFrame(pdSentencesLength.describe()).loc['max'])

    # Part Of Speech Tagging -------------------------------------------------------
    # The primary target of Part-of-Speech(POS) tagging is to identify the
    # grammatical group of a given word.
    # Whether it is a NOUN, PRONOUN, ADJECTIVE, VERB, ADVERBS, etc.
    # based on the context. POS Tagging looks for relationships within the sentence
    # and assigns a corresponding tag to the word.

    All_tag = nltk.pos_tag(word_tokenize(Text), tagset='universal')

    Verb    = [a for (a, b) in All_tag if b == 'VERB']
    print(Verb[:10])
    Noun    = [a for (a, b) in All_tag if b == 'NOUN']
    Num     = [a for (a, b) in All_tag if b == 'NUM']
    Pron    = [a for (a, b) in All_tag if b == 'PRON']
    Punct   = [a for (a, b) in All_tag if b == '.']

    lem = WordNetLemmatizer()       # Lemmatization

    Verb_Lemma = []
    for i in range(0,len(Verb)):
        Verb_Lemma.append(lem.lemmatize(Verb[i],'v'))
    print(Verb_Lemma[:10])
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
print(Main.columns)
print('\n ----------------------------------------------------------------')
print(Y.columns)
print('\n')

'''
    # Contando la frencuencia de las longitudes de las sentencias de
    # pdSentencesLength y convertiendola en Pandas
    a = list(pdSentencesLength['Length'])
    d = {x:a.count(x) for x in a}

    pdFrequency     = pd.DataFrame(d.keys())
    pdFrequency.rename(columns = {list(pdFrequency)[0]:'Length'}, inplace = True)
    Nombre = 'Freq_Book_' + str(j)
    pdFrequency[Nombre] = pd.DataFrame(d.values())
    pdFrequency.sort_values(by='Length', inplace = True)

    pdFrequencyReference = pdFrequencyReference.merge(pdFrequency, how='left')
    pdFrequencyReference[Nombre].fillna(0, inplace=True)
    SumaDeFrequencies = pdFrequencyReference[Nombre].sum()
    pdFrequencyReference[Nombre] = pdFrequencyReference[Nombre]*100/SumaDeFrequencies

    # Plot each result
    AditionalName = '2021-02-15-'
    FileName_FreqDis = 'Frequency_LengthSentences_' + Book_Name + '_'
    FileName_FreqDis = FileName_FreqDis +  '_'
    FileName_FreqDis = FileName_FreqDis + AditionalName +'.png'

    #plt.ion()
    #pdFrequencyReference.plot(x = 'Length', y = Nombre, style = '-', xlim = [1,LongitudMax], ylim = [0,2], label = Book_Name)
    #plt.savefig(Folder_Graphs+FileName_FreqDis, bbox_inches = "tight")
    #plt.ioff()

    # Stopwords --------------------------------------------------------------------
    # Stopwords considered as noise in the text.
    # Text may contain stop words such as is, am, are, this, a, an, the, etc.

    # Standar Stopwords
    stop_words=set(stopwords.words("english"))
    # Manually Stopwords
    Words_to_be_Ignored = [',','.', '«', '»', ':', '"']

    for i in range(0,len(Words_to_be_Ignored)):
        stop_words.add(Words_to_be_Ignored[i])
    #print('\nVamos a omitir estas palabras: ', stop_words)

    # Removing the StopWords
    tokenized_word = word_tokenize(Text)
    filtered_sent=[]
    for w in tokenized_word:
        if w not in stop_words:
            filtered_sent.append(w)

    #FuntionFrequencyDistribution(filtered_sent, 50, True, 'FilteredSentences')

    #---------------------------------------------------------------------------
'''
