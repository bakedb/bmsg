# https://stuvel.eu/python-rsa-doc/usage.html for docs

import rsa

def generate_keys(length):
    public_key, private_key = rsa.newkeys(length)
    return public_key, private_key

def encrypt(message, public_key):
    encoded = message.encode('utf8')
    enc_message = rsa.encrypt(encoded, public_key)
    return enc_message

def decrypt(message, private_key):
    dec_message = rsa.decrypt(message, private_key)
    return message.decode('utf.8')