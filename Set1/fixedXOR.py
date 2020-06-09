def fixedXOR(bytes1, bytes2):
    if len(bytes1) != len(bytes2):
        print("passed bytes are not equal")
        return
    return b''.join( [ bytes([b1 ^ b2]) for b1, b2 in zip(bytes1, bytes2) ] )

if __name__ == "__main__":
    arg1 = bytes.fromhex('1c0111001f010100061a024b53535009181c')
    arg2 = bytes.fromhex('686974207468652062756c6c277320657965')
    print(fixedXOR(arg1, arg2).hex())
