import json
import requests
import argparse
'''
Geo Location tracker is responsible to give us information about URL or
IP address, we get the informaption from public API and represent it to the user
in easy way to understand.
This step of gathering information is important to build profile on the target that
you want to attack.
If theres information about the company on the API it add the risk complexity on the 
risk algorithm calculation
'''
class tracker:
    def __init__(tracker):
        '''
        Init varibales that we will use in the code
        '''
        tracker.state = ""
        tracker.api = ""
        tracker.target = ""
        tracker.get_response = ""
        tracker.create_json =""

    def create_api_request(target):
        tracker.target = tracker.api + tracker.target
    
    def parse_json(target):
        tracker.get_response = requests.get(tracker.target)
        tracker.create_json = json.loads(tracker.get_response.content)
    
    def init_main(target):
        tracker.api = "http://ip-api.com/json/"
        tracker.target = input("Enter target")
        tracker.create_api_request(tracker)
        tracker.parse_json(tracker)
        print(tracker.create_json)

if __name__ == "__main__":
    track = tracker()
    track.init_main()