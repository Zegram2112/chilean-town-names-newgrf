import os
import requests as re
from bs4 import BeautifulSoup
from pprint import pprint


def getCities():
    response = re.get("https://es.wikipedia.org/wiki/Anexo:Ciudades_de_Chile")
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('table.wikitable:nth-child(5)')[0].select('tr')[1::]
    def rowToCity(row):
        tds = row.find_all('td')
        pop = int(tds[4].text.replace(' ', '').strip().replace('\xa0', ''))
        return {
            "city": tds[0].text,
            "population": pop,
            "probability": int(pop / (600_000 / 127)) + 1,
        }
    cities = list(map(rowToCity, rows))
    pprint(cities)
    return cities

cities = getCities()

print("Building town definition...")
town_names = map(lambda x: f"text(\"{x['city']}\", {x['probability']})", cities)
town_definition = f"""town_names {{
    styles: string(STR_MENU_NAME);
    {{
        {', '.join(town_names)}
    }}
}}"""

print("Building NML file...")
with open("grf.grf", "r") as grf_file:
    grf_definition = grf_file.read()
with open("chilean-town-names.nml", "w") as nml:
    nml.writelines([grf_definition, town_definition])

print("Building .nml file...")
os.system("nmlc -c --grf chilean-town-names.grf chilean-town-names.nml")
print("Installing NewGRF on openttd documents...")
os.system("cp ./chilean-town-names.grf ~/Documents/OpenTTD/newgrf")
print("Done.")
