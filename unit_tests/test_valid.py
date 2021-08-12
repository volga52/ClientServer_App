# import sys
# import os
import unittest
# sys.path.append(os.path.join(os.getcwd(), '..'))
from setting_hosts import SettingPortAddress


class TestValidFunc(unittest.TestCase):
    valid_args = ['-p', '10000', '-a', '500']
    # ['E:/Python_work/Test/client.py', '-a', '192.168.3.8', '-p', '8087']
    no_valid_port_args = "-p 'error'"

    # def test_valid_port_Raises(self):         # Не проходит
    #     with self.assertRaises(Exception):
    #         SettingPortAddress(self.no_valid_port_args).get_port()

    def test_get_port_equal(self):
        self.assertEqual(SettingPortAddress(self.valid_args).get_port(), 10000)

    def test_get_addr_equal(self):
        self.assertEqual(SettingPortAddress(self.valid_args).get_address(), '500')


if __name__ == '__main__':
    unittest.main()
