import logging

import requests

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RelayBoard(Base):
    """A class describing a relay board"""

    __tablename__ = 'relay_board'
    id = Column(Integer, primary_key=True)
    
    #url = Column(String)
    url = ''
    
    #key = Column(String)
    key = ''
    
    #name = Column(String)
    name = ''
    
    #number_of_relays = Column(Integer)
    number_of_relays = 0
    
    relays = []
    states = []

    def __init__(self, url='', key='', name='', number_of_relays=0):
        self.url = url
        self.key = key
        self.name = name
        self.number_of_relays = number_of_relays
        self.states = [None for i in range(number_of_relays)]

    def sync(self):
        r = requests.get(self.url + '/sync', params={'key' : self.key})
        print(r.text)

    #version:sender:action:argument
    def process_data(self, json_data):
        try:
            if json_data['action'] == 'status':
                self.set_states(json_data['argument'])
                #logging.debug(self.get_states())
                print(self.get_states())

            elif json_data['action'] == 'error':
                #logging.error(self.name + ', got the error : ' + json_data['argument'])
                pass

        except KeyError:
            pass

    def toggle_relay(self, number):
        if not 0 <= number < self.number_of_relays:
            raise NameError('invalid argument')

        r = requests.get(
            self.url + '/control', 
            params={'key' : self.key, 'action' : 'toggle', 'args' : number}
        )
        print(r.text)

    def on_relay(self, number):
        if not 0 <= number < self.number_of_relays:
            raise NameError('invalid argument')
        
        r = request.get(
            self.url + '/control',
            params={'key' : self.key, 'action' : 'on', 'args' : number}
        )

    def off_relay(self, number):
        if not 0 <= number < self.number_of_relays:
            raise NameError('invalid argument')

        r = request.get(
            self.url + '/control',
            params={'key': self.key, 'action' : 'off', 'args' : number}
        )

    def set_states(self, argument):
        argument = argument.split(',')
        map(lambda x : int(x), argument)
        self.states = argument

    def get_states(self, relay=-1):
        if relay == -1:
            return self.states
        elif not 0 <= relay < self.number_of_relays:
            raise NameError('invalid argument')
        elif relay >= len(self.states):
            raise NameError('Argument equal or bigger than list size')
        else:    
            return self.states[relay]
