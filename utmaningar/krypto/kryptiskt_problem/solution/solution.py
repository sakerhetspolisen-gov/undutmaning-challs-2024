import os
import socket

def reveal(cryptogram, partial, length, offset):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("135.181.109.23", 29182))

    tosend = partial + (b"\x00" * 127)

    s.send(tosend)
    r = s.recv(length)

    if length > len(cryptogram):
        length = len(cryptogram)

    copy = bytearray()
    for i in range(offset, length):
        copy.append(cryptogram[i] ^ r[i])

    s.close()

    return copy

try:
    with open("data") as f:
        cryptogram = f.read()

        cryptogram = bytes.fromhex(cryptogram)

        p1 = reveal(cryptogram, b"", 127, 0)
        p2 = reveal(cryptogram, p1, 127 * 2, 127)
        p3 = reveal(cryptogram, p1 + p2, 127 * 3, 127 * 2)
        p4 = reveal(cryptogram, p1 + p2 + p3, 127 * 4, 127 * 3)
        p5 = reveal(cryptogram, p1 + p2 + p3 + p4, 127 * 5, 127 * 4)

        os.write(1, p1 + p2 + p3 + p4 + p5)

except Exception as e:
    print(f"failed {e}")
