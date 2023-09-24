import requests
import json

class hueBridge:

    def connect(self):
        r = requests.get("https://discovery.meethue.com")
        print(r.text)
        print(json.loads(r.text))
        

    def __init__(self):
        self.connect()
