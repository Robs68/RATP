import cgi
import datetime
import cgitb
import pytz
import requests
import sys
import re
import csv
import pandas as pd
import numpy as np
print ("Lancement du Script Formatage RATP")
print (" ")

bad_words = ['SERVI', 'INFO','DERNIER', 'PREMIER', 'COMMEN', 'arr', 'approc', 'BUS', 'PERTURBATIO', 'ARRET']

with open('temps.csv') as oldfile, open('temps_format.csv', 'w') as newfile:
    for line in oldfile:
        if not any(bad_word in line for bad_word in bad_words):
            newfile.write(line)

df = pd.read_csv("temps_format.csv", sep='\s+',header=None, index_col=None, quotechar=" ")
df.columns = ['Date','Heure','First', 'Second']
print ('Row')
print ("")
print ("")
print ('Formatage')
print ("")

#1 datafram
df["Date"] = pd.to_datetime(df["Date"] + ' ' + df["Heure"])
df=df.drop(['Heure'],axis=1)
print df
print " "
print "Select Time Interval"
print " "

#test stackoverflow
#df['in_range'] = np.where((df['Date'].dt.hour == 8) & (df['Date'].dt.minute < 25), 'In Range', 'Out of Range')
#df['condition'] = df['First'] == 0
#print(df.groupby('in_range')['condition'].mean())
#heure = df.set_index('Date').between_time('07:50:00','08:20:00') #Rajout des secondes
#print heure
#df = pd.DataFrame(heure)
#print df

print ('Formatage pour relation')
print ("")
result = df.loc[df['First'] == '0']

test = (df.set_index('Date').between_time('07:50:00','08:20:00').reset_index().loc[lambda x: x.First == 0].Date.dt.time.value_counts().index[0])

valeur = (df.set_index('Date').between_time('07:50:00','08:20:00').reset_index().loc[lambda x: x.First == 0].Date.dt.time.value_counts())
print valeur
print test
