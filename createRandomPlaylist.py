from mpd import MPDClient
from dotenv import load_dotenv
import os, json

# Read Environment Variables.
load_dotenv()
mpdServer = os.getenv('MPD_SERVER')
mpdPort = os.getenv('MPD_PORT')

# Variables
randomPlaylist = 'Z;Random;VGM'
musicDir = 'VGM'
maxDuration = 15.0

mpd = MPDClient()

mpd.connect(mpdServer,mpdPort)

data = mpd.listall(musicDir)

# Read Data and add to the random playlist
for entry in data:
    if "file" in entry:
        song = mpd.find('file', entry['file'])[-1]
        if float(song['duration']) > maxDuration:
            mpd.playlistadd(randomPlaylist,song['file'])

mpd.disconnect()
