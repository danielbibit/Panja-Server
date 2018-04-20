from panja import common
from panja import tools


class Room():
    id = 0

    def __init__(self, name=''):
        self.name = name
        self.rules = []
        self.devices = []
        common.rooms.append(self)

    def add_device(self, device):
        self.devices.append(device)

    def add_actuator(self, actuator):
        self.actuators.append(actuator)

    def devices_status(self):
        status = {}

        # for device in self.devices:
        #     if device is actuator: #WILL NOT WORK
        #         status['ACTUATORS'][device.name] = device.state
        #     elif device is sensor: #also not work
        #         status['SENSORS'][device.name] = device.state
        #     else:
        #         pass

        devices_dic = {}
        sensors_dic = {}

        for device in self.devices:
            devices_dic[device.name] = device.state

        status["ACTUATORS"] = devices_dic

        return status
