#!/usr/bin/env python3

import sys
import time


class Viking:
    key = "Ragnar Lodbrok"
    goal = "Power is dangerous. It corrupts the meetest and attracts the worst. Power is only granted to those who prepared to lower themselves to pick it up."
    valid_output_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.? '
    valid_key_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '

    def print(self, msg='', *, end=None, flush=False, printable=True):
        if printable:
            msg = ''.join((c if c in self.valid_output_chars else '.') for c in msg)
        msg += '\n' if end is None else end
        sys.stdout.write(msg)
        if flush:
            sys.stdout.flush()

    def clear_screen(self):
        sys.stdout.buffer.write(b'\x1b[H\x1b[2J')

    def prompt(self):
        self.print("Who thou? ", end='', flush=True)
        key = input()
        if key:
            if not self.is_sane_key(key):
                print("Thou has entered an incorrect character that doth not compute with mine XOR-logic.\nAdieu!")
                key = None
        return key

    def scramble(self, msg, key):
        if not key:
            return msg
        key = key.encode()
        msg = msg.encode()
        arr = [c ^ key[i % len(key)] for i, c in enumerate(msg)]
        return ''.join(map(chr, arr))

    def is_sane_key(self, key):
        for c in key:
            if c not in self.valid_key_chars:
                return False
        return True

    def run(self):
        scrambled_goal = self.scramble(self.goal, self.key)
        key = ''

        while True:
            self.clear_screen()
            self.print(self.scramble(scrambled_goal, key))
            self.print()
            time.sleep(0.1)
            if key:
                if key == self.key:
                    f = open("flag.txt","r")
                    text = f.read()
                    f.close()
                    self.print(text, printable=False)
                    break

                print("I know not thou.")

            key = self.prompt()
            if key is None:
                break


if __name__ == '__main__':
    Viking().run()
