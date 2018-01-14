import os
import sys
import time
import threading
import json
import logging
from logging.handlers import RotatingFileHandler

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask import request
from flask import render_template

from panja import user
from panja import common
from panja import room
from panja import tools
from panja.modules import relay_board
from panja.modules import sensor_module_m1
from panja.devices import switch


app = Flask(__name__)

sensors = 's'
board = relay_board.RelayBoard('http://esp-2', 'mykey', 'exordial_board', 4)

quarto_daniel = room.Room('quarto_daniel')
quarto_daniel.devices.append(switch.Switch('luz', board, 0))
quarto_daniel.devices.append(switch.Switch('porta', board, 1))

quarto_laura = room.Room('quarto_laura')
quarto_laura.devices.append(switch.Switch('luz', board, 2))

banheiro = room.Room('banheiro')
banheiro.devices.append(switch.Switch('luz', board, 3))

# # Hardcoded users
daniel = user.User('Daniel', 'danielbibit', 'danielbibit@gmail.com', 'senha12345', True)
laura = user.User('Laura', 'laura', 'laura@email.com', 'senhafraca', False)
root = user.User('root', 'root', 'root@panja.com.br', 'root', True)


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

    engine = create_engine('sqlite:///' + os.getcwd() +  '/database.db')
    session = sessionmaker()
    session.configure(bind=engine)

    poller_thread = threading.Thread(target=poller)
    poller_thread.daemon = True
    poller_thread.start()
    print('Poller thread started in: ' + poller_thread.name)

    print('Main server started at: ' + time.asctime())

    app.run(host='0.0.0.0', threaded=True)


@app.route('/test', methods=['GET', 'POST'])
def test():
    room_model = tools.generate_all_room_status()
    return render_template('dashboard.html', rooms=room_model)


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

    return render_template('layout.html', rooms=room_model)


@app.route('/clients', methods=['POST'])
def clients():
    print(request.form)
    json_data = request.get_json()
    print(json_data)

    if json_data != None:
        if json_data['action'] == 'toggle' and json_data['device'] == 'ACTUATOR':
            room = tools.get_room(json_data['room'])

            for device in room.devices:
                if device.name == json_data['name']:
                    device.toggle()

        return 'done'
    ## gambs
    elif request.form['action'] == 'toggle':
        devices = tools.get_all_devices()

        for device in devices:
            if device.relay_board_number == int(request.form['args']):
                device.toggle()
                break

        return 'done'
    else:    
        return 'fail modules'


@app.route('/clients/rooms', methods=['GET','POST'])
def handle_room():
    return 'room'


@app.route('/clients/rooms/<idd>/<ccc>', methods=['GET','POST'])
def handle_room_idd(idd, ccc):
    return 'your romm ' + str(idd) + str(ccc)


@app.route('/modules', methods=['POST'])
def modules():
    try:
        json_data = request.get_json()

        print(json_data)

        for module in common.modules:
            if module.name == json_data['name']:
                module.process_data(json_data)
                break

        return 'thanks for being a moduled'
    except KeyError as e:
        return 'thanks for being a useless moduled'


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
