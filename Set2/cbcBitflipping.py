from ecbCutPaste import removeMeta, addMeta
from Cryptodome import Random
from aesCBC import AES_CBC

# Hack to import fixedXOR
import sys
import os
sys.path.append(os.path.realpath('../Set1'))
from fixedXOR import fixedXOR


def encrypt(message, aes):
    safeMessage = removeMeta(message, ';=')
    safeMessage = 'comment1=cooking%20MCs;userdata=' + \
        safeMessage + ';comment2=%20like%20a%20pound%20of%20bacon'
    encrypted = aes.encrypt(safeMessage.encode())
    return encrypted


def decryptCheck(cipherText, aes):
    message = aes.decrypt(cipherText)
    print(f'\nDecrypted message:\n{message}')
    if message.find(b';admin=true;') > -1:
        print('ADMIN ACCESS GRANTED')
    else:
        print('ADMIN ACCESS DENIED')


if __name__ == "__main__":
    aes = AES_CBC()
    cipherText = encrypt('A' * 32, aes)
    print(f'\nOriginal Ciphertext:\n{cipherText}')

    # Begin attack

    xorText = fixedXOR(b'A'*12, b';admin=true;')
    modifiedCipherText = cipherText[:32] + fixedXOR(cipherText[32:48], b'z %,(/|534$z' + b'\x00' * 4) + cipherText[48:]

    # End attack

    print(f'\nModified Ciphertext:\n{modifiedCipherText}')
    decryptCheck(modifiedCipherText, aes)
