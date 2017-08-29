#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
class Util(object):

    def __init__(self):
        pass

    def encrypt(self, message):
        obj = AES.new("1a2b3c4d5e6f7g8z", AES.MODE_CBC, "1a2b3c4d5e6f7g8z")

        length = 32
        count = len(message)
        add = length - (count%length)
        message = message + ('\0' * add)
        passkey = obj.encrypt(message)
        return b2a_hex(passkey)

    def decrypt(self, passkey):
        obj = AES.new("1a2b3c4d5e6f7g8z", AES.MODE_CBC, "1a2b3c4d5e6f7g8z")
        message = obj.decrypt(a2b_hex(passkey))
        message = message.rstrip('\0')
        return message
