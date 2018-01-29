import logging
import requests

from panja import common

class RelayBoard(object):
    """A class describing a relay board"""

    def __init__(self, url='', key='', name='', number_of_relays=0):
        self.url = url
        self.key = key
        self.name = name
        self.number_of_relays = number_of_relays
        self.devices = []
        common.modules.append(self)

    def attach_device(self, device):
        if not len(self.devices) < self.number_of_relays:
            raise NameError('Cant attacht more devices')

        self.devices.append(device)

    def sync(self):
        r = requests.get(self.url + '/sync', params={'key' : self.key})
        print(r.text)

    def process_data(self, json_data):
        try:
            if json_data['action'] == 'status':
                self.set_states(json_data['argument'])
                # print(self.get_states())

            elif json_data['action'] == 'error':
                pass

        except KeyError:
            pass

    def set_states(self, argument):
        argument = argument.split(',')
        map(lambda x : int(x), argument)
        print(argument)

        for n, state in enumerate(argument):
            for device in self.devices:
                if device.relay_board_number == n:
                    print(device.name + str(device.relay_board_number) + 'has the state set to' + str(state))
                    # device.state = bool(state)
                    device.state = state
