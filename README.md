# MPD Playlist Scheduler

* [Version en español](#español)
  * [Pre Requisitos](#pre-requisitos)
  * [Instalación](#instalación)
* [English version](#english)
  * [Requirements](#requirements)
  * [Installation](#installation)

## Español

### Pre requisitos

MPD Playlist Scheduler es un algoritmo escrito en python que te permitirá tener música aleatoria reproduciéndose 24/7

Es importante mencionar que ya debes tener implementado un servidor MPD en tu computador o en otro conectado en la red y además playlist creadas.

Este proyecto fue pensado desde la base de estar reproduciendo VGM (Video Game Music), por lo que los nombres de ciertas keys, listas y variables están ajustadas a esta idea, pero con una propia adaptación puede ser usada en música normal.

El formáto de las playlist debe ser el siguiente: 
`"OST;FRANCHISE;GAME;TYPE"`

Prefix | Razón
------ | -----
OST | En el caso de llegar a realizar playlist que no queremos que sea tomada en cuenta, no debe empezar con "OST", si queremos evitar esto debemos eliminar la comprobación en el script **playlistSchedule**
Franchise | Con esto agrupamos todos las playlist que pertenezcan a una misma franquicia
Game | Este es efectivamente el juego al que pertenece la playlist
Type | El tipo de playlist, es meramente informativo así que puedes poner lo que quieras

**\*** Las separación de estos prefijos debe ser con `";"`, ya que es uno de los caracteres que menos problemas causará con los nombres de los distintos prefijos.

Ejemplo:

`"OST;Persona;Persona 3;Best"`

Luego de correr playlistSchedule quedará algo así:

```javascript
[
    {
        "Playlist": "OST;Persona;Persona 3;Best",
        "Nombre": "Persona 3",
        "Tipo": "Best",
        "Duracion": "01:24:33"
    }
]
```

### Instalación

Cree estos scripts en linux Rasbian con python 3.7.3 
no ha sido probado en windows o MacOS, pero debería funcionar mientras tengas python3

Primero deberás instalar las dependencias utilizadas: `pip install -r dependences.txt`. Esto instalará: [python-mpd2](https://python-mpd2.readthedocs.io/en/latest/), [holidays](https://github.com/dr-prodigy/python-holidays), [schedule](https://schedule.readthedocs.io/en/stable/) y [python-dotenv](https://github.com/theskumar/python-dotenv). Lee sus documentaciones para más detalles.

Si gustas puedes cambiar el nombre de los archivos JSON que están en el inicio de cada script o dejarlos así, ya que puedes acceder a ellos desde otras aplicaciones para realizar otras acciones.

Algo que **debes** cambiar es la variable `local_holidays` de acuerdo a donde vives para obtener los días libres correctamente.
Además, si el servidor MPD está en otro computador debes cambiar la configuración en el archivo **.env**.

Luego debes programar estos script en CRON o una herramienta similar:

```sh
# MPD Radio
0 23 * * sun sh /path/to/repo/script_playlistSchedule.sh
@reboot sh /path/to/repo/script_actualizar.sh
```
>Recomiendo crear un shell script que ejecute estos python script, te ahorrará un montón de problemas con CRON (créeme). Dejaré unos ejemplos.

playlistSchedule debes correrlo una vez a la semana para que realize la planeación.

actualizar corre en un loop infinito que revisa la programación constantemente, por lo que solo debes correrlo una vez cada vez que el sistema se inicie.

## English

### requirements

MPD Playlist Scheduler is an algorithm wrote in python that will let you have random music playing 24/7.

for this to work, you need to have an already implemented MPD Server on your computer or another connected to the network and playlist created.

This project was thought with the idea of playing VGM (Video Game Music), some keys, list and variables are made for this idea, but with the proper adaptation it can be used with normal músic.

The format of the playlist in the MPD Server has to be:
`"OST;FRANCHISE;GAME;TYPE"`

Prefix | Reason
------ | ------
OST | in the case of create a playlist you not want to use here, does not have to start with "OST", if you have to remove this you also have to remove the verification in **playlistSchedule** script
Franchise | group all the playlist that are from the same franchise
Game | this is the game the playlist is from.
Type | the type of the playlist, this is only informative, it can be whatever you want

**\*** The separation of the prefix has to be with `";"`, it's the character that will cause you less problems with the names for the prefix,

Example:

`"OST;Persona;Persona 3;Best"`

After run playlistSchedule you will get something like:

```javascript
[
    {
        "Playlist": "OST;Persona;Persona 3;Best",
        "Nombre": "Persona 3",
        "Tipo": "Best",
        "Duracion": "01:24:33"
    }
]
```

### Installation

This scripts was made in linux Rasbian with python 3.7.3
there aren't tested in windows or MacOs, but it has to work if you have python3

First install the dependencies: `pip install -r dependences.txt`. Esto instalará: [python-mpd2](https://python-mpd2.readthedocs.io/en/latest/), [holidays](https://github.com/dr-prodigy/python-holidays), [schedule](https://schedule.readthedocs.io/en/stable/) y [python-dotenv](https://github.com/theskumar/python-dotenv). Read the their documentation for more details.

If you want you can change the name of the JSON Files (they are in the beginning of the scripts) or leave it, so you can access them form other applications to do other actions.

Something you **need** to change is the variable `local_holidays` according of where you live, so you can get the proper holidays.
If you have the MPD Server on another computer, you need to change the information in the **.env** file.

Then you have to schedule this scripts with CRON or something similar:

```sh
# MPD Radio
0 23 * * sun sh /path/to/repo/script_playlistSchedule.sh
@reboot sh /path/to/repo/script_actualizar.sh
```
>I recommend create a shell script to execute the python scripts, it will save you a lot of problems with CRON (believe me). i leave you some examples.

playlistSchedule has to be ran once a week so can create the weekly schedule.
actualizar run on an infinite loop that check the schedule constantly, so only has to be ran on reboot.
