import singleByteXOR

def main():
    input_lines = open('4.txt', 'r').readlines()
    maxScore = 0
    hiddenText = ''
    for line in input_lines:
        try:
            byteLine = bytes.fromhex(line.strip())
            likelyText = singleByteXOR.breakSingleByteXOR(byteLine)[0]
            score = singleByteXOR.scoreText(likelyText)
            if score > maxScore:
                maxScore = score
                hiddenText = likelyText
        except ValueError:
            pass
    print(hiddenText)

if __name__ == "__main__":
    main()
