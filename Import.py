from Server_Connection import CovidDataImport
import sys
import Main
from datetime import date,timedelta
import json
import requests

args = sys.argv
option = int(args[2])
reg = str(args[1])
yesterday = str(Main.convertDateToInt(date.today() - timedelta(days=1)))

if option == 1:
    CovidDataImport().main(reg)

if option == 2:
    print("[Output] " + str(Main.getCovidData(yesterday,reg)))

if option == 3:
    print("[Output] " + str(json.loads(requests.get('https://api.covidtracking.com/v1/status.json').text)))

if option == 4:
    jsonFrame = Main.getCovidData(yesterday,reg.lower())

    print(
        '[Output] '+ 'On ' + yesterday + ", in region " + reg + ", there were " + str(jsonFrame['positiveIncrease']) + " new cases.\n"
        + "[Output] Additionally, there were " + str(jsonFrame['inIcuCurrently']) + " individuals in the ICU on this day, and " + str(
            jsonFrame['onVentilatorCurrently'])
        + " individuals on a ventilator.\n[Output] Furthermore, deaths increased by " + str(
            jsonFrame['deathIncrease']) + ", and hospitalizations by "
        + str(jsonFrame['hospitalizedIncrease']) + "."
        )
