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
import json
import numpy as np
from tqdm import tqdm
from pathlib import Path
from enigma import Enigma


class TestEnigma(unittest.TestCase):

    enigma_nums = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    reflectors = ['A', 'B', 'C', 'B_thin', 'C_thin']
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def test_message(self):
        """Test a known message."""

        print('\nTesting known message...')
        message = 'hello world'
        enigma = Enigma(['I', 'II', 'III'], [0, 0, 0], ['aa'])  # basic enigma
        pre_processed = ''.join(message.upper().split())
        cipher = enigma(message)
        assert cipher != pre_processed
        enigma.reset()
        decoded = enigma(cipher)
        assert decoded == pre_processed

    def test_random_enigma(self):
        """Randomly initializes a bunch of Enigmas and tests them."""

        num_machines = 100
        print(f'\nTesting {num_machines} random Enigma machines...')
        for _ in tqdm(range(num_machines)):  # test random enigma machines
            # Set up the machine randomly with a random message.
            message = np.random.choice(list(self.alphabet), size=705, replace=True)
            message = ''.join(message).upper()
            wheels = np.random.choice(self.enigma_nums, size=3, replace=False)
            reflector = np.random.choice(self.reflectors, size=1)
            rings = np.random.randint(0, 25, size=(3,))
            offsets = np.random.randint(0, 25, size=(3,))
            patches = list(self.alphabet)
            np.random.shuffle(patches)
            patches = np.split(np.asarray(patches), 13)  # random letter pairings
            patches = [str(p[0]) + str(p[1]) for p in patches]

            # Create the machine and test it.
            enigma = Enigma(wheels, rings, patches, offsets=offsets,
                            reflector=reflector[0])
            cipher = enigma(message)
            assert cipher != message
            enigma.reset()
            decoded = enigma(cipher)
            assert decoded == message

    def test_known_vectors(self):
        """Tests known cipher/message pairs encrypted with WWII Enigmas."""

        print('\nTesting known historical vectors...')
        path = Path(__file__).parent.absolute() / 'test_vectors.json'
        with open(path, 'r') as fp:
            data = json.load(fp)
        for vector in data['vectors']:
            enigma = Enigma(
                wheels=vector['rotors'],
                ring_settings=vector['ring_settings'],
                patch_list=vector['plugs'],
                reflector=vector['reflector'],
                offsets=vector['offsets']
            )
            cipher = enigma(vector['message'])
            assert cipher != vector['message']
            # TODO: remove debug prints
            print(cipher)
            print(''.join(vector['cipher'].split()))
            assert cipher == ''.join(vector['cipher'].split())
            enigma.reset()
            decoded = enigma(cipher)
            assert decoded == vector['message']

if __name__ == '__main__':
    unittest.main()


#*******************************************************************************
#                                END OF FILE
#*******************************************************************************
