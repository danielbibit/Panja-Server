import os
import sys
import time
import threading
import json
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask import request
from flask import render_template

from panja import common
from panja import tools
from panja import house_config


app = Flask(__name__)


def poller():
    while True:
        time.sleep(common.settings["POLL_INTERVAL"])

        for module in common.modules:
            module.sync()

        print('alive')
        print(json.dumps(tools.generate_all_room_status(), sort_keys=True, indent=4))


def main():
    if not os.path.isfile(common.PANJADIR + '/config.json'):
        print(common.error_strings['CONFIG_USER_NOT_FOUND'])
        exit()

    poller_thread = threading.Thread(target=poller)
    poller_thread.daemon = True
    poller_thread.start()
    print('Poller thread started in: ' + poller_thread.name)

    print('Main server started at: ' + time.asctime())

    app.run(host='0.0.0.0', threaded=True)


@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'test'


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return app.send_static_file('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return 'Goodbye'


@app.route('/webclient', methods=['GET'])
def web_client():
    room_model = tools.generate_all_room_status()

    return render_template('dashboard.html', rooms=room_model, room=None)


@app.route('/webclient/settings', methods=['GET'])
def web_client_settings():
    return 'yeah'


@app.route('/webclient/room/<name>', methods=['GET'])
def web_client_room(name):
    room_model = tools.generate_all_room_status()

    return render_template(
        'dashboard.html',
        rooms=room_model,
        room=tools.get_room(name).devices_status(),
        selected_room_name=name
    )


#TODO must fix this method to use wakeonlan and other devices
@app.route('/clients', methods=['POST'])
def clients():
    print(request.form)
    json_data = request.get_json()
    print(json_data)

    if json_data != None:
        if  json_data['device'] == 'ACTUATOR' and json_data['action'] == 'toggle':
            room = tools.get_room(json_data['room'])

            for device in room.devices:
                if device.name == json_data['name']:
                    device.toggle()
        #Probable fix
        elif json['device'] == 'ALGUMOUTRO':
            pass

        return 'done'

    ## gambs !!!!!!!!!!!!
    elif request.form['action'] == 'toggle':
        devices = tools.get_all_devices()

        for device in devices:
            if device.relay_board_number == int(request.form['args']):
                device.toggle()
                break

        return 'done'
    else:
        return 'fail modules'


@app.route('/client/room', methods=['GET', 'POST'])
def client_room():
    return json.dumps(tools.generate_all_room_status())


@app.route('/client/room/<name>', methods=['GET', 'POST'])
def client_room_name(name):
    return json.dumps(tools.get_room(name).devices_status())


@app.route('/modules', methods=['POST'])
def modules():
    json_data = request.get_json()

    print(json_data)

    for module in common.modules:
        if module.name == json_data['name']:
            module.process_data(json_data)
            break

    return 'thanks for being a moduled'



@app.route('/services/ifttt', methods=['POST'])
def ifttt_service():
    if request.method == 'POST':
        print(request.form)

        if request.form['api_key'] == 'testkey':
            if request.form['argument'] == 'door':
                relay = 1
            elif request.form['argument'] == 'light':
                relay = 0

            if request.form['action'] == 'toggle':
                board.toggle_relay(relay)
            elif request.form['action'] == 'on':
                board.on_relay(relay)
            elif request.form['action'] == 'off':
                pass

            return 'ok'
        else:
            return 'Invalid'
    else:
        return 'This service only accepts POST request'


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
