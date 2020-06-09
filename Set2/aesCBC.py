from pkcs7Pad import pkcs7Pad, pkcs7Strip
from Cryptodome import Random
from Cryptodome.Cipher import AES

# Hack to import Set1 files, will show pylint error
import sys
import os
sys.path.append(os.path.realpath('../Set1'))
from fixedXOR import fixedXOR
from readBase64 import readBase64


class AES_CBC:
    def __init__(self, key=None, iv=None):
        self.key = key if key else Random.get_random_bytes(AES.block_size)
        self.iv = iv if iv else Random.get_random_bytes(AES.block_size)
        self.ecb = AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, message):
        message = pkcs7Pad(message, AES.block_size)
        blocks = [message[i:i+AES.block_size]
                  for i in range(0, len(message), AES.block_size)]

        cipherText = b""
        prevCipher = self.iv
        for block in blocks:
            block = fixedXOR(block, prevCipher)
            prevCipher = self.ecb.encrypt(block)
            cipherText += prevCipher
        return cipherText

    def decrypt(self, cipherText):
        blocks = [cipherText[i:i+AES.block_size]
                  for i in range(0, len(cipherText), AES.block_size)]

        message = b""
        message += fixedXOR(self.ecb.decrypt(blocks[0]), self.iv)
        for i in range(1, len(blocks)):
            tmp = self.ecb.decrypt(blocks[i])
            message += fixedXOR(blocks[i-1], tmp)

        return pkcs7Strip(message, AES.block_size)


if __name__ == "__main__":
    cipherText = readBase64('10.txt')

    key = b'YELLOW SUBMARINE'
    iv = b'\00' * AES.block_size
    cbc = AES_CBC(key, iv)
    message = cbc.decrypt(cipherText)

    print('Message is:')
    print(message.decode('utf-8'))
