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
    with open(os.path.join(os.path.dirname(__file__), "doctors-super.json"), "r") as jsonfile:
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

def poke_easydoc(name):
    with open(os.path.join(os.path.dirname(__file__), "doctors-easy.json"), "r") as jsonfile:
        fileData = json.load(jsonfile)
        data = fileData[name]
        print("Read successful")
    
    url = data["apiUrl"]
    r = requests.post(url, json = data["body"], headers = {"Content-Type": "application/json;charset=utf-8", "Accept": "application/json"}) if data["type"] == "POST" else requests.get(url)

    if r.status_code >= 200 and r.status_code < 300:
        result_json = r.json()
        #print(result_json)
        appointment = result_json['first_available_slot']
        resp_message = result_json['first_available_slot_message']
        print(f'[{datetime.now()}] -- {r.status_code} -- {resp_message}')

        if appointment and not "Няма намерен свободен час" in resp_message:
          return f"New appointment slot for {name}: {resp_message}! {data['url']}" 
    else:
        print(f'[{datetime.now()}] -- {r.status_code}')
    
    return None