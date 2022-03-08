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


class Enigma:
    """Defines the enigma machine."""

    # Define constants for the machine.
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

    def __init__(self, wheels, ring_settings, patch_lists):
        """Initializes the machine."""

        init_wheels(wheels, ring_settings)
        init_patch_board(patch_lists)
        init_reflector()

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

        # Run through patch board.
        patched = ''
        for char in message:
            if char in self.patches.keys():
                char = self.patches[char]
            patched += char

        # Set the wheels up for the message, if a setting is specified.
        if offsets is not None:
            self.set_offsets(offsets)

        # Run the message through the wheels, first direction.
        wheels_forward = ''
        for char in patched:
            rotate_next = False
            for i in range(len(self.wheels)):
                if i == 0:
                    # Always rotate first wheel.
                    self.message_wheels[i] = self._shift_wheel(self.message_wheels[i])
                    offsets[i] += 1
                else:
                    # Check for rotating later wheels.
                    if rotate_next:
                        self.message_wheels[i] = self._shift_wheel(self.message_wheels[i])
                        offsets[i] += 1
                        rotate_next = False
                if offsets[i] > 25:
                    offsets[i] = 0  # wrap at Z
                if offsets[i] is in self.notches[i]:
                    rotate_next = True
                index = string.ascii_lowercase.index(char.lower())
                char = self.message_wheels[i][index]
            wheels_forward += char

        # Run the message through the reflector.
        reflected = ''
        for char in wheels_forward:
            reflected += self.reflector[char]

        # Run the message through the wheels the other way. No rotating.
        final_message = ''
        for char in reflected:
            for i in range(len(self.wheels)):
                index = string.ascii_lowercase.index(char.lower())
                char = self.message_wheels[-1 - i][index]  # reverse order
            final_message += char

        return final_message

    def _shift_wheel(self, wheel, shift=1)
        """Shifts the input wheel by the shift value and returns."""
        return wheel[shift:] + wheel[:shift]

    def set_offsets(self, offsets: list):
        """Sets the message offsets for the cipher wheels.

        Args:
            offsets: list of offsets, 0-25, for each wheel.
        """

        # Set the wheels up for the message.
        self.offsets = offsets
        message_wheels = []
        for i, offset in enumerate(offsets):
            message_wheels[i] = self._shift_wheel(self.wheels[i], offset)
        self.message_wheels = message_wheels

    def init_patch_board(self, patch_lists):
        """Initialize patch board settings.

        Args:
            patch_lists: two lists mapping inputs (first list) to outputs
                (second list) for the patch board. Note that the resulting
                patches go both ways.
        """

        patch_a, patch_b = patch_lists
        patch_a_final = patch_a.extend(patch_b)
        patch_b_final = patch_b.extend(patch_a)
        self.patches = {a: b for a, b in patch_a_final, patch_b_final}

    def init_wheels(self, wheels, ring_settings):
        """Initialize rotor wheels.

        Choose the selected wheels in the selected order, then shift them by
        ring setting.

        Args:
            wheels: list of keys for the wheels, roman numerals I-VIII.
            ring_settings: list of offsets for rings, integers 0-25.
        """

        self.wheels = [WHEELS[wheel] for wheel in wheels]
        self.notches = [NOTCHES[wheel] for wheel in wheels]
        for i, ring in enumerate(ring_settings):
            self.wheels[i] = self._shift_wheel(self.wheels[i], ring)

    def init_reflector(self):
        """Initialize reflector.

        The reflector maps all letters in pairs, allowing for the machine to
        decrypt it's own messages.
        """

        reflector_a = 'ABCDEFGHIJKLM'
        reflector_b = 'NOPQRSTUVWXYZ'
        refl_a_final = reflector_a.extend(reflector_b)
        refl_b_final = reflector_b.extend(reflector_a)
        self.reflector = {a: b for a, b in zip(refl_a_final, refl_b_final)}


#*******************************************************************************
#                                END OF FILE
#*******************************************************************************
