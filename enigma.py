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


class Wheel:
    """Defines a cipher wheel for the enigma machine."""

    WHEELS = {'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
              'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
              'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
              'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
              'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
              'VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
              'VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
              'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV'}
    NOTCHES = {'I': [16],
               'II': [21],
               'III': [4],
               'IV': [9],
               'V': [25],
               'VI': [12, 25],
               'VII': [12, 25],
               'VIII': [12, 25]}

    def __init__(self, wheel_key, ring_setting=0, offset=0):
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

    def __call__(self, input, rotate=False):
        """Runs the character through the wheel."""

        shift_next = False
        if rotate:
            self.shift_wheel()
            if self.offset in self.notch:
                shift_next = True
            if self.offset > 25:
                self.offset = 0  # reset at Z
        if isinstance(input, str):
            index = string.ascii_uppercase.index(input.upper())
        elif isinstance(input, int):
            index = input
        else:
            index = int(input)
        return self.output[index], shift_next

    def __repr__(self):
        return self.output

    def shift_wheel(self, shift=1):
        """Shifts the wheel by the shift value."""

        self.output = self.output[shift:] + self.output[:shift]
        self.offset += shift

    def set_offset(self, offset):
        """Sets the offset to a specific value."""

        self.output = self.initial_output[offset:] + self.initial_output[:offset]
        self.offset = offset

class Enigma:
    """Defines the enigma machine."""

    # Define constants for the machine.

    def __init__(self, wheels, ring_settings, patch_lists, offsets=None):
        """Initializes the machine."""

        self.wheel_choices = wheels
        self.ring_settings = ring_settings
        self.init_patch_board(patch_lists)
        self.init_reflector()
        if offsets is None:
            offsets = [0] * len(wheels)
        self.wheels = []
        for wheel, ring, offset in zip(wheels, ring_settings, offsets):
            self.wheels.append(Wheel(wheel, ring, offset))

    def __call__(self, message: str, offsets: list = None):
        """Calls the machine on the provided message and returns the result.

        Removes spaces and capitalizes everything before operating.

        Args:
            message: string to encrypt/decrypt.

        Keyword Args:
            offsets: list of three offsets for the message wheels, each a
                number from 0-25. If None, leaves wheels as-is. Can also be
                set by calling set_offsets directly.

        Returns:
            message after running through the machine with provided settings.
        """

        # Convert to upper case and remove all white space.
        message = message.upper()
        message = ''.join(message.split())

        # Set the wheels up for the message, if a setting is specified.
        if offsets is not None:
            self.set_offsets(offsets)

        # Encode/decode the message.
        final_message = ''
        for char in message:
            # First run through patch board.
            if char in self.patches.keys():
                char = self.patches[char]

            # Next run through the wheels in the first direction.
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
            for i in range(len(self.wheels)):
                char, _ = self.wheels[-1 - i](char)
            final_message += char

        return final_message

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

    def init_patch_board(self, patch_lists):
        """Initialize patch board settings.

        Args:
            patch_lists: two lists mapping inputs (first list) to outputs
                (second list) for the patch board. Note that the resulting
                patches go both ways.
        """

        patch_a, patch_b = patch_lists
        patch_a_final = patch_a.upper() + patch_b.upper()
        patch_b_final = patch_b.upper() + patch_a.upper()
        self.patches = {a: b for a, b in zip(patch_a_final, patch_b_final)}

    def init_reflector(self):
        """Initialize reflector.

        The reflector maps all letters in pairs, allowing for the machine to
        decrypt it's own messages.
        """

        reflector_a = 'ABCDEFGHIJKLM'
        reflector_b = 'NOPQRSTUVWXYZ'
        refl_a_final = reflector_a.upper() + reflector_b.upper()
        refl_b_final = reflector_b.upper() + reflector_a.upper()
        self.reflector = {a: b for a, b in zip(refl_a_final, refl_b_final)}


#*******************************************************************************
#                                END OF FILE
#*******************************************************************************
