import math


def flip_num(num):
    return 0 if num != 0 else 1


def float_bin(number, places=3):
    whole, dec = str(number).split(".")
    whole = int(whole)
    dec = int(dec)
    res = bin(whole).lstrip("0b") + "."

    for x in range(places):
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res += whole

    return res


def decimal_converter(num):
    while num > 1:
        num /= 10
    return num


def gray_to_binary(gray):
    binary = str(gray[0])
    for i in range(1, len(gray)):
        binary += str(int(binary[i - 1]) ^ int(gray[i]))
    return binary


def binary_to_gray(binary):
    gray = str(binary[0])
    for i in range(1, len(binary)):
        gray += str(int(binary[i - 1]) ^ int(binary[i]))
    return gray


def gray_to_decimal(gray):
    binary = gray_to_binary(gray)
    return int(binary, 2)


def decimal_to_gray(decimal):
    binary = bin(decimal)[2:]
    return binary_to_gray(binary)


def encode(x, a, b, m):
    step = (math.pow(2, m) - 1) / (b - a)
    n = round((x - a) * step)
    code = decimal_to_gray(n)
    return code


def decode(code, a, b, m):
    step = (b - a) / (math.pow(2, m) - 1)
    n = gray_to_decimal(code)
    x = round(a + n * step, 2)
    return x 


def chars2ints(s):
    return [int(ch) for ch in s]
