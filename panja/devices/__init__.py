''' A class describing pure devices'''

class Light(object):
    pass


class Switch(object):

    def __init__(self, adress, key):
        self.adress = adress
        self.key = key

    def toggle(self):
        pass

    def on(self):
        pass

    def off(self):
        pass



class Sensor(object): # Rfid ?
    pass


class Media(object):
    pass


class Client(object): # Commander ? Prompt ?
    pass


class TemperatureSensor(object):
    pass


class PresenceSensor(object):

    def __init__(self, name):
        self.name = name

        self.last_seen = 0.0


class IrReceiver(object):
    pass
