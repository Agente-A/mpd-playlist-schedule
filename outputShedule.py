from prettytable import PrettyTable

import json, requests, shutil

with open('programacion.json', 'r') as file:
   programacion = json.load(file)


table = PrettyTable()

for key, day in programacion.items():
    data = []
    for item in day:
        data.append(item['Nombre'])    
    table.add_column(key, data)


html = table.get_html_string()

