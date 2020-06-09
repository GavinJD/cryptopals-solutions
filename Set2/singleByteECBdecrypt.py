import base64
from pkcs7Pad import pkcs7Pad, pkcs7Strip
from Cryptodome import Random
from Cryptodome.Cipher import AES
from ECoracle import isCBC


class EncryptionOracle:
    def __init__(self, unknownText):
        self.key = Random.get_random_bytes(16)
        self.secret = unknownText
        self.aesECB = AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, text):
        paddedText = pkcs7Pad(text + self.secret, AES.block_size)
        return self.aesECB.encrypt(paddedText)


def findBlockSize(oracle):
    dummyString = b''
    inputSizes = []
    prevLen = len(oracle.encrypt(dummyString))

    while len(inputSizes) < 2:
        dummyString += b'A'
        currLen = len(oracle.encrypt(dummyString))
        if currLen > prevLen:
            inputSizes.append(len(dummyString))
            prevLen = currLen

    blockSize = inputSizes[1] - inputSizes[0]
    return blockSize


def singleByteDecrypt(oracle):
    # Step 1: Find blocksize
    blockSize = findBlockSize(oracle)
    print(f'Block size of Encryption Oracle is {blockSize}')

    # Step 2: Detect whether encryption uses ECB
    mode = isCBC(oracle.encrypt(b'A' * blockSize * 2))
    print(f'Mode of Encryption is {mode}')

    # Step 3: Begin byte by byte decryption
    message = b''
    messageLen = len(oracle.encrypt(b''))

    for i in range(1, messageLen + 1):
        dummyBlock = b'A' * (messageLen - i)
        refDict = {}
        for j in range(256):
            refDict[bytes([j])] = oracle.encrypt(
                dummyBlock + message + bytes([j]))[:messageLen]

        newCipherText = oracle.encrypt(dummyBlock)[:messageLen]
        for k, v in refDict.items():
            if v == newCipherText:
                message += k

    return pkcs7Strip(message, AES.block_size)


if __name__ == "__main__":
    b64Data = open('12.txt', 'r').read().encode('utf-8')
    unknownText = base64.b64decode(b64Data)

    oracle = EncryptionOracle(unknownText)

    message = singleByteDecrypt(oracle).decode('utf-8')

    print('-' * 100)
    print(' '*45, 'MESSAGE')
    print('-' * 100)
    print(message)
    print('-' * 100)
