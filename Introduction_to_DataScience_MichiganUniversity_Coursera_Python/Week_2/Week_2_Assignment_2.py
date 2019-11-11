# Introduction to Data Science - University of Michigan
# Week 2 - Assignment 2
# DataFrame with Pandas

# Autor: Feelix Ernesto Charry Pastrana
# Ciudad de Meexico, Octubre 22 de 2019

import pandas as pd
import numpy as np
df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)
census_df = pd.read_csv('census.csv')

#print(df.head(n=10))
#print(census_df.head(n=20))

#Changing the names, identifying patterns
for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(')
df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] 
# the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
#print("\n Data: \n")
#print(df.head(n=15))

# ------------------------------------------------------------------------------
# Question 0 (Example)
# What is the first country in df

def answer_zero():
    print("\n Question 0 ")
    print(" The first country in the DataFrame df is: \n  ")
    return print(df.iloc[0])

print("\n Question 0")
#answer_zero() 

# ------------------------------------------------------------------------------
# Question 1 
# Which country has won the most gold medals in summer games?

def answer_one():
    x = df.loc[ df["Gold"] == max(df["Gold"])]
    return print(x.index[0])

print("\n Question 1")
#answer_one()

# ------------------------------------------------------------------------------
# Question 2
# Which country had the biggest difference between 
# their summer and winter gold medal counts?

def answer_two():
    import numpy as np 
    df['Diff.Gold'] = np.absolute(df['Gold']-df['Gold.1'])
    x = df.loc[ df["Diff.Gold"] == max(df["Diff.Gold"])]
    return print(x.index[0])

print("\n Question 2")
#answer_two()

# ------------------------------------------------------------------------------
# Question 3
# Which country has the biggest difference between their summer gold medal 
# counts and winter gold medal counts relative to their total gold medal count?

# (Only include countries that have won at 
# least 1 gold in both summer and winter.)
def answer_three():
    import numpy as np
    df['Q3'] = np.nan
    df.Q3[(df.Gold>0)&(df["Gold.1"]>0)]=(df.Gold-df["Gold.1"])/df["Gold.2"]
    maxValue = np.nanmax(df.Q3)
    x = df.loc[ df.Q3 == maxValue]
    return print(x.index[0])

print("\n Question 3")
#answer_three()

# ------------------------------------------------------------------------------
# Question 4
# Write a function that creates a Series called "Points" which is a weighted 
# value where each gold medal (Gold.2) counts for 3 points, 
# silver medals (Silver.2) for 2 points, and bronze medals (Bronze.2) 
# for 1 point. 

# The function should return only the column (a Series object) 
# which you created, with the country names as indices.

def answer_four():
    df['Question4']=df['Gold.2']*3+df['Silver.2']*2+df['Bronze.2'] 
    x = df.Question4
    return print(x)

print("\n Question 4")
#answer_four()

# ------------------------------------------------------------------------------
# Question 5
# Which state has the most counties in it?

def answer_five():
    a = census_df["STNAME"].value_counts()
    return print(a.index[0])

print("\n Question 5")
#answer_five()

# ------------------------------------------------------------------------------
# Question 6
# Only looking at the three most populous counties for each state, 
# what are the three most populous states 
# (in order of highest population to lowest population)? 
# Use CENSUS2010POP.

def answer_six():
    indexUniqueA    = census_df.STATE.unique()
    StNameSumPop = pd.DataFrame(columns=['STNAME', 'Sum'])

    for i in indexUniqueA:
        MaxStates = census_df[ 
            (census_df.STATE==i) & (census_df.SUMLEV==50)
                            ].nlargest(3, ["CENSUS2010POP"])
        StNameSumPop = StNameSumPop.append({
            'STNAME':MaxStates["STNAME"].iloc[0],'Sum':float(sum(MaxStates.CENSUS2010POP))
                                            }, ignore_index=True)
    
    b = ((StNameSumPop.nlargest(3, ["Sum"])).copy()).index
    a = list(StNameSumPop["STNAME"].loc[b])
    
    print(a)
    return a

print("\n Question 6")
answer_six()

# ------------------------------------------------------------------------------
# Question 7
# Which county has had the largest absolute change in population within 
# the period 2010-2015? 
# (Hint: population values are stored in columns POPESTIMATE2010 through 
# POPESTIMATE2015, you need to consider all six columns.)
def answer_seven():
    new = (census_df[census_df.SUMLEV == 50 ]).copy()

    columns_to_keep = [
        'POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012',
        'POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']
    
    b = (new[ columns_to_keep ]).copy()
    c = (b.T).copy()
    x = c.max()-c.min()
    xValue = max(x)
    indexValue = (x[x==xValue]).index
    seven = str(census_df["CTYNAME"].loc[indexValue[0]])
    print(seven)
    return seven 

print("\n Question 7")
answer_seven()

# ------------------------------------------------------------------------------
# Question 8
# In this datafile, the United States is broken up into 
# four regions using the "REGION" column. Create a query that finds the 
# counties that belong to regions 1 or 2, whose name starts with 'Washington', 
# and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# This function should return a 5x2 DataFrame with the 
# columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df 
# (sorted ascending by index).

def answer_eigth():
    columns_to_keep = ["REGION", "DIVISION", "STATE", "STNAME", "CTYNAME", "POPESTIMATE2014", "POPESTIMATE2015"]
    x = (census_df[columns_to_keep]).copy()

    x= (x[ ( (x.REGION==1) | (x.REGION==2) ) & (x["CTYNAME"].str.slice(stop=10) == "Washington") & (x["POPESTIMATE2014"] < x["POPESTIMATE2015"]) ]).copy()
    
    x["Index"] = x.index.values
    x = x.set_index(["Index"])
    x = (x[["STNAME", "CTYNAME"]]).copy()

    return print(x)
print("\n Question 8")
#answer_eigth()