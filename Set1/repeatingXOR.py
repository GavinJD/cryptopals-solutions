import fixedXOR
import binascii

def getInput():
    print("Enter message -")
    content =[]
    while True:
        try:
            line = input()
        except EOFError:
            break
        content.append(line)
    return content

def encodeRepeatingXOR(key, message):
    keyIterator = 0
    result = b''
    for byte in message:
        result += fixedXOR.fixedXOR(bytes([byte]), bytes([key[keyIterator]]))
        keyIterator = (keyIterator + 1) % len(key)
    return result

def main():
    key = "ICE".encode()
    message = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal".encode()

    cipherText = encodeRepeatingXOR(key, message)
    plainText = encodeRepeatingXOR(key, cipherText)
    print("Key:", key)
    print("Message:", plainText)
    print("CipherText:", binascii.hexlify(cipherText))

if __name__ == "__main__":
    main()
