import socket
import sys
import json
import logging

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR
from common.utils import get_message, send_message
from setting_hosts import SettingPortAddress as SPA
import logs.configs.cofig_server_log
# from decos import log


class ServerConnect:
    LOGGING = logging.getLogger('server')

    def __init__(self, starts_param):
        self.sys_arg = starts_param
        self.is_valid = True

    @staticmethod
    def process_client_message(message):

        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':

            return {RESPONSE: 200}
        LOG = logging.getLogger('server')
        LOG.error(f"failed message {message}")              # log
        return {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }

    def connect(self):
        listen_address = SPA(self.sys_arg).get_address()
        print(listen_address)
        listen_port = SPA(self.sys_arg).get_port()

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((listen_address, listen_port))

        # Слушаем порт
        transport.listen(MAX_CONNECTIONS)

        while True:
            client, client_address = transport.accept()
            try:
                message_from_client = get_message(client)

                self.LOGGING.info(f"Подключен клиент {message_from_client['user']['account_name']}")    # log

                print(message_from_client)
                # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
                response = self.process_client_message(message_from_client)

                send_message(client, response)
                client.close()
            except (ValueError, json.JSONDecodeError):
                self.LOGGING.error(f'error')
                print('Принято некорретное сообщение от клиента.')
                client.close()


if __name__ == '__main__':
    ServerConnect(sys.argv).connect()
