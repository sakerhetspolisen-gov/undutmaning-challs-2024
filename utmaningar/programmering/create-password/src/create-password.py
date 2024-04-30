#!/usr/bin/python3

# Inspired by https://neal.fun/password-game/

import sys
import re
import random
import time
import os
import signal
import argparse

import user_account

def out(text="", end="\n"):
    print(text, end=end)
    sys.stdout.flush()

class PasswordChecker:
    def __init__(self, seed=None):
        if seed:
            random.seed(seed)
        else:
            random.seed(os.urandom(8))

        self.value = random.randint(100, 200)
        self.visitor_number = random.randrange(0x1000, 0x10000) * random.randrange(0x1000, 0x10000)
        self.time = time.time()
        self.rules = []
        self.hex = 0
        self.octal = 0

        for name in PasswordChecker.__dict__:  
            attr = getattr(self, name)
            if callable(attr) and name.startswith("check_"):
                self.rules.append([attr.__doc__, attr])

    def welcome(self):
        out('==========================================')
        out(f'Welcome, brave traveler #{self.visitor_number}!')
        out('==========================================\n')
        out('Thou art now able to create a new password that will allow thee access to this realm. May thy password be strong and true, lest thou wish to face the challenges that lie ahead.\n')
        out('Hear ye, hear ye! Heed these rules and waste not thy time with delay!\n')

    def check_min_length(self):
        '''Thy password shall consist of more than eight runes. Let no man sayeth otherwise!'''
        return len(self.password) > 8

    def check_max_length(self):
        '''Thou shalt not make thy password greater than 64 runes in length, lest ye anger the gods.'''
        return len(self.password) < 64

    def check_letters(self):
        '''Let thy password contain both upper and lower case letters.'''
        have_upper = have_lower = False
        for i in self.password:
            if i.islower():
                have_lower = True
            if i.isupper():
                have_upper = True
        return have_lower and have_upper

    def check_common(self):
        '''Thou shalt not use a common password. Be creative, or suffer the consequences!'''
        for s in ["password", "qwerty", "123456", "123123", "secret", "abcabc", "aaaaa", "11111", "asdf"]:
            if s in self.password.lower():
                rule = '''Thou shalt not use a common password, such as {seq}. Be creative, or suffer the consequences!'''
                return (False, rule.format(seq=s))
        return True

    def check_digits(self):
        '''Let thy password be made up of more than 10 digits, lest thou wish to be challenged by the guardians of this realm.'''
        self.digits = []
        for i in self.password:
            if i.isdigit():
                self.digits.append(int(i))
        return len(self.digits) > 10

    def check_letters2(self):
        '''Thy password shall have at least three lower case letters and five upper case letters, that thy strength may be known to all.'''
        upper = lower = 0
        for i in self.password:
            if i.islower():
                lower += 1
            if i.isupper():
                upper += 1
        return lower > 3 and upper > 5

    def check_hex(self):
        '''Let thy password contain a hexadecimal number (0x..), greater than one, lest ye wish to face the wrath of the vikings.'''
        if m := re.search(r'0x[0-9a-fA-F]+', self.password):
            self.hex = int(m.group(0), 16)
        return self.hex > 1

    def check_octal(self):
        '''Thy password shall also contain an octal number (0o..), greater than one, that all may know thy worth.'''
        if m := re.search(r'0o[0-7]+', self.password):
            self.octal = int(m.group(0), 8)
        return self.octal > 1

    def check_sum(self):
        '''Let the sum of all digit runes in thy password be equal to {value}, lest thou wish to face the challenges of the realm.'''
        ok = sum(self.digits) == self.value
        return (ok, self.check_sum.__doc__.format(value=self.value))

    def check_octal_hex_product(self):
        '''Thy password must have the octal number ({octal:#o}) multiplied with the hexadecimal number ({hex:#x}) equal to thy traveler number, that all may know thee as a true warrior of this land.'''
        ok = self.hex * self.octal == self.visitor_number
        return (ok, self.check_octal_hex_product.__doc__.format(octal=self.octal, hex=self.hex))

    def check_time(self):
        '''Verify thy password within three seconds, lest thou wish to be cast out into the wilderness! Haste, my friend, for time is of the essence in this realm.'''
        elapsed = time.time() - self.time
        return elapsed < 3.0

    def show_rules(self, count=3):
        for i, (doc, _) in enumerate(self.rules):
            if i>= count: break
            out(f"Rule {i+1}: {doc}")

    def verify(self, password):
        self.password = password
        for i, (doc, check) in enumerate(self.rules):
            res = check()
            if isinstance(res, tuple):
                doc = res[1]
                res = res[0]
            if not res:
                out(f"Rule {i+1} failed: {doc}")
                return False
            else:
                out(f"Rule {i+1} passed: {doc}")
        return True

def set_time_limit(seconds):
    def alarm(*_):
        raise SystemExit("Time out!")
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(seconds)

def main():
    if sys.version_info < (3,8):
        out("Python 3.8 or newer is required")
        return

    set_time_limit(20)

    parser = argparse.ArgumentParser(description='Verify password')
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('-l', '--list-rules', action='store_true')
    args = parser.parse_args()

    p = PasswordChecker(args.seed)

    if args.list_rules:
        p.show_rules(100)
        return

    p.welcome()

    # show rules in advance or only when failing?
    p.show_rules()

    while True:
        out("\nSpeak thy new password: ", end='')
        password = sys.stdin.readline().strip()
        out()

        if p.verify(password):
            out('Huzzah! Thy account hath been created with a password that will allow thee access to this realm: ' + user_account.get_account())
            return

if __name__ == "__main__":
    main()
