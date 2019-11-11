# Introduction to Data Science - University of Michigan
# Week 3 - Assignment 3
# Advanced DataFrame with Pandas

# Autor: Feelix Ernesto Charry Pastrana
# Ciudad de Meexico, Octubre 25 de 2019

import pandas as pd
import numpy as numpy
from pandas import ExcelFile

# ------------------------------------------------------------------------------
# Energy Indicators.xls

# Removing the first 18 rows
energy = pd.read_excel('Energy Indicators.xls', skiprows = list(range(0,17)))
energy.drop(energy.columns[[0, 1]], axis = 1, inplace = True)
energy.rename(columns = {"Unnamed: 2": 'Country', "Petajoules":'Energy Supply', 
"Gigajoules":'Energy Supply per Capita', "%":'% Renewable'}, inplace = True)
energy.dropna(how='any', inplace=True)
energy['Energy Supply'] =pd.to_numeric(energy['Energy Supply'], errors='coerce')
energy['Energy Supply'] = energy['Energy Supply']*(10**6)
energy['Energy Supply per Capita'] = pd.to_numeric(
    energy['Energy Supply per Capita'], errors='coerce')
energy['% Renewable'] =pd.to_numeric(energy['% Renewable'], errors='coerce')
energy['Country'] = energy['Country'].astype(str)

# Removing numbers of the Country string
energy['Country'] = energy['Country'].str.replace('\d+','')
# Finding the countries with ( or )
from itertools import compress
key_words_to_find = ['(', ')', 'of America', 'Korea', 'Britain', 'Hong Kong']

my_list = []
for i in range(0,len(key_words_to_find)):
    x = energy['Country'].str.find(key_words_to_find[i]) >= 0
    y = list(compress(range(len(x)), x))
    my_list = list(set(my_list+y))

my_list.sort()
print(my_list)

# Changing the names manually 
names= ["Bolivia", "Hong Kong", "Korea", "Malvinas", "Iran", "Micronesia", 
    "South Korea", "Dutch", "United Kingdom", "United States", "Venezuela"]

energy.loc[my_list, 'Country']  = names
#print(energy['Country'].iloc[my_list])

# ------------------------------------------------------------------------------
# world_bank.csv
GPD = pd.read_csv('world_bank.csv', skiprows=4)
GPD["Country Name"] = GPD["Country Name"].astype(str)

# Removing numbers of the Country string
GPD["Country Name"] = GPD["Country Name"].str.replace('\d+','')

key_words_to_find = ["Korea, Rep","Iran","Hong Kong"]


my_list = []
for i in range(0,len(key_words_to_find)):
    x = GPD["Country Name"].str.find(key_words_to_find[i]) >= 0
    y = list(compress(range(len(x)), x))
    my_list = list(set(my_list+y))

my_list.sort()
print(my_list)

# Changing the names manually 
names = ["Hong Kong",  "Iran", "South Korea"]
GPD.loc[my_list, 'Country Name']  = names
#print(GPD["Country Name"].iloc[my_list])

# ------------------------------------------------------------------------------
# scimagojr-3.xlsx
ScimEn = pd.read_excel('scimagojr-3.xlsx')

# ------------------------------------------------------------------------------
# Selecting some of the columns and rows of energy, GPD and ScimEn 

# Energy:   All columns
# GPD:      'Country Name','2006', '2007', '2008', '2009', '2010', '2011', 
#           '2012', '2013', '2014', '2015'
# ScimEn:   All columns but only first 15 rows 

namesGPD = ['Country Name','2006', '2007', '2008', '2009', '2010', '2011', 
    '2012', '2013', '2014', '2015']

x1 = ScimEn.iloc[range(0,15)].copy()
x2 = energy.copy()
x3 = GPD[namesGPD].copy()

Three = pd.merge(x1,x2,how='inner',left_on='Country', right_on='Country')
Three = pd.merge(Three,x3,how='inner',left_on='Country', right_on='Country Name')

del Three['Country Name']
Three = Three.set_index('Country').copy()

print(Three.head(n=40))
print(Three.columns)

# ------------------------------------------------------------------------------
# The previous question joined three datasets then reduced this to just the 
# top 15 entries. When you joined the datasets, but before you reduced 
# this to the top 15 items, how many entries did you lose?

lenX1 = len(ScimEn)
lenX2 = len(x2)
lenX3 = len(x3) 
lenX2X3 = len(pd.merge(x2,x3,
    how='inner',left_on='Country',right_on='Country Name'))
lenX1X2 = len(pd.merge(x1,x2,how='inner',left_on='Country', right_on='Country'))
lenX1X3 = len(pd.merge(x1,x3,how='inner',left_on='Country', 
    right_on='Country Name'))
lenX1X2X3 = len(Three)

ValuesInX1X2 = lenX1X2 - lenX1X2X3
ValuesInX1X3 = lenX1X3 - lenX1X2X3
ValuesInX2X3 = lenX2X3 - lenX1X2X3

ValuesInX1 = lenX1 - ValuesInX1X2 - ValuesInX1X3 - lenX1X2X3
ValuesInX2 = lenX2 - ValuesInX1X2 - ValuesInX2X3 - lenX1X2X3
ValuesInX3 = lenX3 - ValuesInX1X3 - ValuesInX2X3 - lenX1X2X3

Total=ValuesInX1+ValuesInX2+ValuesInX3+ValuesInX1X2+ValuesInX1X3+ValuesInX2X3 

print("\n\n")
print("Question 2: how many entries did you lose?")
print(Total)

# ------------------------------------------------------------------------------
# What is the average GDP over the last 10 years for each country?

Years = ['2006', '2007', '2008', '2009', '2010', '2011', 
        '2012', '2013', '2014', '2015']

avgGDP = Three[Years].mean(axis = 1, skipna = True) 
avgGDP.sort_values(ascending=False, inplace = True)
print(avgGDP.head(n=20))

# ------------------------------------------------------------------------------
# By how much had the GDP changed over the 10 year span 
# for the country with the 6th largest average GDP?
ChangeGPD = Three[Years].loc[avgGDP.index[5]].max() - Three[Years].loc[avgGDP.index[5]].min()

# ------------------------------------------------------------------------------
# Question 5
Three["Energy Supply per Capita"].mean()

# ------------------------------------------------------------------------------
# Question 6
print(Three["% Renewable"].idxmax(), Three["% Renewable"].max())

# ------------------------------------------------------------------------------
# Question 7
