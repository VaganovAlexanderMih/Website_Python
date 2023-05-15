from . import helpers
from PIL import Image


special_symbols = { 255: ".", 200: " ", 210: ",", 240: ":", 260: "!", 230: "?",
                    300: "-", 310: "'", 320: "(", 340: ")", 360: "0", 361: "1",
                    362: "2", 363: "3", 364: "4", 365: "5", 366: "6", 367: "7",
                    368: "8", 369: "9",
                  }


def VernamCipher(string_, key_path, output):
    # if first bits are nulls - delete
    helpers.delete_first_nulls(string_)

    # getting random key
    result_key = helpers.getting_random_key(string_, key_path)

    # formatting string
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
        # else xoring symbol's bits with key's bits
        cur_char_bin = bin(ord(string_[i]))[2:]
        xored_char = helpers.xor_char(
            cur_char_bin, bin(ord(result_key[i]))[2:])
        final_string += chr(int(xored_char, 2))
    # writing the line to output file
    crypted = open(output, "a+")
    crypted.write(final_string)
    crypted.write("\n")
    crypted.close()


def CaesarCipher(string_, offset, output):
    final_string = helpers.caesar_cipher_coder(string_, offset)
    # writing the line to output file
    crypted = open(output, "a+")
    crypted.write(final_string)
    crypted.write("\n")
    crypted.close()


def VigenereCipher(string_, key_path, output):

    # getting random key
    result_key = helpers.getting_random_key(string_, key_path)

    # cipher
    final_string = helpers.vigenere_cipher_coder(
        special_symbols, string_, result_key)
    # writing the line in output file
    crypted = open(output, "a+")
    crypted.write(final_string)
    crypted.write("\n")
    crypted.close()

def ColumnarCipher(string_, key_path, output):
    new_key = helpers.GettingKeyCrypto(key_path)
    
    # making key and string readable 
    if (string_.endswith("\n")):
        string_ = string_[:-1]
    if (new_key.endswith("\n")):
        new_key = new_key[:-1]

    if (len(string_) // len(new_key) <= len(new_key)):
        size = len(new_key)
    else:
        size = len(string_) // len(new_key)

    matrix = []

    # creating matrix

    for i in range(len(new_key)):
        temp_matrix = []
        for j in range(size):
            temp_matrix.append("-")
        matrix.append(temp_matrix)
    
    for i in range(len(string_)):
        matrix[i // len(new_key)][i % len(new_key)] = string_[i]
    
    # encoding the string using matrix and key
    new_string = ""
    sorted_key = sorted(new_key)
    for letter in sorted_key:
        index = new_key.index(letter)
        for j in range(len(matrix)):
            new_string += matrix[j][index]
    
    f = open(output, "+a")
    f.write(new_string)
    f.write("\n")
    f.close()
