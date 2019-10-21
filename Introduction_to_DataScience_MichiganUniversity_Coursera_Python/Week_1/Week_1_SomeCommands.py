# Introduction to Data Science in Python - Michigan University
# Coursera 
# FECHP 20191021
# Week 1 - Some commands to remember

import numpy as np
import datetime as dt 
import time as tm 
import csv 

# Functions 
def add_numbers(x, y):
    return x + y

x = add_numbers(1, 2)
print(x)

# This is called TUPLE. Immutable
x = (1, 'a', 2, 'b')
print(type(x))

# This is a LIST. Mutable 
x = [1, '1', 'abs', 2, 3]
print(type(x))

x.append('My name is Ernesto')
print(x)

#-------------------------------------------------------------------------------
# Directories associated keys with Values 
x = {'FirstName':'Feelix', 'MiddleName':'Ernesto', 
    'LastName':'Charry','MothersName':'Pastrana'}
print(x['MothersName'])

#-------------------------------------------------------------------------------
with open('Week_1_DemoData.csv') as csvfile:
    dataCSV = list(csv.DictReader(csvfile))

#print(dataCSV[0:1]) 
print(dataCSV[0].keys())

#-------------------------------------------------------------------------------
print('\n\n')
SomeTime = tm.time()
print(SomeTime)

#Converting time 
dtnow = dt.datetime.fromtimestamp(SomeTime)
print(dtnow)
print(dtnow.second)

#-------------------------------------------------------------------------------
print('\n\nPYTHON CLASS\n\n')

class Person: # Adding some characteristics 
    departament = 'Physics departament'
    def set_name(self, newname):
        self.name = newname
    def set_location(self, location):
        self.location = location

persona = Person()
print(persona.departament)

persona.set_name('Natalia Charry Pastrana')
persona.set_location('Neiva - Huila - Colombia')

print(persona.name)
print(persona.location)

#-------------------------------------------------------------------------------
print('\n\n-----Numpy-----\n\n')

a = []
for i in dataCSV:
    a.append(float(i['id']))

b = np.array(a)
print(b.mean())
print(b.std())

#-------------------------------------------------------------------------------
print('\n\n----- Lambda and List Comprehensions -----\n\n')

people = ['Dr. Christopher Brooks', 'Dr. Kevyn Collins-Thompson', 
            'Dr. VG Vinod Vydiswaran', 'Dr. Daniel Romero']

split_title_and_name = lambda person : person.split()[0] + ' ' + person.split()[-1]

for i in people: 
    print(split_title_and_name(i))

# Another example 
lowercase = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'

Users = []
nL = len(lowercase)
nN = len(digits)
Users = [lowercase[i]+lowercase[j]+digits[k]+digits[m]
        for i in range (0,nL) 
        for j in range (0,nL)
        for k in range (0,nN)
        for m in range (0,nN) ]

