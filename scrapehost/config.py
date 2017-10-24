import json


config = {}

with open('config.json') as configfile:
    config = json.loads(configfile.read())
configfile.close()
