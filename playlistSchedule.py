from mpd import MPDClient
from dotenv import load_dotenv
import re, json, datetime, holidays, random, time, os

# Read Environment Variables.
load_dotenv()
mpdServer = os.getenv('MPD_SERVER')
mpdPort = os.getenv('MPD_PORT')

# This Variables depend on your configurations.
scheduleJson = 'programacion.json'  # The name of the file where the schedule will be read."
franchiseJson = 'playlists.json'    # The name of the file where all the playlist will be save in order.
timeJson = 'horario.json'           # The name of the file where you need to put the times when you want the playlist to schedule.
local_holidays = holidays.Chile()   # This will check for holidays in your local zone, change as you need, please refere to README.md

mpd = MPDClient()

mpd.connect(mpdServer,mpdPort)

playlists = mpd.listplaylists()

""" Create the JSON object with the list of all the playlist store in the MPD Server
the way this is designed is spliting the name of the actual playlist, that have this format:
"OST;FRANCHISE;GAME;TYPE", for more information of this, please refere to README.md
"""

franchise = {}

for pl in playlists:

    # Get the playlist
    playlist = pl['playlist']
    splittedPlaylist = re.split(';',pl['playlist'])

    # Check if is a OST Playlist
    if (splittedPlaylist[0] == 'OST'):

        # Check if the franchise didn't already exist
        if splittedPlaylist[1] not in franchise:
            franchise[splittedPlaylist[1]] = []

        # Populate the object
        aux = {}
        aux['Playlist'] = playlist
        aux['Nombre'] = splittedPlaylist[2]
        aux['Tipo'] = splittedPlaylist[3]
        songs = mpd.listplaylistinfo(playlist)
        duration = 0.0
        for x in songs:
            duration += float(x['duration'])

        duration = int(duration)
        duration = time.strftime("%H:%M:%S", time.gmtime(duration))
        aux['Duracion'] = str(duration)

        # Append the playlist
        franchise[splittedPlaylist[1]].append(aux)


# Disconnect and save to file.
mpd.disconnect()

with open(franchiseJson, 'w') as file:
    json.dump(franchise, file)

# Read the times when the playlist will be schedule
with open(timeJson, 'r') as file:
    horario = json.load(file)

# Days of the week
week = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

# the final object
schedule = {}

for i in range(len(week)):

    # Get the real date in the calendar base on today
    day = datetime.date.today()
    day += datetime.timedelta(days=i)

    # Check if is a workday or holiday
    if day not in local_holidays and i <= 4:
        # Workday, one random playlist per time schedule

        # Choose random playlist until all the time schedule are filed
        totalPlaylists = len(horario['Weekdays'])
        aux = []
        while len(aux) < totalPlaylists:
            selectedSaga = random.choice(list(franchise))               # Choose a random Franchise
            selectedPl = random.choice(franchise[selectedSaga]).copy()  # From the chossed Franchise, Choose a random Playlist

            # Exclude repeated playlist in the same day
            if selectedPl not in aux:
                aux.append(selectedPl)
            
        # Add the time schedule and enable the selected playlist
        for j in range(len(horario['Weekdays'])): 
            hour = horario['Weekdays'][j]
            aux[j]['Horario'] = str(datetime.time(hour['hora'], hour['minuto'])) 
            aux[j]['Enable']  = True
        
        # Finally add the day to the schedule.
        schedule[week[i]] = aux.copy()
    else:
        # Holiday, use only one random franchise until all time schedule are file
        # if there are not enough playlist, choose another random franchise and repeat
        
        totalPlaylists = len(horario['Holidays'])
        aux = []
        x = totalPlaylists

        # Choose random playlist until all the time schedule are filed
        while len(aux) < totalPlaylists:
            selectedSaga = random.choice(list(franchise))

            # If the selected Franchise have enough playlist to fill the schedule, choose 'x' amount of playlist for that franchise, else just copy it
            selectedPl = random.sample(franchise[selectedSaga], x if len(franchise[selectedSaga]) >= x else len(franchise[selectedSaga])).copy()
            aux.extend(selectedPl)
            x -= len(selectedPl)

        # Add the time schedule and enable the selected playlist
        for j in range(len(horario['Holidays'])): 
            hour = horario['Holidays'][j]
            aux[j]['Horario'] = str(datetime.time(hour['hora'], hour['minuto'])) 
            aux[j]['Enable']  = True
        
        # Finally add the day to the schedule.
        schedule[week[i]] = aux.copy()
        
# Save the JSON Object
with open(scheduleJson, 'w') as file:
    json.dump(schedule, file, indent=3)