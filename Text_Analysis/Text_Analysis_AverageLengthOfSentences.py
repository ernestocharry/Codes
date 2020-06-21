# Analizing the average length of the sentences in a Book.  
# Autor: Félix Ernesto Charry Pastrana 
# email: charrypastranaernesto@gmail.com
# Date started: 2020 03 05 

'''
This code will find the distribution of the length. 
'''
import nltk # Natural Languaje TollKit nltk.download() Download all!
import matplotlib.pyplot as plt
import glob # To know all the txt files in a folder 
from nltk.tokenize import sent_tokenize, word_tokenize
import re # Removing \n
import pandas as pd

Folder_Main     = '/Users/F.E.CharryPastrana/Documents/GitHub_PersonalCodes/'
Folder_Main     = Folder_Main + 'Text_Analysis/'

Folder_Books    = Folder_Main + 'Books_in_English/'
Folder_Graphs   = Folder_Main + 'Graphs/'

all_books  = glob.glob(Folder_Books+"*.txt")
Longitud_Folder_Books = len(Folder_Books)
print('\n Se analizaran ', len(all_books), ' libros')

LongitudMax = 800
print('\n La longitud máxima de las oraciones analizadas será ', LongitudMax)

pdFrequencyReference = pd.DataFrame({'Length':range(1,LongitudMax+1)})

for j in range(0, len(all_books)):
    Book_Name = all_books[j][Longitud_Folder_Books:len(all_books[j])]
    File_Name   = open(all_books[j],'r')
    Text        = File_Name.read()
    tokenized_sent=sent_tokenize(Text)
    tokenized_sent = [re.sub('\n', '', fname) for fname in tokenized_sent]
    tokenized_word=word_tokenize(Text)

    print('\n ----------------------------------------------------------------')
    print('\n j: ', j)
    print(' Book Analized: ', Book_Name)
    print(' Total oraciones en archivo:', len(tokenized_sent))
    print(' Total palabras en archivo:',  len(tokenized_word))

    # En pdSentencesLength se guardará las oraciones y su longitud 
    pdSentencesLength = pd.DataFrame(tokenized_sent)
    pdSentencesLength.rename(columns = {list(pdSentencesLength)[0]:'Sentences'}, inplace = True)
    pdSentencesLength['Length'] = pdSentencesLength['Sentences'].apply(len)

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
    AditionalName = '20200306'
    FileName_FreqDis = 'Frequency_LengthSentences_' + Book_Name + '_'
    FileName_FreqDis = FileName_FreqDis +  '_'
    FileName_FreqDis = FileName_FreqDis + AditionalName +'.png'

    plt.ion()
    pdFrequencyReference.plot(x = 'Length', y = Nombre, style = '-', xlim = [1,LongitudMax], ylim = [0,2], label = Book_Name)
    plt.savefig(Folder_Graphs+FileName_FreqDis, bbox_inches = "tight")
    plt.ioff() 

print('\n ----------------------------------------------------------------')
print(pdFrequencyReference.head(30))
print('\n')