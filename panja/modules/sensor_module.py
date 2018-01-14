import requests
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SensorModule():
    """A class describing a sensor module"""

    def __init__(self, url='', key='', name='', sensors_avaliable=[]):
        self.url = url
        self.key = key
        self.name = name
        self.sensors = []
    
    def sync(self):
        r = requests.get(self.url + '/sync', params={'key' : self.key})
        print(r.text)

    def process_data(self, json_data):
        pass
