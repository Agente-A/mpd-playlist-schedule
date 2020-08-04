#!/usr/bin/env python3
from mpd import MPDClient
from credentials import *
import re, json, datetime, holidays, random, time

mpd = MPDClient()

mpd.connect(mpdServer,mpdPort)

playlists = mpd.listplaylists()

sagas = {}

'''
    Separación de string de playlist
    OST;SAGA;JUEGO;TIPO
'''
for pl in playlists:
    playlist = pl['playlist']
    s = re.split(';',pl['playlist'])
    if (s[0] == 'OST'):
        if s[1] not in sagas:
            sagas[s[1]] = []
        aux = {}
        aux['Playlist'] = playlist
        aux['Nombre'] = s[2]
        aux['Tipo'] = s[3]

        songs = mpd.listplaylistinfo(playlist)
        duration = 0.0
        for x in songs:
            duration += float(x['duration'])

        duration = int(duration)
        duration = time.strftime("%H:%M:%S", time.gmtime(duration))
        aux['Duracion'] = str(duration)
        sagas[s[1]].append(aux)

mpd.disconnect()

with open('playlists.json', 'w') as file:
    json.dump(sagas, file)

cl_holidays = holidays.Chile()

with open('horario.json', 'r') as file:
    horario = json.load(file)

week = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

programacion = {}

for i in range(7):
    day = datetime.date.today()
    day += datetime.timedelta(days=i)
    if day not in cl_holidays and i <= 4:
        # Día normal, una playlist por horario
        totalPlaylists = len(horario['Weekdays'])
        aux = []
        while len(aux) < totalPlaylists:
            selectedSaga = random.choice(list(sagas))
            selectedPl = random.choice(sagas[selectedSaga]).copy()
            if selectedPl not in aux:
                aux.append(selectedPl)
            
        for j in range(len(horario['Weekdays'])): 
            hour = horario['Weekdays'][j]
            aux[j]['Horario'] = str(datetime.time(hour['hora'], hour['minuto'])) 
            aux[j]['Enable']  = True
        programacion[week[i]] = aux.copy()
    else:
        # día libre, especial de una saga
        # Utilizar una sola saga (2 o más si no hay más playlist disponibles)
        totalPlaylists = len(horario['Holidays'])
        aux = []
        x = totalPlaylists
        while len(aux) < totalPlaylists:
            selectedSaga = random.choice(list(sagas))
            selectedPl = random.sample(sagas[selectedSaga], x if len(sagas[selectedSaga]) >= x else len(sagas[selectedSaga])).copy()
            aux.extend(selectedPl)
            x -= len(selectedPl)
        for j in range(len(horario['Holidays'])): 
            hour = horario['Holidays'][j]
            aux[j]['Horario'] = str(datetime.time(hour['hora'], hour['minuto'])) 
            aux[j]['Enable']  = True
        programacion[week[i]] = aux.copy()
        
with open('programacion.json', 'w') as file:
    json.dump(programacion, file, indent=3)