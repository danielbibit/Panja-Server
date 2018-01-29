import requests


class SensorBoard():
    """A class describing a sensor module"""

    def __init__(self, url='', key='', name='', sensors_avaliable=[]):
        self.url = url
        self.key = key
        self.name = name
        self.sensors = []
    
    def attach_device(self, device):
        pass

    def sync(self):
        r = requests.get(self.url + '/sync', params={'key' : self.key})
        print(r.text)

    def process_data(self, json_data):
        pass
