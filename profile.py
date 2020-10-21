from pyrh import Robinhood
import json                     # credentials in json

class Profile:

    # Initializer / Instance Attributes
    def __init__(self):
        with open('credentials.json') as f:

            creds = json.load(f)

            self.username = creds['username']
            self.password = creds['password']

            self.rh = Robinhood()
            self.rh.login(username=self.username, password=self.password)