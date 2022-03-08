#*******************************************************************************
# Filename: test_enigma.py
# Language: Python
# Author: nathantoner
# Created: 2022-03-08
#
# Description:
# Tests for the enigma machine.
#
#*******************************************************************************


import unittest
from enigma import Enigma


class TestEnigma(unittest.TestCase):

    enigma_nums = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    enigma1 = Enigma(['I', 'II', 'III'], [0, 0, 0], ['a', 'a'])  # basic enigma

    def test_message(self):
        message = 'hello world'
        pre_processesd = ''.join(message.upper().split())
        cipher = enigma(message)
        enigma.reset()
        decoded = enigma(cipher)
        assert cipher == pre_processed

if __name__ == '__main__':
    unittest.main()


#*******************************************************************************
#                                END OF FILE
#*******************************************************************************
