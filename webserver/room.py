from panja import common
from panja import tools


class Room():
    id = 0
    name = ''
    actuators = []
    sensors = []
    rules = []

    def __init__(self, name=''):
        self.name = name
        self.sensors = []
        self.rules = []
        self.actuators = []

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def add_actuator(self, actuator):
        self.actuators.append(actuator)
        
    def devices_status(self):
        status = {}
        
        actuators_dic = {}
        sensors_dic = {}
        
        for i in self.actuators:
            actuators_dic[i[0]] = tools.get_module(i[1][0]).get_states(i[1][1])

        for i in self.sensors:
            sensors_dic[i[1]] = tools.get_module(i[0]).get_states(i[1])

        status["ACTUATORS"] = actuators_dic
        status["SENSORS"] = sensors_dic

        return status
