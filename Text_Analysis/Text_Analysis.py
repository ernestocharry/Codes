# Analizing books such as "Hundred Years of Solitud"
# Autor: Félix Ernesto Charry Pastrana
# email: charrypastranaernesto@gmail.com
# Date started: 2020 02 25

# Based on
#  https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk

'''
 The main question is which characterisctis DEFINE a book and, by extantion,
 analizing many book of a particular writter, I want to know the differences
 between two autors.
 Due the main Python library is written in English, all book will be read and analized in English.
'''

# Natural Languaje TollKit
import nltk
#nltk.download() Download all!
import matplotlib.pyplot as plt

# Frequency Distribution Function ----------------------------------------------
def FuntionFrequencyDistribution(NombreLista, MaxPalabrasRepetidas,
    Guardar, AditionalName=''):
    from nltk.probability import FreqDist
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
# ------------------------------------------------------------------------------

Folder_Main = '/Users/F.E.CharryPastrana/Documents/GitHub_PersonalCodes/'
Folder_Main = '/Users/Feliche/Documents/Codes/'
Folder_Main = Folder_Main + 'Text_Analysis/'

Folder_Books    = Folder_Main + 'Audiolibros/'
Folder_Graphs   = Folder_Main + 'Graphs/'

Book_Name   = 'Summaries'

File_Name   = open(Folder_Books + Book_Name + '.txt','r')
Text        = File_Name.read()

print('\n Book Analized: ', Book_Name)

# Sentence and Word Tokenization -----------------------------------------------
from nltk.tokenize import sent_tokenize, word_tokenize

tokenized_sent=sent_tokenize(Text)
import re # Removing \n
tokenized_sent = [re.sub('\n', '', fname) for fname in tokenized_sent]

tokenized_word=word_tokenize(Text)

print('\n Total oraciones en archivo:', len(tokenized_sent))
print('\n Total palabras en archivo:',  len(tokenized_word))

# Stopwords --------------------------------------------------------------------
# Stopwords considered as noise in the text.
# Text may contain stop words such as is, am, are, this, a, an, the, etc.
from nltk.corpus import stopwords

# Standar Stopwords
stop_words=set(stopwords.words("english"))
# Manually Stopwords
Words_to_be_Ignored = [',','.', '«', '»', ':', '"']

for i in range(0,len(Words_to_be_Ignored)):
    stop_words.add(Words_to_be_Ignored[i])
#print('\nVamos a omitir estas palabras: ', stop_words)

# Removing the StopWords
filtered_sent=[]
for w in tokenized_word:
    if w not in stop_words:
        filtered_sent.append(w)

FuntionFrequencyDistribution(filtered_sent, 50, True, 'FilteredSentences')

# Lexicon Normalization --------------------------------------------------------
# Lexicon normalization considers another type of noise in the text.
# For example, connection, connected, connecting word reduce to a common word
# "connect".
# It reduces derivationally related forms of a word to a common root word.

# Stemming - derivación
# Stemming is a process of linguistic normalization,
# which reduces words to their word root word or chops off
# the derivational affixes.
# For example, connection, connected, connecting word
# reduce to a common word "connect".

from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer

#ps = SnowballStemmer('spanish') # Be careful about the method to do the stemming
ps = PorterStemmer()
# The following languages are supported:
# Arabic, Danish, Dutch, English, Finnish, French, German, Hungarian, Italian,
# Norwegian, Portuguese, Romanian, Russian, Spanish and Swedish.
stemmed_words=[]

for w in filtered_sent:
    stemmed_words.append(ps.stem(w))
# ps.stem change Capital ltters and remove plurals

#print("Filtered Sentence:",filtered_sent)
#print("Stemmed Sentence:",stemmed_words)

#FuntionFrequencyDistribution(stemmed_words, 50, True)

# Lemmatization
# Lemmatization reduces words to their base word,
# which is linguistically correct lemmas.
# It transforms root word with the use of vocabulary and morphological analysis.
# Lemmatization is usually more sophisticated than stemming.
# Stemmer works on an individual word without knowledge of the context

# Find first the verb, noun, etc.

from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()       # Lemmatization
from nltk.stem.porter import PorterStemmer
stem = PorterStemmer()          # Stemming

# print("Lemmatized Word Working: ", lem.lemmatize('working','v'))

# Part Of Speech Tagging -------------------------------------------------------
# The primary target of Part-of-Speech(POS) tagging is to identify the
# grammatical group of a given word.
# Whether it is a NOUN, PRONOUN, ADJECTIVE, VERB, ADVERBS, etc.
# based on the context. POS Tagging looks for relationships within the sentence
# and assigns a corresponding tag to the word.

Sentence1   = tokenized_sent[1]
Words1      = word_tokenize(Sentence1)

#print('\n Example sentece:\n', Sentence1)
#print('\n Tokenize example sentence:\n', Words1)

All_tag = nltk.pos_tag(Words1,tagset='universal') # Superficial analysis
All_tag = nltk.pos_tag(tokenized_word, tagset='universal')

Verb    = [a for (a, b) in All_tag if b == 'VERB']
Noun    = [a for (a, b) in All_tag if b == 'NOUN']
Num     = [a for (a, b) in All_tag if b == 'NUM']
Pron    = [a for (a, b) in All_tag if b == 'PRON']
Punct   = [a for (a, b) in All_tag if b == '.']

FuntionFrequencyDistribution(Noun, 30, True, 'Noun')
FuntionFrequencyDistribution(Verb, 30, True, 'Verb')

Verb_Lemma = []
for i in range(0,len(Verb)):
    Verb_Lemma.append(lem.lemmatize(Verb[i],'v'))

FuntionFrequencyDistribution(Verb_Lemma, 30, True, 'VerbLemma')

print('\n\n')

# Sentiment Analysis -----------------------------------------------------------

# Machine learning based approach: Develop a classification model, which is
# trained using the pre-labeled dataset of positive, negative, and neutral.

# An important thing to remember about machine learning is that a model will
# perform well on texts that are similar to the texts used to train it.

# Once the algorithm has learned the style in terms of the most commonly used
# words and rhythmic patterns

# WORDS ADJACENCY NETWORKS - Methods
# "A more reliable approach is to use functional, rather than meaningful,
# words: 'the,' 'and,' 'or,' 'to,' and so on," explains Segarra.
# "Everyone has to use these words, so analyzing how they differ between
# authors gets closer to an objective measure of 'style'."
