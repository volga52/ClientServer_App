"""Программа-клиент
Запускается с параметрами-аргументами в виде
client.py -a 192.168.1.2 -p 8079
"""

import sys
import json
import socket
import time
import logging

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
from config_network import SettingPortAddress as SPA, create_arg_parser
import logs.configs.config_client_log
import logs.configs.config_messages_log
from decos import Log


class Client:
    LOGGER = logging.getLogger('client')

    def __init__(self, start_param):
        self.sys_param = start_param

    @Log()
    def create_presence(self, account_name='Guest'):
        '''
        Функция генерирует запрос о присутствии клиента
        :param account_name:
        :return:
        '''
        # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }

        LOG_FUN = logging.getLogger('messages')
        LOG_FUN.info(f'Сформировано сообщение {out}')
        return out

    @Log()
    def process_ans(self, message):
        '''
        Функция разбирает ответ сервера
        :param message:
        :return:
        '''
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            return f'400 : {message[ERROR]}'
        raise ValueError

    def connect(self):
        param_network = SPA(create_arg_parser())
        server_address = param_network.get_address()
        server_port = param_network.get_port()

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = self.create_presence()
        send_message(transport, message_to_server)
        try:
            answer = self.process_ans(get_message(transport))
            print(answer)
            self.LOGGER.info(f"Сервер {server_address} ответ'{answer}' ")   # log
        except (ValueError, json.JSONDecodeError):
            error_mess = 'Не удалось декодировать сообщение сервера.'
            self.LOGGER.error(error_mess)                                   # log
            print(error_mess)


def test_launcher():
    test_class = Client(sys.argv)
    while True:
        test_class.connect()
        input()


if __name__ == "__main__":
    Client(sys.argv).connect()
    # test_launcher()       # Для демонстрации launcher строку 74 закомментировать
