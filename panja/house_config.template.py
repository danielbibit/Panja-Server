from panja import user
from panja import room
from panja.modules import relay_board
from panja.modules import sensor_board
from panja.devices import switch


board = relay_board.RelayBoard('http://esp-1', 'keyesp1', 'exordial_board', 4)
sensors = sensor_board.SensorBoard('http://esp-2', 'keyesp2', 'einstein', ['IR', 'TEMP', 'HUMI', 'PIR1'])

quarto_daniel = room.Room('quarto_daniel')
quarto_daniel.devices.append(switch.Switch('luz', board, 0))
quarto_daniel.devices.append(switch.Switch('porta', board, 1))

quarto_laura = room.Room('quarto_laura')
quarto_laura.devices.append(switch.Switch('luz', board, 2))

banheiro = room.Room('banheiro')
banheiro.devices.append(switch.Switch('luz', board, 3))

# # Hardcoded users
daniel = user.User('Daniel', 'danielnick', 'danie@mail.com', 'senha12345', True)
laura = user.User('Laura', 'laura', 'laura@email.com', 'senhafraca', False)
root = user.User('root', 'root', 'root@panja.com.br', 'root', True)
