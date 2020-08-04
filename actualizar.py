from mpd import MPDClient
from credentials import *
from time import sleep
import schedule, datetime, json

log = '/home/pi/scripts/radio/act_log.txt'

def setPlaylist(mpd, i):
    day = datetime.date.today()
    with open('programacion.json', 'r') as file:
        prog = json.load(file)
    today = prog[list(prog)[day.weekday()]]
    if today[i]['Enable']:
        mpd.connect(mpdServer,mpdPort)
        
        s = int(mpd.currentsong()['pos'])
        mpd.delete((s+1,))
        mpd.delete((0,s))

        mpd.random(0)
        mpd.load(today[i]['Playlist'])
        mpd.play()
        total = len(mpd.playlist())

        mpd.add('VGM')
        mpd.shuffle((total,))
        mpd.disconnect()

        f = open(log, "a")
        f.write("Playlist: " + today[i]['Playlist'] + " En cola\n")
        f.close()

        

def loadDay():
    schedule.clear('playlist')
    day = datetime.date.today()
    with open('programacion.json', 'r') as file:
        prog = json.load(file)

    playlists = prog[list(prog)[day.weekday()]]
    for i, pl in enumerate(playlists):
        # Recuperar Horario de playlist y convertirlo en objeto datetime
        horario = datetime.datetime.strptime(pl['Horario'], "%H:%M:%S")
        schedule.every().day.at(horario.strftime("%H:%M:%S")).do(setPlaylist, mpd, i).tag('playlist')

    f = open(log, "a")
    f.write("\n ** "+ datetime.datetime.now().strftime("%Y-%m-%d") + " ** \nJobs:\n")
    for x in schedule.jobs:
        f.write(str(x) + "\n")      
    f.close()

mpd = MPDClient()

loadDay()
schedule.every().day.at('05:00').do(loadDay)

while True:
    schedule.run_pending()
    sleep(1)