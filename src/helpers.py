import random
import string
from PIL import Image


def xor_char(char1_bin, char2_bin):
    final_str = ""
    final_arr = []
    first_arr = []
    second_arr = []
    for i in char1_bin:
        first_arr.append(i)
    for i in char2_bin:
        second_arr.append(i)
    first_arr.reverse()
    second_arr.reverse()
    for i in range(min(len(char1_bin), len(char2_bin))):
        final_arr.append((int(first_arr[i]) + int(second_arr[i])) % 2)
    final_arr.reverse()
    for i in final_arr:
        final_str += str(i)
    return final_str


def delete_first_nulls(cur_string):
    while cur_string[0] == "0" and not (int(cur_string) == 0):
        cur_string = cur_string[1:]
    return cur_string


def getting_random_key(string_, key_path):
    result_key = ""
    for i in range(len(string_)):
        letter = random.choice(string.ascii_letters)
        while (
            delete_first_nulls(
                xor_char(bin(ord(string_[i]))[2:], bin(ord(letter))[2:]))
            == "1011100"
            or delete_first_nulls(
                xor_char(bin(ord(string_[i]))[2:], bin(ord(letter))[2:])
            )
            == "1010"
            or delete_first_nulls(
                xor_char(bin(ord(string_[i]))[2:], bin(ord(letter))[2:])
            )
            == "1101"
        ):
            letter = random.choice(string.ascii_letters)
        result_key += letter
    key = open(key_path, "a+")
    key.write(result_key)
    key.write("\n")
    key.close()
    return result_key


def caesar_cipher_coder(string_, offset):
    if string_.endswith("\n"):
        string_ = string_[:-1]
    final_string = ""
    special_symbols = [ ".", " ", ",", ":", "!", "?", "-", "(", ")", "0", "1",
                        "2", "3", "4", "5", "6", "7", "8", "9", ";", "'",
                      ]
    for letter in string_:
        # if the symbol is in syntactic signs, then we set a fixed value
        if letter in special_symbols:
            final_string += letter
            continue

        # else we set chars with offset
        if letter.lower() == letter:
            letter_ind = ord(letter) - ord("a")
            letter_ind += offset
            letter_ind %= ord("z") - ord("a")
            letter_ind += ord("a")
        else:
            letter_ind = ord(letter) - ord("A")
            letter_ind += offset
            letter_ind %= ord("Z") - ord("A")
            letter_ind += ord("A")
        final_string += chr(letter_ind)
    return final_string


def vigenere_cipher_coder(special_symbols, string_, result_key):
    final_string = ""
    if string_.endswith("\n"):
        string_ = string_[:-1]
    for i in range(len(string_)):
        # if the symbol is in syntactic signs, then we set a fixed value
        if string_[i] in special_symbols.values():
            final_string += chr(
                list(
                    filter(lambda x: special_symbols[x] == string_[
                           i], special_symbols)
                )[0]
            )
            continue

        # else we using cipher algorithm on it
        if string_[i].lower() == string_[i]:
            letter_ind = ord(string_[i]) - ord("a")
            letter_ind += ord(result_key[i]) - ord("a")
            letter_ind %= ord("z") - ord("a")
            letter_ind += ord("a")
        else:
            letter_ind = ord(string_[i]) - ord("A")
            letter_ind += ord(result_key[i]) - ord("A")
            letter_ind %= ord("Z") - ord("A")
            letter_ind += ord("A")
        final_string += chr(letter_ind)
    return final_string


def getting_offset(inp, letter_counter, probability):
    count_symbols = 0
    for string in inp:
        for letter in string:
            # counting symbols
            count_symbols += 1
            if not (65 <= ord(letter) <= 90 or 97 <= ord(letter) <= 122):
                continue
            letter_counter[letter.lower()] += 1
    # getting probabilities
    for letter in letter_counter.keys():
        letter_counter[letter] /= count_symbols
        letter_counter[letter] *= 100
    offsets = []
    # getting probable offsets
    for letter in letter_counter:
        for ideal_letter in probability:
            if (
                letter_counter[letter] >= probability[ideal_letter] - 0.25
                and letter_counter[letter] <= probability[ideal_letter] + 0.25
            ):
                offsets.append(ord(letter) - ord(ideal_letter))
    offsets.sort()
    count = 0
    max_count = 0
    offset = 0
    # getting most possible offset option
    for i in range(len(offsets)):
        if i == 0:
            continue
        if offsets[i - 1] == offsets[i]:
            count += 1
        else:
            if count > max_count:
                max_count = count
                offset = offsets[i - 1]
            count = 0
    return offset


def GettingKeyCrypto(key_path):
    f = open(key_path, "r")
    key = f.readline()
    temp_key = []
    for letter in key:
        if (letter in temp_key):
            continue
        temp_key.append(letter)
    
    new_key = ""
    for letter in temp_key:
        new_key += letter
    return new_key

def GettingKeyDecode(key):
    temp_key = []
    for letter in key:
        if (letter in temp_key):
            continue
        temp_key.append(letter)
    
    new_key = ""
    for letter in temp_key:
        new_key += letter
    return new_key
