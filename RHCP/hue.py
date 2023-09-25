import requests
import json
import os
import time
import getpass

class hueBridge:

    def __generateClient(self):

        url = "http://" + self.ip + "/api"  # reuquest url 
        self.user = None                    # User variable
        
        # request body
        body = '{"devicetype":"RHCP-py#iphone ' + getpass.getuser()  + '"}' 

        # loop start time to calculate time elapsed
        startTime = time.time()

        # loop to wait for hueBridge button to be pressed
        while (self.user == None):

            # ask user to press the button on the bridge
            print("Press the hue bridge button to connect")
            
            # request username to connect to bridge
            r = requests.post(url, body)
            rJson = json.loads(r.text)[0]

            # check if username was successfuly generated
            if "success" in rJson.keys():
                self.user = rJson["success"]["username"]

            # wait to not overload network with requests
            time.sleep(0.2) 

            # calculate time elapsed and check if it surpassed the limit
            finalTime = time.time()
            if(finalTime - startTime) > 300:
                print("Time ran out, try connecting again later!")
                rJson = None
                break

        return rJson
        
    # Function to connect the class to the hue bridge
    def connect(self):
 
        # check if the resources path exists
        if not os.path.exists("./resources"):
            os.mkdir("./resources")

        # retrieve ip information from last sesson 
        if os.path.isfile("./resources/hue.json"):
            with open("./resources/hue.json", "r") as f:
                self.ip = json.loads(f.read())["internalipaddress"]
                print(self.ip)
                f.close()

        # saves this session bridge ip to a file
        else:
            r = requests.get("https://discovery.meethue.com")
            bridgeSettings = json.loads(r.text)[0]
            
            with open("./resources/hue.json", "w") as f:
                f.write(json.dumps(bridgeSettings))
                f.close()

        # retrieve username from file to controll connected devices 
        if os.path.isfile("./resources/hueUser.json"):
            with open("./resources/hueUser.json", "r") as f:
                self.user = json.loads(f.read())
                f.close()
       
        # generate username and save to a file
        else:
            clientGenerated = self.__generateClient()
            print(clientGenerated)
            if clientGenerated != None:
                with open("./resources/hueUser.json", "w") as f:
                    f.write(json.dumps(clientGenerated["success"]))
                    f.close()

    def __init__(self):
        self.connect()
