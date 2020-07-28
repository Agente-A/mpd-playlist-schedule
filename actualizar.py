from mpd import MPDClient
from credentials import *
from time import sleep
import schedule, datetime, json

def setPlaylist(mpd, playlist):
    mpd.connect(mpdServer,mpdPort)
    mpd.clear()
    mpd.random(0)
    mpd.load(playlist)
    mpd.play()
    mpd.disconnect()
    print("Playlist: " + playlist + "En cola")

def setRandom(mpd):
    mpd.connect(mpdServer,mpdPort)
    mpd.random(1)
    mpd.add('VGM')
    mpd.pause(0)
    mpd.disconnect()
    print("Random en cola")

def loadDay():
    schedule.clear()
    day = datetime.date.today()
    with open('programacion.json', 'r') as file:
        prog = json.load(file)

    playlists = prog[list(prog)[day.weekday()]]
    for pl in playlists:
        # Recuperar Horario de playlist y convertirlo en objeto datetime
        horario = datetime.datetime.strptime(pl['horario'], "%H:%M:%S")
        # Recuperar duracion y convertirlo en objeto datetime
        duracion = datetime.datetime.strptime(pl['Duracion'], "%H:%M:%S")
        fin = horario + datetime.timedelta(hours = int(duracion.strftime("%H")), minutes = int(duracion.strftime("%M")), seconds = int(duracion.strftime("%S")))

        schedule.every().day.at(horario.strftime("%H:%M:%S")).do(setPlaylist, mpd, pl['Playlist'])
        schedule.every().day.at(fin.strftime("%H:%M:%S")).do(setRandom, mpd)

mpd = MPDClient()

loadDay()
schedule.every().day.at('05:00').do(loadDay)

for x in schedule.jobs:
    print(x)

while True:
    schedule.run_pending()
    sleep(1)