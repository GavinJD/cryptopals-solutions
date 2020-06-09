import base64

def readBase64(fileName):
    inputFile = open(fileName, 'r')
    fileContent_b64 = inputFile.read().encode('utf8')
    fileContent = base64.b64decode(fileContent_b64)

    return fileContent
