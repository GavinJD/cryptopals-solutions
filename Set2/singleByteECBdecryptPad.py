import random
import base64
from pkcs7Pad import pkcs7Pad, pkcs7Strip
from Cryptodome import Random
from Cryptodome.Cipher import AES
from singleByteECBdecrypt import findBlockSize
from ECoracle import isCBC


class EncryptionOracle:
    def __init__(self, unknownText):
        self.pad = Random.get_random_bytes(random.randint(1, 16))
        self.key = Random.get_random_bytes(AES.block_size)
        self.secret = unknownText
        self.aesECB = AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, text):
        paddedText = pkcs7Pad(self.pad + text + self.secret, AES.block_size)
        return self.aesECB.encrypt(paddedText)


def hardSingleByteDecrypt(oracle):
    # Step 1: Find blocksize
    blockSize = findBlockSize(oracle)
    print(f'Block size of Encryption Oracle is {blockSize}')

    # Step 2: Detect whether ECB is used
    mode = isCBC(oracle.encrypt(b'A' * blockSize * 2))
    print(f'Mode of Encryption is {mode}')

    # Step 3: Determine length of pad before text
    dummyString = b'A' * blockSize * 3
    newCipherText = oracle.encrypt(dummyString)
    checkBlock = b''  # Assume pad has no repeating blocks
    for i in range(0, len(newCipherText), blockSize):
        if newCipherText[i:i+blockSize] == newCipherText[i+blockSize:i+2*blockSize]:
            checkBlock = newCipherText[i:i+blockSize]
            break

    dummyString = b''
    startPos = -1
    while startPos == -1:
        dummyString += b'A'
        newCipherText = oracle.encrypt(dummyString)
        for i in range(0, len(newCipherText), blockSize):
            if newCipherText[i:i+blockSize] == checkBlock:
                startPos = i

    padLen = startPos - (len(dummyString) - blockSize)
    offset = blockSize - (padLen % blockSize)

    # Step 4: Begin byte by byte decryption
    message = b''
    messageLen = len(oracle.encrypt(b''))
    for _ in range(messageLen):
        dummyPad = b'A' * offset
        dummyString = dummyPad + b'A' * (messageLen - len(message) - 1)

        refDict = {}
        for j in range(256):
            refDict[bytes([j])] = oracle.encrypt(
                dummyString + message + bytes([j]))[startPos:startPos+messageLen]

        newCipherText = oracle.encrypt(
            dummyString)[startPos:startPos+messageLen]
        for k, v in refDict.items():
            if v == newCipherText:
                message += k

    return pkcs7Strip(message, blockSize)


if __name__ == "__main__":
    b64Data = open('12.txt', 'r').read().encode('utf-8')
    unknownText = base64.b64decode(b64Data)

    oracle = EncryptionOracle(unknownText)

    message = hardSingleByteDecrypt(oracle).decode()

    print('-' * 100)
    print(' '*45, 'MESSAGE')
    print('-' * 100)
    print(message)
    print('-' * 100)
