# from collections import namedtuple
#
# message = {'action': 'presence', 'time': 1628613105.5254085, 'user': {'account_name': 'Guest'}}
# mes_bad = {'action': 'presence', 'user': {'account_name': 'Guest'}}
#
# # a = ['action', 'time', 'user', {'account_name': 'Guest'}, 'presence']
# ab = ['action', 'time', 'user']
# ac = {'action': 'presence', 'user': {'account_name': 'Guest'}}
#
# _dict = mes_bad
#
# # print(message_tuple)
# # print(message_tuple_bad)
# # print(mes_null._replace(**mes_bad)._fields)
# test_error = []
#
# for i in ab:
#     if not mes_bad.get(i):
#         test_error.append(i)
#
# # for j in ac:
#
#
# print(test_error)
#
#
# # Message = namedtuple('Message', ['action', 'time', 'user'], defaults=None, rename=True)
# # mes_null = Message(None, None, None)
# #
# # message_tuple = mes_null._replace(**message)._asdict()
# # message_tuple_bad = mes_null._replace(**mes_bad)._asdict()
import argparse


def create_arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser
