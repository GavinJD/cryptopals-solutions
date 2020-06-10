from Cryptodome.Random import get_random_bytes
from Cryptodome.Random.random import randint
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Util.strxor import strxor, strxor_c
from Cryptodome.Cipher import AES

KEY = get_random_bytes(AES.block_size)

def encryption_oracle():
    with open('17.txt', 'rb') as text_file:
        lines = text_file.readlines()
        choice = lines[randint(0, len(lines) - 1)]
        print(f'Selected before pad: {choice}')
        choice = pad(choice, AES.block_size)
        print(f'Selected: {choice}')
        aes = AES.new(KEY, AES.MODE_CBC)
        return (aes.encrypt(choice), aes.iv)


def decryption_oracle(ciphertext, iv):
    aes = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted = aes.decrypt(ciphertext)
    try:
        decrypted = unpad(decrypted, AES.block_size)
    except ValueError:
        return False
    return True


if __name__ == "__main__":
    encrypted_message, iv = encryption_oracle()

    secret = b''
    attacked_message = iv + encrypted_message 
    for i in range(0, len(attacked_message) - AES.block_size, AES.block_size):  # For each block
        decrypted_block = b''

        for j in range(AES.block_size-1, -1, -1):  # For every char in block
            padding_bit = AES.block_size - j
            # Get block to XOR with
            xor_block = strxor_c(decrypted_block, padding_bit)
            # TODO: Figure out why random bytes were better than just a single byte repeated
            xor_block = get_random_bytes(AES.block_size - len(xor_block)) + xor_block

            # Try every bit till padding satisfies
            new_attacked = attacked_message[:i] + \
                strxor(attacked_message[i:i+AES.block_size], xor_block) + \
                attacked_message[i+AES.block_size:i+2*AES.block_size]
            attacked_iv = new_attacked[:AES.block_size]
            attacked_ciphertext = new_attacked[AES.block_size:]
            
            while not decryption_oracle(attacked_ciphertext, attacked_iv):
                xor_block = xor_block[:j] + \
                    bytes([(xor_block[j] + 1) % 256]) + xor_block[j+1:]

                new_attacked = attacked_message[:i] + \
                strxor(attacked_message[i:i+AES.block_size], xor_block) + \
                attacked_message[i+AES.block_size:i+2*AES.block_size]
                attacked_iv = new_attacked[:AES.block_size]
                attacked_ciphertext = new_attacked[AES.block_size:]
    
            decrypted_block = bytes([xor_block[j] ^ padding_bit]) + decrypted_block
        secret += decrypted_block
        print(f'Block decrypted:{decrypted_block}')
    
    print(f'Attack success! Secret obtained is:\n{secret}')