# Introduction to Data Science in Python 
# Michigan University 
# Week 3
# Playing again with Pandas

import pandas as pd
import numpy as np 
import timeit

#---------- Series with PANDAS -------------------------------------------------
df = pd.DataFrame([{'Chris', 'Sponge',          22.50},
                   {'Kevyn', 'Kitty Litter',    2.50},
                   {'Filip', 'Spoon',           5.00}],
                  index=['Store 1', 'Store 1', 'Store 2'])
df.columns = ['Col_1', 'Col_2', 'Col_3']
print('\n')
print(df)

# MERGE ------------------------------------------------------------------------
staff_df = pd.DataFrame([{'Name': 'Kelly', 'Role': 'Director of HR'},
                         {'Name': 'Sally', 'Role': 'Course liasion'},
                         {'Name': 'James', 'Role': 'Grader'}])
staff_df = staff_df.set_index('Name')
student_df = pd.DataFrame([{'Name': 'James', 'School': 'Business'},
                           {'Name': 'Mike', 'School': 'Law'},
                           {'Name': 'Sally', 'School': 'Engineering'}])
#student_df = student_df.set_index('Name')

both = pd.merge(student_df, staff_df, how = 'outer', left_on = 'Name',
    right_index=True)

staff_df = pd.DataFrame([
    {'First Name': 'Kelly','Last Name': 'Desjardins', 'Role': 'Director of HR'},
    {'First Name': 'Sally','Last Name': 'Brooks', 'Role': 'Course liasion'},
    {'First Name': 'James','Last Name': 'Wilde', 'Role': 'Grader'}])
student_df = pd.DataFrame([
    {'First Name': 'James', 'Last Name': 'Hammond', 'School': 'Business'},
    {'First Name': 'Mike', 'Last Name': 'Smith', 'School': 'Law'},
    {'First Name': 'Sally', 'Last Name': 'Brooks', 'School': 'Engineering'}])

print('\n')
print(staff_df)
print('\n')
print(student_df)
# Merging using two columns 
both = pd.merge(staff_df, student_df, how='outer', 
    left_on=['First Name','Last Name'], right_on=['First Name','Last Name'])
print('\n')
print(both)

# Idiomatic Pandas.... PANDORABLE ----------------------------------------------
df = pd.read_csv('census.csv')
(df.where(df['SUMLEV']==50)
    .dropna()
    .set_index(['STNAME','CTYNAME'])
    .rename(columns={'ESTIMATESBASE2010': 'Estimates Base 2010'}))

def min_max(row):
    data = row[['POPESTIMATE2010',
                'POPESTIMATE2011',
                'POPESTIMATE2012',
                'POPESTIMATE2013',
                'POPESTIMATE2014',
                'POPESTIMATE2015']]
    return pd.Series({'min': np.min(data), 'max': np.max(data)})
print("\n")
print(df.apply(min_max, axis=1))

rows = ['POPESTIMATE2010',
        'POPESTIMATE2011',
        'POPESTIMATE2012',
        'POPESTIMATE2013',
        'POPESTIMATE2014',
        'POPESTIMATE2015']
print("\n")
print(df.apply(lambda x: np.max(x[rows]), axis=1))

# GroupBy ----------------------------------------------------------------------
# Example 
# print(df.groupby('Category').apply(lambda df,a,b: sum(df[a] * df[b]), 
# 'Weight (oz.)', 'Quantity'))
df = df[df['SUMLEV']==50]

