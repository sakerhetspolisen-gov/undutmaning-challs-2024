#!/usr/bin/python3
import os
import sys
import re
import socket
import time
import math

def sendline(sock, line):
    print(line)
    sock.send(line.encode() + b'\n')

def recvuntil(sock, what):
    what = what.encode()
    buf = bytearray()
    while b := sock.recv(1):
        buf += b
        if buf.endswith(what):
            break
    print(buf.decode())
    return buf.decode()

def find_factors(n):
    max = int(math.sqrt(n) + 1)
    for i in range(2, max):
        if n % i == 0:
            return [i, n // i]
    return []

def main():
    if len(sys.argv) != 3:
        print("Usage: solve.py host port")
        return

    host, port = sys.argv[1], int(sys.argv[2])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    prompt = "Enter new password: "
    prompt = "Speak thy new password: "
    
    welcome = recvuntil(s, prompt)
    m = re.search(r'traveler #(\d+)!', welcome)
    if not m:
        print("traveler not found")
        return
    
    visitor_number = int(m.group(1))
    print("Visitor number: ", visitor_number)
    
    password = "azax12611156812aAXAYAZA"
    sendline(s, password)
    output = recvuntil(s, prompt)

    # Rule 11. octal * hex = visitor number
    # - octal > 1 and hex > 1
    octal_number, hex_number = find_factors(visitor_number)
    if octal_number * hex_number != visitor_number:
        print("Bad product")
        return

    password += f"0x{hex_number:x}.0o{octal_number:o}."
    sendline(s, password)
    output = recvuntil(s, prompt)

    m = re.search(r'equal to (\d+)', output)
    if not m:
        print("Sum not found")
        return
    
    wanted_sum = int(m.group(1))
    print("Wanted sum: ", wanted_sum)

    total = sum([int(x) for x in password if x.isdigit()]) 

    while (diff := wanted_sum - total) > 0:
        if diff > 9:
            diff = 9
        total += diff
        password += str(diff)

    sendline(s, password)

    recvuntil(s, prompt)

main()

