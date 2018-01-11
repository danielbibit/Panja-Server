from panja import common


def get_module(name):
    for i in common.modules:
        if i.name == name:
            return i
    return None


def generate_all_room_status():
    dic = {}
    for room in common.rooms:
        dic[room.name] = room.devices_status()

    return dic


def generate_server_model():
    dic = {}

    dic['rooms'] = generate_all_room_status()

    return dic