import requests

class Switch():

    def __init__(self, name, parent_module, relay_board_number, state=False):
        self.parent_module = parent_module
        self.name = name # This should be a label
        self.adress = parent_module.url + '/control'
        self.relay_board_number = relay_board_number
        self.key = parent_module.key
        self.state = state
        
        self.parent_module.attach_device(self)

    def update(self):
        self.parent_module.sync()

    def on(self):
        r = requests.get(
            self.adress, 
            params={'key' : self.key, 'action' : 'on', 'args' : self.relay_board_number}
        )
        print(r.text)

    def off(self):
        r = requests.get(
            self.adress,
            params={'key' : self.key, 'action' : 'off', 'args' : self.relay_board_number}
        )
        print(r.text)

    def toggle(self):
        r = requests.get(
            self.adress, 
            params={'key' : self.key, 'action' : 'toggle', 'args' : self.relay_board_number}
        )
        print(r.text)