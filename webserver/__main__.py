from flask import Flask
from flask import request
import json
import socket
app = Flask(__name__)

HOST, PORT = "panja-server", 9997

def tcp_send(data):
	print('entrei na funcao tcp_send')
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
		print('sending' + data)
		sock.connect((HOST, PORT))
		sock.sendall(data.encode())
		
		received = sock.recv(1024)
	except Exception as e:
		print(e)
	finally:
		sock.close()

dictionary = {
	'version' : 0,
	'name' : 'WEB',
	'user' : 'root@panja.com',
	'password' : 'root',
	'action' : '',
	'argument' : ''
}


@app.route('/services/ifttt', methods=['POST'])
def ifttt_service():
	if request.method == 'POST':
		print(request.form)

		if request.form['api_key'] == 'testkey':
			dictionary['action'] = request.form['action']
			dictionary['argument'] = request.form['argument']
			tcp_send(json.dumps(dictionary))
			return 'ok'
		else: 
			return 'nopnop'
	else:
		return 'fail'
