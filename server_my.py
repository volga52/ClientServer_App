import socket
import sys
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message


def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    '''
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


class ServerConnect:
    def __init__(self, starts_param):
        self.sys_arg = starts_param
        self.listen_port = DEFAULT_PORT
        self.listen_address = ''
        self.is_valid = True

    def valid_port(self):
        try:
            if '-p' in self.sys_arg:
                self.listen_port = int(self.sys_arg[self.sys_arg.index('-p') + 1])
            else:
                self.listen_port = DEFAULT_PORT
            if self.listen_port < 1024 or self.listen_port > 65535:
                raise ValueError

        except IndexError:
            print('После параметра -\'p\' необходимо указать номер порта.')
            sys.exit(1)
        except ValueError:
            print(
                'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)

        return self.is_valid

    def valid_address(self):
        try:
            if '-a' in self.sys_arg:
                self.listen_address = self.sys_arg[self.sys_arg.index('-a') + 1]
            else:
                self.listen_address = ''

        except IndexError:
            print(
                'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
            sys.exit(1)

        return self.is_valid

    def connect(self):
        if self.valid_port() and self.valid_address():
            transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            transport.bind((self.listen_address, self.listen_port))

            # Слушаем порт

            transport.listen(MAX_CONNECTIONS)

            while True:
                client, client_address = transport.accept()
                try:
                    message_from_client = get_message(client)
                    print(message_from_client)
                    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
                    response = process_client_message(message_from_client)
                    # response = self.process_client_message(message_from_client)
                    send_message(client, response)
                    client.close()
                except (ValueError, json.JSONDecodeError):
                    print('Принято некорретное сообщение от клиента.')
                    client.close()


ServerConnect(sys.argv).connect()
