from functions import *


def encrypt(input_text, e, n):
    text_nums = to_nums(input_text)
    encrypted_text_nums = [0] * len(text_nums)
    for i in range(len(encrypted_text_nums)):
        encrypted_text_nums[i] = pow(text_nums[i], to_bin(e), n)

    return encrypted_text_nums


def decrypt(text_nums, d, n):

    decrypted_text_nums = [0] * len(text_nums)
    for i in range(len(decrypted_text_nums)):
        decrypted_text_nums[i] = pow(text_nums[i], to_bin(d), n)

    decrypted_text = to_letters(decrypted_text_nums)
    print(decrypted_text_nums)
    return decrypted_text
