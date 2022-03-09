# enigma
A simulated Enigma machine based on the 1942 M3 and M4 Naval Enigma with eight
wheels to choose from.

## Installation
To install, clone the GitHub repo and pip install. A pip package is forthcoming.

```bash
$ git clone git@github.com:Engineero/enigma.git
$ cd enigma
$ pip install .
```

## Terminal Use
To use from the command line, change directory to `enigma/enigma/` and see

```bash
$ python enigma.py -h
```

for details on command line arguments. To encrypt a message with default
arguments, simply call:

```bash
$ python enigma.py "my message"
NUDVZWUFF
```

to see the encrypted text. To decrypt the cipher text, use the same settings
(in this case default):

```bash
$ python enigma.py NUDVZWUFF
MYMESSAGE
```

## Use in Code
For use in code, import the `Enigma` class and initialize it with wheels,
ring offsets, message offsets, and patch board settings (details below).

```python
from enigma import Enigma

my_enigma = Enigma(
    wheels=['I', 'II', 'III'],
    ring_settings=[0, 0, 0],
    patch_list=['ab', 'cd'],
    offsets=[0, 0, 0]
)
```

A message can then be encoded by calling the initialized machine:

```python
cipher = my_enigma('my message')
print(cipher)
# 'NUCVZWSFF'
```

Note that in this case, the message produced is different because we are using
(slightly) different settings than the default. The fact that it is not
dramatically different points to a weakness of the Enigma machine that allowed
it to be broken: similar machine settings produce similar results, and as
machine settings approach the settings used to generate a cipher, the decoded
text becomes more and more realistic (i.e., English or German or whatever was
encoded).

To decode the message using the same object, first you must reset it to its
initialized settings, then pass the cipher text through the machine to get
the decoded message:

```python
my_enigma.reset()
message = my_enigma(cipher)
print(message)
# MYMESSAGE
```

## Background
Not a history lesson, but the Enigma machine was a mechnical cipher used by
the Germans in World War II to secure messages. The cipher had some weaknesses,
and was ultimately cracked by the Allies, although doing so required some
serious math, really smart people, and the invention of new computing machines.

The machine works simliarly to an oldschool decoder ring or substitution cipher,
where an input letter is encoded as another letter based on the setting of an
encoding ring. Enigma takes it several steps further by introducing multiple
encoding (wheels) with vairous settings (ring offset and message offset) that
move as letters are input, and a patch board that swaps letters at the input and
output.

To encode a message, choose (typically three, but can be more) wheels from the
available 8 and optionally ring offsets (shifts the letter mapping per wheel),
message offsets (shifts the wheel's starting position, affecting letter
mapping and when the next wheel rotates), and patch board pairings (swaps
letters at input and output). Then the message is passed one letter at a time
through the machine and the resulting encoded letters are recorded and printed.
To recover the message, initialize the machine to the same settings as were used
to produce the cipher, and pass the encoded message through the machine.

For example, if we use the default settings in this script and pass the message
'hello world', we get:

```bash
$ python enigma.py "hello world"
YNKCQSMAJE
```

If we then pass this cipher back into the machine with default settings, we get:

```bash
$ python enigma.py YNKCQSMAJE
HELLOWORLD
```

Note that, true to the original, spaces and punctuation are not included, and
all letters are represented as uppercase.