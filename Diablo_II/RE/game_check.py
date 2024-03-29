from validation import createKeyHash

def decode_key(key):
    key = list(key)

    # Decoded: 0x13ac9741
    magicNumbers = [1, 0, 5, 3, 1, 1, 3, 5, 3, 2]
    mi = 0

    i = 0xf

    while True:

        c = key[i]

        # 0, 1, 2, 3, 4, 5, 6, 7
        if (c < '8'):
            
            if mi > 9:
                xorVal = 0
            else:
                xorVal = magicNumbers[mi]

            key[i] = chr(xorVal ^ ord(c))
            mi += 1

        # 8, 9
        elif (c < 'A'):
            key[i] = chr(i & 1 ^ ord(c))

        i -= 1
        if i < 0:
            break

    return "".join(key)

def shuffle_key(key):
    """
    GGGG-GGXX-YYGG-GGGG --> XXGG-GGGG-GGGG-GGYY
    """

    key = list(key)

    i = 0xf
    while True:

        temp = key[i]

        newIndex = i + 1 + 0x16 & 0xf

        key[i] = key[newIndex]
        key[newIndex] = temp

        i -= 1
        if i < 0:
            break

    return "".join(key)

def test_number_count(key):
    """
    Counts number of values 0-7
    """

    numberCount = 0
    for k in key:

        try:
            v = int(k)
            
            if v < 8:
                numberCount += 1

        except:
            pass

    return numberCount

def is_diablo_2_key(key):

    _, keyHash = createKeyHash(key)

    nC = test_number_count(keyHash)

    shuffle = shuffle_key(keyHash)
    code = decode_key(shuffle)

    if code[:2] == "06" or code[:2] == "07":
        return True

    return False