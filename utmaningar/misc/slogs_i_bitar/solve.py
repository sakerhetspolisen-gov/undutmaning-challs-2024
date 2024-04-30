#!/bin/env python3
import sys
from PIL import Image


def main(args):
    chall = Image.open(args[0])
    result = bytes()
    for y in range(chall.height):
        for x in range(chall.width):
            p = chall.getpixel((x, y))
            lsb = p & 1
            if lsb == 0:
                # Extract text
                result += int(f'{p:08b}'[::-1], 2).to_bytes(1, 'big')
            else:
                # Extract bunny
                chall.putpixel((x, y), 0x00)

    text = result.decode('ascii')
    # Optional remove padding
    text = text[0:text.find('THISISJUSTPADDINGPLEASEIGNORE')]
    print(text)
    chall.show()


if __name__ == "__main__":
    main(sys.argv[1:])
