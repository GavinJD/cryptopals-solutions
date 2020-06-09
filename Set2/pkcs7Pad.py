def pkcs7Pad(message, blockSize):
    if len(message) % blockSize == 0:
        return message

    padLength = blockSize - (len(message) % blockSize)
    message += padLength * bytes([padLength])
    return message


def pkcs7Strip(message, blockSize):
    if message[-1] < blockSize:
        return message[:-message[-1]]
    else:
        return message

if __name__ == "__main__":
    message = b'email=michael_scott@dundermifflin.com&uid=60&role=user'
    padLength = 16
    padMessage = pkcs7Pad(message, padLength)
    strippedMessage = pkcs7Strip(message, padLength)
    print(f'Message before pad: {message}\nMessage after pad: {padMessage}\nMessage after removing pad: {strippedMessage}')