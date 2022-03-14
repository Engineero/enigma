#*******************************************************************************
# Filename: enigma.py
# Language: Python
# Author: nathantoner
# Created: 2022-03-08
#
# Description:
# Defines the enigma machine.
#
#*******************************************************************************


import string
import argparse


class Wheel:
    """Defines a cipher wheel for the enigma machine."""

    # Define wheel constants. Note I'm zero-indexing the alphabet for notches.
    WHEELS = {'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
              'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
              'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
              'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
              'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
              'VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
              'VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
              'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV'}
    NOTCHES = {'I': [16],  # Q
               'II': [4],  # E
               'III': [21],  # V
               'IV': [9],  # J
               'V': [25],  # Z
               'VI': [12, 25],  # M, Z
               'VII': [12, 25],  # M, Z
               'VIII': [12, 25]}  # M, Z

    def __init__(self, wheel_key, ring_setting=0, offset=0):
        if wheel_key not in self.WHEELS.keys():
            raise KeyError(f'Wheel "{wheel_key}" not found.')
        self.wheel_key = wheel_key
        self.output = self.WHEELS[wheel_key]
        self.notch = self.NOTCHES[wheel_key]
        self.ring_setting = ring_setting
        self.initial_offset = offset
        self.offset = 0
        self.shift_wheel(ring_setting)
        self.initial_output = self.output  # store in case we need it
        self.offset = 0  # reset the offset counter
        self.shift_wheel(offset)

    def __call__(self, input, rotate=False, reverse=False):
        """Runs the character through the wheel."""

        shift_next = False
        if rotate:
            self.shift_wheel()
            if self.offset - 1 in self.notch:
                shift_next = True
            if self.offset > 25:
                self.offset = 0  # reset at Z
        if reverse:
            index = self.output.find(input.upper())
            result = string.ascii_uppercase[index]
        else:
            index = string.ascii_uppercase.index(input.upper())
            result = self.output[index]
        return result, shift_next

    def __repr__(self):
        return self.output

    def shift_wheel(self, shift=1):
        """Shifts the wheel by the shift value."""

        self.output = self.output[shift:] + self.output[:shift]
        self.offset += shift

    def set_offset(self, offset):
        """Sets the offset to a specific value."""

        self.output = self.initial_output[offset:] + self.initial_output[:offset]
        self.initial_offset = offset
        self.offset = offset

    def reset(self):
        """Resets wheel to starting configuration."""

        self.set_offset(self.initial_offset)

class Enigma:
    """Defines the enigma machine."""

    # Define constants for the machine.
    REFLECTORS = {'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
                  'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
                  'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
                  'B_thin': 'ENKQAUYWJICOPBLMDXZVFTHRGS',
                  'C_thin': 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'}

    def __init__(self, wheels, ring_settings, patch_list, reflector='A',
                 offsets=None):
        """Initializes the machine."""

        self.wheel_choices = wheels
        self.ring_settings = ring_settings
        self.reflector_setting = reflector
        self.init_patch_board(patch_list)
        self.init_reflector()
        if offsets is None:
            offsets = [0] * len(wheels)
        self.wheels = []
        for wheel, ring, offset in zip(wheels, ring_settings, offsets):
            self.wheels.append(Wheel(wheel, ring, offset))

    def __call__(self, message: str):
        """Calls the machine on the provided message and returns the result.

        Removes spaces and capitalizes everything before operating.

        Args:
            message: string to encrypt/decrypt.

        Returns:
            message after running through the machine with provided settings.
        """

        # Convert to upper case and remove all white space.
        message = ''.join(message.upper().split())

        # Encode/decode the message.
        cipher = ''
        for char in message:
            # First run through patch board.
            if char in self.patches.keys():
                char = self.patches[char]

            # Next run through the wheels in the first direction.
            rotate_next = False
            for i, wheel in enumerate(self.wheels):
                if i == 0:
                    # Always rotate first wheel.
                    char, rotate_next = wheel(char, rotate=True)
                else:
                    # Check for rotating later wheels.
                    char, rotate_next = wheel(char, rotate_next)

            # Run the message through the reflector.
            char = self.reflector[char]

            # Run the message through the wheels the other way. No rotating.
            for wheel in self.wheels[::-1]:
                char, _ = wheel(char, reverse=True)
            
            # Run back through the patch board.
            if char in self.patches.keys():
                char = self.patches[char]
            cipher += char

        return cipher

    def __repr__(self):
        result = f'Message wheels: {self.wheels}\n'
        result += f'Reflector: {self.reflector}\n'
        result += f'Patch board: {self.patches}\n'
        return result

    def set_offsets(self, offsets: list):
        """Sets the message offsets for the cipher wheels.

        Args:
            offsets: list of offsets, 0-25, for each wheel.
        """

        # Set the wheels up for the message.
        for wheel, offset in zip(self.wheels, offsets):
            wheel.set_offset(offset)

    def reset(self):
        for wheel in self.wheels:
            wheel.reset()

    def init_patch_board(self, patch_lists):
        """Initialize patch board settings.

        Args:
            patch_lists: two lists mapping inputs (first list) to outputs
                (second list) for the patch board. Note that the resulting
                patches go both ways.
        """

        self.patches = {}
        for patch in patch_lists:
            self.patches[patch[0].upper()] = patch[1].upper()
            self.patches[patch[1].upper()] = patch[0].upper()

    def init_reflector(self):
        """Initialize reflector.

        The reflector maps all letters in pairs, allowing for the machine to
        decrypt it's own messages.
        """

        if self.reflector_setting not in self.REFLECTORS.keys():
            raise KeyError(f'Reflector key "{self.reflector_setting}" not found.')
        keys = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        vals = self.REFLECTORS[self.reflector_setting]
        self.reflector = {a: b for a, b in zip(keys, vals)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Enigma machine.')

    parser.add_argument('message', type=str,
                        help='Message to be run through the machine.')
    parser.add_argument('-w', '--wheels', nargs='+', type=str,
                        default=['I', 'II', 'III'],
                        help='List of wheels, in order, to be used in machine. Roman numerals I-VIII.')
    parser.add_argument('-r', '--rings', nargs='+', type=int,
                        default=[0, 0, 0],
                        help='Ring offset settings for wheels in machine. Integers 0-25.')
    parser.add_argument('-o', '--offsets', nargs='+', type=int,
                        default=[0, 0, 0],
                        help='Message offset settings for wheels in machine. Integers 0-25.')
    parser.add_argument('-p', '--patches', nargs='+', type=str,
                        default=['aa'],
                        help='Letter pairs to patch together. Default is "aa" or no patches.')

    # Run the machine on the message and return the cipher.
    args = parser.parse_args()
    enigma = Enigma(args.wheels, args.rings, args.patches, args.offsets)
    cipher = enigma(args.message)
    print(f'Encrypted message:\n{cipher}')


#*******************************************************************************
#                                END OF FILE
#*******************************************************************************
