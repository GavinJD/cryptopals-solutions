import fixedXOR
import string

def scoreText(text):
    # FREQUENCY TABLE
    freqTable =  {
            "e": 12.02, "t": 9.10, "a": 8.12, "o": 7.68,
            "i": 7.31, "n": 6.95, "s": 6.28, "r": 6.02,
            "h": 5.92, "d": 4.32, "l": 3.98, "u": 2.88,
            "c": 2.71, "m": 2.61, "f": 2.30, "y": 2.11,
            "w": 2.09, "g": 2.03, "p": 1.82, "b": 1.49,
            "v": 1.11, "k": 0.69, "x": 0.17, "q": 0.11,
            "j": 0.10, "z": 0.07, ' ': 3.00
            }

    score = 0
    for bit in text:
        if chr(bit) not in string.printable:
            return 0
        score += freqTable.get(chr(bit), 0)
    return score

def breakSingleByteXOR(cipherText):
    maxScore = 0
    plainText = ""
    key = 0
    for i in range(256):
        likelyKey = i
        likelyText = fixedXOR.fixedXOR( cipherText, b''.join( [ bytes([likelyKey]) ] * len(cipherText) ) )
        score = scoreText(likelyText)
        if maxScore < score:
            plainText = likelyText
            maxScore = score
            key = chr(likelyKey)
#     print(f"Cipher Text: {cipherText}\nPlain Text: {plainText}\n")
    return [plainText, key]


if __name__ == "__main__":
    cipherText = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    plainText, key = breakSingleByteXOR(cipherText)

    print("Plaintext:", plainText)
    print("Key:", key)
