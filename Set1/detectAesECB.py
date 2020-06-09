from Cryptodome.Cipher import AES
from singleByteXOR import scoreText
import binascii

def detectAesECB(bytes_list):
    maxRepeat = 0
    probableLine = 0
    for line in bytes_list:
        blocks = [ line[i:i+AES.block_size] for i in range(0, len(line), AES.block_size) ]
        for i in range(len(blocks)):
            repeatCount = 0
            for j in range(len(blocks)):
                if i != j and blocks[i] == blocks[j]:
                    repeatCount += 1
            if repeatCount > maxRepeat:
                maxRepeat = repeatCount
                probableLine = line
    return (probableLine, maxRepeat)

def main():
    cipherFile = open('8.txt', 'r')
    fileContent_hex = cipherFile.readlines()
    fileContent = list(map(bytes.fromhex, fileContent_hex))

    line, score = detectAesECB(fileContent)
    print(f"Line: {binascii.hexlify(line)}\nScore: {score}\nLine: {fileContent.index(line) + 1}")

if __name__ == "__main__":
    main()
