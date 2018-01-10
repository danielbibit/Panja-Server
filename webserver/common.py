import os
# import queue
import json

PANJADIR = os.path.abspath(os.path.dirname(__file__))

# input_queue = queue.Queue()

settings = json.load(open(PANJADIR + '/config.json'))
error_strings = json.load(open(PANJADIR + '/resources/errors.json'))

clients = ['ANDROID', 'WEB', 'JAVA', 'CLI', 'IOS']

modules = []
rooms = []
users = []