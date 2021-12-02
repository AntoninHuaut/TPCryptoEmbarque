# FONTAINE Quentin, HUAUT Antonin
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import number
import time


# Questions
print("Avec ILOVEYOU, il y aura 2^(8*8) clés à tester en moyenne, ce qui fait beaucoup de clés à tester !, soit :", 2**64)
print("Taille de l'espace des clés 2^128 soit", 2**128, "\n")


def findKey(msg, strEnd):
    msgBytes = bytes(msg, encoding='ascii')
    key = get_random_bytes(16)
    keyNumber = number.bytes_to_long(key)
    strEnd = ''.join(str(format(ord(c), 'x')) for c in strEnd)

    while True:
        keyNumber += 1
        key = number.long_to_bytes(keyNumber)

        aesCipher = AES.new(key, AES.MODE_ECB)
        cipherMsg = aesCipher.encrypt(msgBytes)
        cipherHex = hex(number.bytes_to_long(cipherMsg))

        if cipherHex.endswith(strEnd):
            break

    return key, hex(number.bytes_to_long(key))


msg = 16*"x"
strEnd = "LOL"

print("Message :", msg)
t0 = time.perf_counter()
key, keyHex = findKey(msg, strEnd)
t1 = time.perf_counter()

print("Il a fallut", t1-t0, "secondes")
print("Clé trouvé (hash) :", keyHex)

aesCipher = AES.new(key, AES.MODE_ECB)
cipherMsg = aesCipher.encrypt(bytes(msg, encoding='ascii'))
cipherMsgNumber = number.bytes_to_long(cipherMsg)
cipherHex = hex(cipherMsgNumber)
print("Vérification - cipherMsgHex :", cipherHex)
print("Déchiffrement :", aesCipher.decrypt(cipherMsg).decode("utf-8"))
