#!/usr/bin/env python3

import argparse
import math

#binets
def fibonacci(n):
    return int(((1+math.sqrt(5))**n-(1-math.sqrt(5))**n)/(2**n*math.sqrt(5)))

def findremiander(n):
    i=2
    while n >= fibonacci(i):
        i += 1
    i -= 1
    return n-fibonacci(i), fibonacci(i)

def findremianderDict(n, d):
    i=0
    while n >= fibonacci(i+2):
        d[i] = 0
        i += 1
    i -= 1
    d[i] = 1
    return n-fibonacci(i+2), fibonacci(i+2)

def fibbencode(n):
    l = []
    while n != 0:
        n , f = findremiander(n)
        l.insert(0,f)
    return l

def fibbDecode(s):
    ret = 0
    for i in range(len(s)):
        if s[i] != "0":
            ret += fibonacci(i+2)
    return ret 

def buildDict(n):
    d = {}
    n
    while n != 0:
        n , f = findremianderDict(n, d)
    return d 

def buildBinStr(n):
    d = buildDict(n)
    ret = ""
    for _,v in d.items():
        ret += str(v)
    ret += "1"
    return ret

def bytesToFibBytes(l):
    acc = "".join([buildBinStr(x) for x in l])
    temp = int("0b1"+acc,2)
    length = 0
    while temp != 0:
        length += 1
        temp = temp >> 8
    b = int("0b1"+acc,2).to_bytes(length, byteorder="little")
    return b

def fibBytesToBytes(b):
    b = bin(int().from_bytes(b, byteorder="little"))[3:]
    l = []
    for x in b.split("11"):
        l.append(fibbDecode(x+"1"))
    return l[:-1]

def encodeWith0(b):
    b = [[256,x][x != 0] for x in b]
    return bytesToFibBytes2(b)

def decodeWith0(b):
    b = fibBytesToBytes2(b)
    return [[0,x][x != 256] for x in b]

def decodeWith0XOR(b):
    b = fibBytesToBytesXOR(b)
    return [[0,x][x < 256] for x in b]

def bytesToFibBytes2(l):
    acc = "".join([buildBinStr(x) for x in l])
    b = bytes()
    for i in range((len(acc)+7)//8):
        b += int("0b"+acc[i*8:i*8+8].ljust(8,'0'), 2).to_bytes(1, byteorder="little")
    return b

def fibBytesToBytes2(b):
    l = []
    bs = ""
    for i in range(len(b)):
        byte = int().from_bytes(b[i*1:i*1+1], byteorder="little")
        bs += f'{byte:08b}'
    
    for x in bs.split("11"):
        l.append(fibbDecode(x+"1"))
    return l[:-1]

def fibBytesToBytesXOR(b):
    l = []
    bs = ""
    for i in range(len(b)):
        byte = int().from_bytes(b[i*1:i*1+1], byteorder="little")
        bs += f'{byte:08b}'
    xorValue = 0xff
    for x in bs.split("11"):
        if fibbDecode(x+"1") == 256:
            temp = xorValue
        else:
            temp = fibbDecode(x+"1")^xorValue
        xorValue = ((int(x+"1",2)<<1)|1) & 0xFF
        #if temp > 255 or temp < 0:
            #print(f'xorvalue = {xorValue}, x = {x+"1"}, temp = {temp}')
        l.append(temp)
    return l[:-1]

l = []
for x in range(0,256):
    l.append(x)

assert decodeWith0(encodeWith0(l)) == l

l = [49,10]

assert decodeWith0(encodeWith0(l)) == l

testl = [1,2,3,4,5]
testb = b'\xd9\xd8\xc0'

def readfile(path):
    ret = None
    with open(path,"rb") as f:
        ret = f.read()
    return ret

def writefile(path,data):
    with open(path,"wb") as f:
        ret = f.write(data)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["encode", "decode", "xordec"], help="en/de-code")
    p.add_argument("input", help="which file to en/de-coded data")
    p.add_argument("output", help="where to write the en/de-coded data")
    
    args = p.parse_args()
    
    if args.action == "encode":
        writefile(args.output, encodeWith0(readfile(args.input)))
    elif args.action == "decode":
        writefile(args.output, bytes(decodeWith0(readfile(args.input))))
    else:
        writefile(args.output, bytes(decodeWith0XOR(readfile(args.input))))

