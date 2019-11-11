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

bad_words = ['SERVI', 'INFO','DERNIER', 'PREMIER', 'COMMEN', 'arr', 'approc', 'BUS', 'PERTURBATIO', 'ARRET', 'CIRCULATION']

with open('temps.csv') as oldfile, open('temps_format.csv', 'w') as newfile:
    for line in oldfile:
        if not any(bad_word in line for bad_word in bad_words):
            newfile.write(line)

df = pd.read_csv("temps_format.csv", sep='\s+',header=None, index_col=None, quotechar=" ")
df.columns = ['Date','Heure','First', 'Second']
print ("")
print ('Formatage')
print ("")

#1 datafram
df["Date"] = pd.to_datetime(df["Date"] + ' ' + df["Heure"])
df=df.drop(['Heure'],axis=1)
#print df
print " "

print ("Formatage pour relation en fonction de l'heure")
print ("")

max_count = (df.set_index('Date').between_time('07:50:00','08:20:00').reset_index().loc[lambda x: x.First == 0].Date.dt.time.value_counts().index[0])

valeur = (df.set_index('Date').between_time('07:50:00','08:20:00').reset_index().loc[lambda x: x.First == 0].Date.dt.time.value_counts())
print valeur

str_max_count = str(max_count)
print "Lheure est : "+ str_max_count
