#!/usr/bin/env python3
import random
from hashlib import sha1
from pathlib import Path
import subprocess

KEY_SIZE = 1024
ASN1_SHA = b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14'
SMALL_PRIMES = [p for p in range(2, 10000) if all(p % n != 0 for n in range(2, p))]

def miller_rabin(n: int) -> bool:
    if n < 2 or any(n % p == 0 for p in SMALL_PRIMES):
        return False
    s = n - 1
    t = 0
    while s % 2 == 0:
        s //= 2
        t += 1
    for _ in range(10):
        a = random.randrange(2, n - 1)
        v = pow(a, s, n)
        if v == 1:
            continue
        i = 0
        while v != n-1:
            if i == t-1:
                return False
            i += 1
            v = pow(v, 2, n)
    return True

def gen_rsa_prime(bits: int) -> int:
    while True:
        p = random.getrandbits(bits) | 1
        while p.bit_length() < bits:
            p = (p << 1) | 1
        if (p - 1) % 3 == 0:
            continue
        if miller_rabin(p):
            return p

def produce_signature(msg: bytes, d: int, n: int) -> int:
    padlen = (KEY_SIZE // 8) - 20 - 3 - len(ASN1_SHA)
    val = b'\x00\x01' + b'\xff' * padlen + b'\00' + ASN1_SHA + sha1(msg).digest()
    return pow(int.from_bytes(val, 'big'), d, n)

def verify_signature(msg: bytes, sig: int, n: int) -> bool:
    s = pow(sig, 3, n)
    m = s.to_bytes((s.bit_length() + 7) // 8, byteorder='big')
    i = next((x for x in range(len(m)) if m[x] != 0), None)
    if i is None or m[i] != 1:
        return False
    i = next((x for x in range(i, len(m)) if m[x] == 0), None)
    if i is None or m[i+1:][:len(ASN1_SHA)] != ASN1_SHA:
        return False
    return m[i+1+len(ASN1_SHA):][:20] == sha1(msg).digest()

def main() -> None:
    p = gen_rsa_prime(KEY_SIZE)
    q = gen_rsa_prime(KEY_SIZE)
    d = pow(3, -1, (p-1) * (q-1))
    n = p * q

    test_sig = produce_signature(b'hello world', d, n)
    assert verify_signature(b'hello world', test_sig, n)

    print('- Hörrudu! Du ser inte ut som herr Bleicenbacher.')
    print('- Och vad är det för konstig hjälm du har på dig?')
    print()
    print('"Sticker de sig inte på de där hornen?" tänker vakten..')
    print()
    print('- För att komma in här måste du minsann bevisa att du är den du säger du är!')
    print('- Som du känner till använder vi RSA för identifiering här på fortet.')
    print('- Vi är dessutom effektiva och använder e=3 som publik exponent!')
    print('- För att släppa in dig måste du visa mig en giltig signatur, signerat med Bleichenbacher\'s nyckel!')
    print()
    print('1) Ge signatur')
    print('2) Fråga om Haralds RSA konfiguration')
    print('3) Spring iväg i panik')

    for _ in range(3):
        option = input('\nVad vill du göra? ').strip()
        print()
        if option not in ['1', '2', '3']:
            print('Ogiltigt val! Skriv 1, 2, eller 3.')
            continue
        if option == '3':
            print('Du springer iväg så snabbt du kan!')
            print('Vakten stirrar fundersamt men orkar inte springa efter..')
            return
        if option == '2':
            print('Vakten svarar glatt:')
            print('- Algoritm:', 'RSA PKCS1.5, e=3')
            print('- Nyckelstorlek:', KEY_SIZE)
            print('- Kommunikationsformat:', 'hexkodat, big endian')
            print('- Bleichenbachers publika nyckel:', hex(n)[2:])
            continue
        msg = random.randbytes(32)
        print('- Om du nu är Bleichenbacher, signera detta meddelande med hans privata nyckel!')
        print(msg.hex())
        sigstr = input('\nSignatur: ').strip()
        print()
        try:
            if sigstr.startswith('0x'):
                sigstr = sigstr[2:]
            if len(sigstr) % 2 != 0:
                sigstr = '0' + sigstr
            sig = bytes.fromhex(sigstr)
        except ValueError:
            print('- Det där ser inte ut som en hexsträng...')
            return

        if not verify_signature(msg, int.from_bytes(sig, 'big'), n):
            print('- Ogiltig signatur! Stick i väg innan jag slänger dig i finkan.')
            return
        print('- Signaturen stämmer! Förlåt herr Bleichenbacher, välkommen in!')
        print((Path(__file__).parent / 'flag.txt').read_text().strip())
        return
    print('- Tillräckligt med frågor från dig! Stick iväg.')

if __name__ == '__main__':
    main()
