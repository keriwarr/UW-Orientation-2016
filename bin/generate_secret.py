#!/usr/bin/env python
import sys

def usage():
    sys.stdout.write('usage: {} [length]\n'.format(sys.argv[0]))

if __name__ == '__main__':
    import random

    length = 50
    if len(sys.argv) == 2:
        try:
            length = int(sys.argv[1])
        except ValueError:
            usage()
            sys.exit(2)
    elif len(sys.argv) > 2:
        usage()
        sys.exit(1)

    letters = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    randomized = list(random.SystemRandom().choice(letters) for i in range(length))

    sys.stdout.write('{}\n'.format(''.join(randomized)))
