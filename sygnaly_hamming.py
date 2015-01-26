def hamming_encode(bits):
    x7 = bits[0]
    x6 = bits[1]
    x5 = bits[2]
    x3 = bits[3]
    x4 = (x5 + x6 + x7) % 2
    x2 = (x3 + x7 + x6) % 2
    x1 = (x3 + x5 + x7) % 2
    return [x7, x6, x5, x4, x3, x2, x1]

def hamming_decode(bits, is_recur=False):
    x7 = bits[0]
    x6 = bits[1]
    x5 = bits[2]
    x4 = bits[3]
    x3 = bits[4]
    x2 = bits[5]
    x1 = bits[6]

    check_x4 = (x5 + x6 + x7) % 2
    check_x2 = (x3 + x7 + x6) % 2
    check_x1 = (x3 + x5 + x7) % 2
    errcode = [
        (x4 + check_x4) % 2,
        (x2 + check_x2) % 2,
        (x1 + check_x1) % 2
    ]
    error_pos = bits2dec(errcode)
    if error_pos == 0:
        return [x7, x6, x5, x3]

    if is_recur:
        return False

    if error_pos == 1:
        x1 = negate(x1)
    elif error_pos == 2:
        x2 = negate(x2)
    elif error_pos == 3:
        x3 = negate(x3)
    elif error_pos == 4:
        x4 = negate(x4)
    elif error_pos == 5:
        x5 = negate(x5)
    elif error_pos == 6:
        x6 = negate(x6)
    elif error_pos == 7:
        x7 = negate(x7)
    return hamming_decode([x7, x6, x5, x4, x3, x2, x1], True)

def bits2dec(bits):
    bits.reverse()
    ans = 0
    for index, value in enumerate(bits):
        ans += (2 ** index) * value
    return ans

def negate(bit):
    if bit:
        return 0
    return 1


info = [1, 1, 1, 0]
print('Kodujemy:')
print(info)

print('Z modyfikacją jednego bitu:')
res = hamming_encode(info)
print(res) # zakodowane kodem Hamminga
res[5] = negate(res[5])
print(res) # zmodyfikowane dwa bity
print(hamming_decode(res)) # zła odpowiedź :(

print('Z modyfikacją dwóch bitów:')
res = hamming_encode([1, 1, 1, 0])
print(res) # zakodowane kodem Hamminga
res[0] = negate(res[0])
res[1] = negate(res[1])
print(res) # zmodyfikowane dwa bity
print(hamming_decode(res)) # zła odpowiedź :(