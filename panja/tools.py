from panja import common


def get_module(name):
    for module in common.modules:
        if module.name == name:
            return module
    return None


def get_room(name):
    for room in common.rooms:
        if room.name == name:
            return room
    return None


def get_user(name):
    for user in common.users:
        if user.name == name:
            return user
    return None

def get_all_devices():
    l = []
    for room in common.rooms:
        for device in room.devices:
            l.append(device)

    return l

def generate_all_room_status():
    dic = {}
    for room in common.rooms:
        dic[room.name] = room.devices_status()

    return dic