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
import numpy as np
from tqdm import tqdm
from enigma import Enigma


class TestEnigma(unittest.TestCase):

    enigma_nums = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def test_message(self):
        message = 'hello world'
        enigma = Enigma(['I', 'II', 'III'], [0, 0, 0], ['aa'])  # basic enigma
        pre_processed = ''.join(message.upper().split())
        cipher = enigma(message)
        assert cipher != pre_processed
        enigma.reset()
        decoded = enigma(cipher)
        assert decoded == pre_processed

    def test_random_enigma(self):
        num_machines = 1000
        print(f'Testing {num_machines} random Enigma machines...')
        for _ in tqdm(range(num_machines)):  # test random enigma machines
            # Set up the machine randomly with a random message.
            message = np.random.choice(list(self.alphabet), size=100, replace=True)
            message = ''.join(message).upper()
            wheels = np.random.choice(self.enigma_nums, size=3, replace=False)
            rings = np.random.randint(0, 25, size=(3,))
            offsets = np.random.randint(0, 25, size=(3,))
            patches = list(self.alphabet)
            np.random.shuffle(patches)
            patches = np.split(np.asarray(patches), 13)  # random letter pairings
            patches = [str(p[0]) + str(p[1]) for p in patches]

            # Create the machine and test it.
            enigma = Enigma(wheels, rings, patches, offsets)
            cipher = enigma(message)
            assert cipher != message
            enigma.reset()
            decoded = enigma(cipher)
            assert decoded == message

if __name__ == '__main__':
    unittest.main()


#*******************************************************************************
#                                END OF FILE
#*******************************************************************************
