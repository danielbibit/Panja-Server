import sys
import os
import threading
import time
import logging
from logging.handlers import RotatingFileHandler
import json

#Only for MY machine
sys.path.remove('/media/sf_Dropbox/Code/Python/Panja-Server')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import Flask
from flask import request
from flask import render_template

import panja
from panja import user
from panja import common
from panja import room
from panja import tools
from panja.modules import relay_board
from panja.modules import sensor_module_m1


app = Flask(__name__)

HOST, PORT = "panja-server", 9997

# Harcoded panja modules
board = relay_board.RelayBoard('http://esp-2', 'mykey', 'exordial_board', 4)
sensor = sensor_module_m1.SensorModule('http://esp-3', 'anotherfreakingkey', 'einstein')

# Hardcoded panja rooms
quarto_daniel = room.Room('quarto_daniel')
quarto_daniel.add_sensor(('einstein', 'IR'))
quarto_daniel.add_sensor(('einstein', 'TEMP'))
quarto_daniel.add_sensor(('einstein', 'HUMI'))
quarto_daniel.add_sensor(('einstein', 'PRESENCE')) 
quarto_daniel.add_actuator(('light', ('exordial_board', 0)))
quarto_daniel.add_actuator(('door', ('exordial_board', 1)))
        
quarto_laura = room.Room('quarto_laura')
quarto_laura.add_actuator(('light', ('exordial_board', 3)))

# Hardcoded users
daniel = user.User('Daniel', 'danielbibit', 'danielbibit@gmail.com', 'senha12345', True)
laura = user.User('Laura', 'laura', 'laura@email.com', 'senhafraca', False)
root = user.User('root', 'root', 'root@panja.com.br', 'root', True)

common.modules.append(board)
common.modules.append(sensor)

common.rooms.append(quarto_daniel)
common.rooms.append(quarto_laura)

common.users.append(daniel)
common.users.append(laura)
common.users.append(root)

def poller():
    while True:
        time.sleep(common.settings["POLL_INTERVAL"])

        for module in common.modules:
            module.sync()

        print('alive')
        # app.logger.info('alive')
        print(json.dumps(tools.generate_server_model(), sort_keys=True, indent=4))


def main():
    # handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)
    
    # logging.basicConfig(
    #     filename=common.PANJADIR + '/../logs/main.log', 
    #     level=logging.DEBUG, 
    #     format='%(levelname)s : %(asctime)s : %(message)s', 
    #     datefmt='%d/%m %H:%M'
    # )
    
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
    room_model = tools.generate_server_model()

    return render_template('layout.html', rooms=room_model)


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
    return app.send_static_file('webclient.html')


@app.route('/clients', methods=['GET', 'POST'])
def clients():
    print(request.form)
    print(request.args)
    # room = tools.get_room(request.form['room'])
    # room.  
    if request.args.get('action') == 'toggle':
        board.toggle_relay(int(request.args.get('args')))
        return 'done'
    elif request.form['action'] == 'toggle':
        board.toggle_relay(int(request.form['args']))
        return 'done'
    else:    
        return 'fail modules'


@app.route('/modules', methods=['POST'])
def modules():
    try:
        json_data = request.get_json()

        print(json_data)

        for module in common.modules:
            if module.name == json_data['name']:
                module.process_data(json_data)

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
    print(panja.__version__)
    app.run(host='0.0.0.0', threaded=True)
