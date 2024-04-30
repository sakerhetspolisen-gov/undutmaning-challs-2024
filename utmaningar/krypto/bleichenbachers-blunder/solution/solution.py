#!/usr/bin/env python3
import sys
import socket
from hashlib import sha1

KEY_SIZE = 1024
ASN1_SHA = b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14'

def read_until(soc: socket.socket, part: str) -> str:
    s = ''
    while part not in s:
        s += soc.recv(1<<16).decode('utf-8')
    return s

def icuberoot(n: int) -> int:
    low, high = 0, 1 << ((n.bit_length() + 2) // 3)
    while low < high:
        mid = (low + high) // 2
        if mid**3 < n:
            low = mid + 1
        else:
            high = mid
    return low

def craft_malicious_sig(msg: bytes) -> str:
    buf = b'\x00\x01\xff\00' + ASN1_SHA + sha1(msg).digest()
    buf += b'\x00' * ((KEY_SIZE // 8) - len(buf))
    return hex(icuberoot(int.from_bytes(buf, 'big')))[2:]


def main() -> int:
    if '--manual' in sys.argv:
        msg = input("Message: ")
        malicious_sig = craft_malicious_sig(bytes.fromhex(msg))
        print(f'Signature: {malicious_sig}')
        return 0
    if len(sys.argv) != 3:
        print(f'usage: {sys.argv[0]} IP PORT')
        print(f'       {sys.argv[0]} --manual')
        return 1
    ip, port = sys.argv[1], int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect((ip, port))
        soc.sendall(b'1\n')
        s = read_until(soc, 'Signatur: ')
        msg = next(l for l in s.splitlines() if l and all(c in '0123456789abcdef' for c in l))
        malicious_sig = craft_malicious_sig(bytes.fromhex(msg))

        print(f'Message:   {msg}')
        print(f'Signature: {malicious_sig}')

        soc.sendall((malicious_sig + '\n').encode('utf-8'))
        print(read_until(soc, 'undut{').rstrip())
    return 0

if __name__ == '__main__':
    sys.exit(main())
