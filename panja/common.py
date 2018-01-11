import os
import json

PANJADIR = os.path.abspath(os.path.dirname(__file__))

settings = json.load(open(PANJADIR + '/config.json'))
error_strings = json.load(open(PANJADIR + '/resources/errors.json'))

clients = ['ANDROID', 'WEB', 'JAVA', 'CLI', 'IOS']

modules = []
rooms = []
users = []