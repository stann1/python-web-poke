from datetime import datetime
import requests
import json
import os

def poke_goethe():
    postUrl = "https://www.goethe-bg.eu/gik/k3_et2_b.php"
    payload = { 'anrede':'m',
                'vorname':'Stanislav',
                'nachname':'Stoychev',
                'telefon':'',
                'email':'',
                'nktnnummer':76672,
                'neuerkurs':'B1.2e',
                'anmelder':4
                }
    r = requests.post(postUrl, data=payload)

    #print response
    print(r.text)

def poke_superdoc(name):
    with open(os.path.join(os.path.dirname(__file__), "doctors.json"), "r") as jsonfile:
        fileData = json.load(jsonfile)
        data = fileData[name]
        print("Read successful")

    getUrl = data["apiUrl"]
    r = requests.get(getUrl)

    if r.status_code >= 200 and r.status_code < 300:
        result_json = r.json()
        appointment = result_json['calendar']['earliestFree']
        print(f'[{datetime.now()}] -- {r.status_code} -- {appointment}')

        match_date = data["refDate"]
        if appointment['date'] < match_date:
          return f"New appointment slot for {name}: {appointment['date']}! {data['url']}" 
    else:
        print(f'[{datetime.now()}] -- {r.status_code}')
        return None