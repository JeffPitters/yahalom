#!/usr/bin/python
import pyprimes
import random
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

def gcd(a,b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

def primitive_root(modulus):
    required_set = set(num for num in range (1, modulus) if gcd(num, modulus) == 1)
    for g in range(1, modulus):
        actual_set = set(pow(g, powers) % modulus for powers in range (1, modulus))
        if required_set == actual_set:
            return g
    return 0

def start():
    buf = int(random.random()*10000)
    t = pyprimes.next_prime(buf)
    buf = int(random.random()*10000)
    p = pyprimes.next_prime(buf)
    g = primitive_root(p)
    buf = divmod(g**t, p) 
    T = buf[1]
    return t, p, g, T

def create_key(A, b, p):
    buf = divmod(A**b, p)
    K = buf[1]
    h = SHA256.new()
    bytekey = str(K).encode()
    h.update(bytekey)
    return h.hexdigest()

def encrypt(key, msg):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encryptmsg = iv + cipher.encrypt(msg.encode())
    return b64encode(encryptmsg)

def decrypt(key, enc):
    enc = b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    decryptmsg = cipher.decrypt(enc[16:])
    return decryptmsg.decode('utf-8')

def gen():
    buf = int(random.random()*10000)
    h = SHA256.new()
    byte = str(buf).encode()
    h.update(byte)
    text = h.hexdigest()
    return text[0:16]