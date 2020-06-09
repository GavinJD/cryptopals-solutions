import base64

def hexToBase64(input_bytes):
    temp = bytes.fromhex(input_bytes)
    return base64.b64encode(temp)

if __name__ == "__main__":
    x = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    y = hexToBase64(x)
    print(y)
