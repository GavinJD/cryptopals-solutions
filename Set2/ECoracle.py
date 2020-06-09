# An ECB/CBC oracle, that detects whether a text is encrypted with either AES ECB or AES CBC
import random
from aesCBC import AES_CBC
from Cryptodome import Random
from Cryptodome.Cipher import AES
from pkcs7Pad import pkcs7Pad

# Hack to import Set1 files, will show pylint error
import sys
import os
sys.path.append(os.path.realpath('../Set1'))
from detectAesECB import detectAesECB 

def isCBC(cipherText):
    _, score = detectAesECB([cipherText])
    return 'CBC' if score == 0 else 'ECB'
        

def randECBCBC(message):
    message = Random.get_random_bytes(random.randint(
        5, 10)) + message + Random.get_random_bytes(random.randint(5, 10))
    choice = random.randint(0, 1)
    cipherText = b''
    if choice == 1:  # CBC
        aesCBC = AES_CBC() # By default makes random key and iv
        cipherText = aesCBC.encrypt(message)
    else:  # ECB
        aesECB = AES.new(Random.get_random_bytes(16), AES.MODE_ECB)
        cipherText = aesECB.encrypt(pkcs7Pad(message, AES.block_size))
    return message, cipherText, 'CBC' if choice == 1 else 'ECB'


def isRepeating(message):
    blocks = [message[i:i+AES.block_size] for i in range(0,len(message), AES.block_size)]
    for i in range(len(blocks)):
        for j in range(len(blocks)):
            if i != j and blocks[i] != blocks[j]:
                return True
    return False


if __name__ == "__main__":

    text = open('/home/gavin/Downloads/text_files/alice29.txt').read()[:1000]
    wrong = ()
    for _ in range(100):

        message = (pkcs7Pad(text[random.randint(0,500):random.randint(501,1000)].encode('utf-8'), AES.block_size) * 2) # Multiply by 2 for repeating blocks
        message, cipherText, mode = randECBCBC(message)
        guess = isCBC(cipherText)
        print(f'TextSize - { str(0) * ( 4 - ( len(str(len(message))) ) ) + str(len(message)) }, Repeating Blocks Present? - {isRepeating(message)}, Mode - {mode}, Guess - {guess}, Correct? - {guess==mode}')