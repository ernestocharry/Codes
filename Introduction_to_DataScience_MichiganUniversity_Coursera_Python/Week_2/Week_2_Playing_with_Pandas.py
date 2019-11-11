# Introduction to Data Science in Python 
# Michigan University 
# Week 2 
# Playing with Pandas

import pandas as pd
import numpy as np 
import timeit

#---------- Series with PANDAS -------------------------------------------------
print('\n\n ------ Pandas ------ \n\n')
animals = ['Tiger', 'Bear', 'Moose']
Serie1 = pd.Series(animals)
print(Serie1)
print(Serie1.index)

# Create series of 10000 random numbers from 0 to 1000
s = pd.Series(np.random.randint(0,1000,10000))
print(s.head())

# timeit measure time ?? 
summary = 0
for item in s:
    summary+=item
print(summary)

s += 2 # Adds two to each item in s using broadcasting

#---------- DataFrame with PANDAS ----------------------------------------------
purchase_1 = pd.Series({'Name': 'Chris',
                        'Item Purchased': 'Dog Food',
                        'Cost': 22.50})
purchase_2 = pd.Series({'Name': 'Kevyn',
                        'Item Purchased': 'Kitty Litter',
                        'Cost': 2.50})
purchase_3 = pd.Series({'Name': 'Vinod',
                        'Item Purchased': 'Bird Seed',
                        'Cost': 5.00})
df = pd.DataFrame([purchase_1, purchase_2, purchase_3], 
                    index=['Store 1', 'Store 1', 'Store 2'])
print(df.head())


#-------------------------------------------------------------------------------
# Video exercise 
# Reindex the purchase records DataFrame to be indexed hierarchically, 
# first by store, then by person. Name these indexes 'Location' and 'Name'. 
# Then add a new entry to it with the value of:
#   Name: 'Kevyn', Item Purchased: 'Kitty Food', Cost: 3.00 Location: 'Store 2'

purchase_1 = pd.Series({'Name': 'Chris',
                        'Item Purchased': 'Dog Food',
                        'Cost': 22.50})
purchase_2 = pd.Series({'Name': 'Kevyn',
                        'Item Purchased': 'Kitty Litter',
                        'Cost': 2.50})
purchase_3 = pd.Series({'Name': 'Vinod',
                        'Item Purchased': 'Bird Seed',
                        'Cost': 5.00})

df = pd.DataFrame([purchase_1, purchase_2, purchase_3], 
        index=(['Store 1', 'Store 1', 'Store 2'] ))


# Your answer here
df['Location'] = list(df.index)
df = df.set_index( ['Location', 'Name'] )

newSeries = pd.Series({
  'Item Purchased': 'Kitty Food', 
  'Cost': 3.00,
  'Location': 'Store 2', 
  'Name': 'Kevyn'
  })

new = pd.DataFrame([newSeries])
new = new.set_index(['Location', 'Name'])

df = df.append(new)
print(df)

# Solution
df = df.set_index([df.index, 'Name'])
df.index.names = ['Location', 'Name']
df = df.append(
    pd.Series(data={'Cost': 3.00, 'Item Purchased': 'Kitty Food'}, name=('Store 2', 'Kevyn')))
df