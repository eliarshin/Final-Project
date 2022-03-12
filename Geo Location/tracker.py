import json
import requests
import argparse

class tracker:
    def __init__(tracker):
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