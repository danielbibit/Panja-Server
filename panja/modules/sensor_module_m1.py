from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SensorModule():
    """A class describing a sensor module"""

    __tablename__ = 'sensor_module'
    id = Column(Integer, primary_key=True)
    
    sensors = {
        'IR' : '',
        'TEMP' : 0.0,
        'HUMI' : 0.0,
        'PRESENCE' : False
    }
    
    url = ''
    name = ''


    def __init__(self, url='', key='', name=''):
        self.url = url
        self.key = key
        self.name = name

    def get_states(self, sensor):
        return self.sensors[sensor]
    
    def sync(self):
        #tcp.send(self.hostname, self.port, '0;server;sync;0\n')
        pass

    def process_data(self, json_data):
        pass
