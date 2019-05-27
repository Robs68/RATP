from zeep import Client
import cgi
import datetime
import cgitb
import pytz
import requests
#import xml.etree.ElementTree as ET
import sys
#import json
import re
import csv

print ("Lancement du Script RATP")
print (" ")

ratp_client = Client('Wsiv.wsdl')

line_t = ratp_client.get_type('ns0:Line')
station_t = ratp_client.get_type('ns0:Station')
direction_t = ratp_client.get_type('ns0:Direction')
mission_t = ratp_client.get_type('ns0:Mission')

# fuseau horaire
tz = pytz.timezone('Europe/Paris')

# retourne le temps actuel en utilisant le format de l'API
def now_ratp():
    d = datetime.datetime.now(tz=tz)
    return '%u%02u%02u%02u%02u' % (d.year, d.month, d.day, d.hour, d.minute)

#info station
def print_station(line, station):

	oline = line_t(codeStif=line)	
	ostation = station_t(line=oline, name=station)
	tram = ratp_client.service.getStations(station=ostation)

#horaire station
def print_horaire(line, station, sens):

	oline = line_t(codeStif=line, realm='r')
        ostation = station_t(line=oline, name=station)
	odirection = direction_t(sens = sens)
	mission = ratp_client.service.getMissionsNext(station=ostation, direction=odirection)
#	print mission
	
	inmission = []
	inmission_next = []
	for ligne in mission['missions'][0]['stationsMessages']:
		inmission.append(ligne)
		print inmission
	for ligne in mission['missions'][1]['stationsMessages']:
        	inmission_next.append(ligne)
                print inmission_next	

#Formatage des donnees

	inmission=inmission[-1]
#	inmission=inmission[:-2]
	t=len(inmission)
	print ("longeur",t)
	if t == 5:
		inmission=inmission[:-1]
	inmission=inmission[:-2]
	if t == 1 or t == 9 or t == 12:
		inmission="0"
	print inmission

	inmission_next=inmission_next[-1]
	t2=len(inmission_next)
	if t2 == 5:
                inmission_next=inmission_next[:-1]
	inmission_next=inmission_next[:-2]
	print inmission_next

	date=datetime.datetime.now()
	date_jour = str(date.strftime('%Y-%m-%d'))
	heure_jour = str(date.strftime('%H:%M'))

	with open('temps.csv','a') as f :
                writer = csv.writer(f, delimiter=' ', quoting=csv.QUOTE_NONE, escapechar=' ')
                writer.writerows(zip([date_jour],[heure_jour],[inmission],[inmission_next]))

print_station('100100179', 'Rond-Point des Bruyeres') #CodeStif, nom station
print_horaire('100100179', 'Rond-Point des Bruyeres', 'R')
