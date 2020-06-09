import fixedXOR
import binascii
import base64 
from singleByteXOR import breakSingleByteXOR
from repeatingXOR import encodeRepeatingXOR
from readBase64 import readBase64

def hammingDistance(bytes1, bytes2): 
    xorSum = fixedXOR.fixedXOR(bytes1, bytes2)
    xorSumBin = bin(int(binascii.hexlify(xorSum), 16))[2:]
    distance = len([bit for bit in xorSumBin if bit == '1'])
    return distance

def getKeySize(input_bytes, start, end):
    minDistance = 100000
    keySize = 0
    for i in range(start, end):

        blocks = [input_bytes[j:j+i] for j in range(0, len(input_bytes) - i, i)]
        distances = [hammingDistance(blocks[j], blocks[(j+1)%len(blocks)]) for j in range(len(blocks))]
        normalizedDistance = sum(distances) / (len(distances) * i)

        if normalizedDistance < minDistance:
            minDistance = normalizedDistance
            keySize = i
    return keySize

def breakRepeatingXOR(cipherText, keySize):
    blocks = []
    key = ""
    for _ in range(keySize):
        blocks.append(b'')
    for bytePos in range(len(cipherText)):
        blocks[bytePos % keySize] += bytes([ cipherText[bytePos] ])
    for block in blocks:
        key += str(breakSingleByteXOR(block)[1])
    return key

def main():
    cipherText = readBase64('6.txt')

    keySize = getKeySize(cipherText, 2, 40)
    key = bytes(breakRepeatingXOR(cipherText, keySize), 'utf8')
    plainText = encodeRepeatingXOR(key, cipherText)
    print(f"KeySize: {keySize}\nKey: {key.decode('utf8')}\nPlain Text: {plainText.decode('utf8')}\n\n")

if __name__ == "__main__":
    main()
