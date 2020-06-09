from Cryptodome.Cipher import AES

from readBase64 import readBase64

def main():
    cipherText = readBase64('7.txt')
    aesECB = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB)
    print(aesECB.decrypt(cipherText).decode('utf8'))

if __name__ == "__main__":
    main()
