import argparse
import sys

import logging
import logs.configs.config_host_log

from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS
from decos import log_decor


class SettingPortAddress:
    LOGGER = logging.getLogger('hosts')

    def __init__(self, sys_args):
        self.sys_arg = sys_args
        self.port_return = DEFAULT_PORT
        self.address_return = ''

    def logger(self):
        self.LOGGER.info(f"Входящие параметры '{' '.join(self.sys_arg[1:])}'")

    @log_decor
    def get_port(self):
        try:
            self.logger()                                           # log
            if '-p' in self.sys_arg:
                self.port_return = int(self.sys_arg[self.sys_arg.index('-p') + 1])
            if self.port_return < 1024 or self.port_return > 65535:
                raise ValueError

        except IndexError:
            self.logger()                                           # log
            print('После параметра -\'p\' необходимо указать номер порта.')
            sys.exit(1)
        except ValueError:
            self.logger()                                          # log
            print(
                'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)

        return self.port_return

    @log_decor
    def get_address(self):
        try:
            if '-a' in self.sys_arg:
                self.address_return = self.sys_arg[self.sys_arg.index('-a') + 1]
            else:
                self.address_return = ''

        except IndexError:
            self.logger()                                           # log
            print(
                # 'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
                'После параметра \'a\'- необходимо указать адрес.')
            sys.exit(1)

        return self.address_return
