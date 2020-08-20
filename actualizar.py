from mpd import MPDClient
from dotenv import load_dotenv
from time import sleep
import schedule, datetime, json, os

# Read Environment Variables.
load_dotenv()
mpdServer = os.getenv('MPD_SERVER')
mpdPort = os.getenv('MPD_PORT')

# This Variables depend on your configurations.
# You can leave them as this but you need to change musicDir if you have it in another location

musicDir = 'VGM'                    # The MPD directory for random music.
log = f'{os.getcwd()}/act_log.txt'  # Where you want to log the information.
scheduleJson = 'programacion.json'  # The name of the file where the schedule will be read."

def setPlaylist(mpd, i):
    """This will clear the current Queue leaving only the current song playing,
    afther that it will load the playlist at the corresponding time.
    The names of the dictionary index are properly from MPD, not change it.

    Args:
        mpd (MPDClient): the instance of the mpd library.
        i (int): the index of the time in the json schedule.
    """
    
    # Read the playlists of today
    day = datetime.date.today().weekday()
    with open(scheduleJson, 'r') as file:
        prog = json.load(file)

    todayPlaylist = prog[list(prog)[day]]
    if todayPlaylist[i]['Enable']:
        
        # Connect
        mpd.connect(mpdServer,mpdPort)
        
        # Clear Queue
        currentSongPos = int(mpd.currentsong()['pos'])
        mpd.delete((currentSongPos+1,))
        mpd.delete((0,currentSongPos))

        # Load Playlist
        mpd.random(0)
        mpd.load(todayPlaylist[i]['Playlist'])
        mpd.play()
        
        # Shuffle all the songs after playlist
        total = len(mpd.playlist())
        mpd.add(musicDir)
        mpd.shuffle((total,))

        # Disconnect and log
        mpd.disconnect()
        f = open(log, "a")
        f.write("Playlist: " + todayPlaylist[i]['Playlist'] + " En cola\n")
        f.close()

def loadDay():
    """This will load the playlist from scheduleJson and schedule them for today
    this method will run every day at the givin time below.
    """

    # Clear the scheduled task to reproduce playlist and read scheduleJson
    schedule.clear('playlist')
    day = datetime.date.today().weekday()
    with open(scheduleJson, 'r') as file:
        prog = json.load(file)

    # Read the playlist for today and schedule them
    playlists = prog[list(prog)[day]]
    for i, pl in enumerate(playlists):

        # Parse From String to datetime format and schedule
        horario = datetime.datetime.strptime(pl['Horario'], "%H:%M:%S")
        schedule.every().day.at(horario.strftime("%H:%M:%S")).do(setPlaylist, mpd, i).tag('playlist')

    # Log the schedule jobs with the current date as header
    f = open(log, "a")
    f.write("\n ** "+ datetime.datetime.now().strftime("%Y-%m-%d") + " ** \nJobs:\n")
    for x in schedule.jobs:
        f.write(str(x) + "\n")      
    f.close()

# Main application

mpd = MPDClient()

# Run onces loadDay() and then schedule it
# You can change the hour
loadDay()
schedule.every().day.at('05:00').do(loadDay)

# Infinite loop to run pending schedule jobs
while True:
    schedule.run_pending()
    sleep(1)