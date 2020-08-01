from beautifultable import BeautifulTable
from PIL import Image, ImageDraw
import json, requests, shutil

with open('programacion.json', 'r') as file:
   programacion = json.load(file)

img = Image.new('RGB', (1000, 2600), color = (73, 109, 137))
d = ImageDraw.Draw(img)
x = 0

table = BeautifulTable()
headers = []
data = []
for key, day in programacion.items():
    subtable = BeautifulTable()
    for item in day:
        for x, y in item.items():
            if x != 'Playlist':
                subtable.rows.append([y], header=x)
    data.append(subtable)
    headers.append(key)

table.rows.append(data)
table.columns.header = headers
d.text((10,10), str(table), fill=(255,255,0))

# with open('programacion.txt', 'w') as file:
#    file.write(str(table))
    
img.save('programacion.jpg')
