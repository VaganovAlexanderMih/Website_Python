from . import helpers
from PIL import Image


def DecoderVernamCipher(input_path, key_path, output_path):
    # helpers
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
        if len(char1_bin) < len(char2_bin):
            for i in range(len(char1_bin), len(char2_bin)):
                final_arr.append(int(second_arr[i]))
        if len(char1_bin) > len(char2_bin):
            for i in range(len(char2_bin), len(char1_bin)):
                final_arr.append(int(first_arr[i]))
        final_arr.reverse()
        for i in final_arr:
            final_str += str(i)
        return final_str

    special_symbols = { 255: ".", 200: " ", 210: ",", 240: ":", 260: "!",
                        230: "?", 300: "-", 310: "'", 320: "(", 340: ")",
                        360: "0", 361: "1", 362: "2", 363: "3", 364: "4",
                        365: "5", 366: "6", 367: "7", 368: "8", 369: "9",
                      }

    # decoder
    key_file = open(key_path, "r")
    text = open(output_path, "a")
    with open(input_path) as inp:
        for string in inp:
            final_string = ""
            key = key_file.readline()
            # making key readable
            if key.endswith("\n"):
                key = key[:-1]
            if string.endswith("\n"):
                string = string[:-1]
            # decoding lines
            for i in range(len(string)):
                # if the symbol is in syntactic signs, then we set a fixed value
                if ord(string[i]) in special_symbols.keys():
                    final_string += special_symbols[ord(string[i])]
                    continue
                # else xoring symbol with key symbol
                cur_char_bin = bin(ord(string[i]))[2:]
                xored_char = xor_char(cur_char_bin, bin(ord(key[i]))[2:])
                final_string += chr(int(xored_char, 2))
            # writing the line to output_files
            text.write(final_string)
            text.write("\n")
    text.close()


def DecoderCaesarCipherWithKey(input_path, offset, output_path):
    offset = -offset
    uncrypted = open(output_path, "a")
    with open(input_path) as f:
        for string_ in f:
            # making string readable
            if string_.endswith("\n"):
                string_ = string_[:-1]
            final_string = helpers.caesar_cipher_coder(string_, offset)
            # writing the line to output file
            uncrypted.write(final_string)
            uncrypted.write("\n")
    uncrypted.close()


def DecoderCaesarCipherWithoutKey(input_path, output_path):
    # normal character distribution
    probability = { "a": 8.1, "b": 1.4, "c": 2.7, "d": 3.9, "e": 13, "f": 2.9,
                    "g": 2, "h": 5.2, "i": 6.5, "j": 0.2, "k": 0.4, "l": 3.4,
                    "m": 2.5, "n": 7.2, "o": 7.9, "p": 2, "q": 0.2, "r": 6.9,
                    "s": 6.1, "t": 10.5, "u": 2.4, "v": 0.9, "w": 1.5,
                    "x": 0.2, "y": 1.9, "z": 0.1,
                  }
    letter_counter = { "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0,
                       "h": 0, "i": 0, "j": 0, "k": 0, "l": 0, "m": 0, "n": 0,
                       "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0, "u": 0,
                       "v": 0, "w": 0, "x": 0, "y": 0, "z": 0,
                     }
    with open(input_path) as inp:
        offset = helpers.getting_offset(inp, letter_counter, probability)
        DecoderCaesarCipherWithKey(input_path, offset, output_path)


def DecoderVigenereCipher(input_path, key_path, output_path):

    special_symbols = { 255: ".", 200: " ", 210: ",", 240: ":", 260: "!",
                        230: "?", 300: "-", 310: "'", 320: "(", 340: ")",
                        360: "0", 361: "1", 362: "2", 363: "3", 364: "4",
                        365: "5", 366: "6", 367: "7", 368: "8", 369: "9",
                      }

    key_file = open(key_path, "r")
    text = open(output_path, "a")
    with open(input_path) as inp:
        for string in inp:
            final_string = ""
            key = key_file.readline()
            # making key and string readable
            if key.endswith("\n"):
                key = key[:-1]
            if string.endswith("\n"):
                string = string[:-1]
            for i in range(len(string)):
                # if the symbol is in syntactic signs, then we set a fixed value
                if ord(string[i]) in special_symbols:
                    final_string += special_symbols[ord(string[i])]
                    continue
                # else decoding symbols using key symbols
                if string[i].lower() == string[i]:
                    letter_ind = ord(string[i]) - ord("a")
                    letter_ind -= ord(key[i]) - ord("a")
                    letter_ind %= ord("z") - ord("a")
                    letter_ind += ord("a")
                else:
                    letter_ind = ord(string[i]) - ord("A")
                    letter_ind -= ord(key[i]) - ord("A")
                    letter_ind %= ord("Z") - ord("A")
                    letter_ind += ord("A")
                final_string += chr(letter_ind)
            # writing the line to output file
            text.write(final_string)
            text.write("\n")
    text.close()


def DecoderColumnarCipher(source, key_path, output):
    key_file = open(key_path, "r")
    with open(source) as inp:
        for string in inp:
            # getting key
            key = key_file.readline()
            new_key = helpers.GettingKeyDecode(key)
            # daking key and string readable
            if (string.endswith("\n")):
                string = string[:-1]
            if (new_key.endswith("\n")):
                new_key = new_key[:-1]

            matrix=[['' for i in range(len(new_key))]
                for j in range(int(len(string)/len(new_key)))]
            
            new_string = ""
            sorted_key = sorted(new_key)

            # decoding the string using matrix and key
            ind = 0
            for letter in sorted_key:
                index = new_key.index(letter)
                for i in range(len(new_key)):
                    matrix[i][index] = string[ind]
                    ind += 1
            
            for i in range(ind):
                new_string += matrix[i // len(new_key)][i % (len(string) // len(new_key))]

            # deleting the fragments of decoding
            while(new_string.endswith("-")):
                new_string = new_string[:-1]

            f = open(output, "+a")
            f.write(new_string)
            f.write("\n")
            f.close()
