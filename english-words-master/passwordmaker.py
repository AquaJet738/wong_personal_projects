import secrets
import string
import random

import read_english_dictionary


words = list(read_english_dictionary.load_words())


def password_generator():
    password_type = ""
    password = ""

    while password_type != "quit":
        password_type = input("Enter type of password to be generated (normal or passphrase, or type \"quit\" to exit): ")
        if password_type == "normal":
            # at least 12 characters long or more
            # a combination of uppercase and lowercase letters, numbers, and symbols
            # not a familiar name, person, character, or product
            chars = string.ascii_letters + string.digits + string.punctuation
            password_len = input("Enter number of characters in password (12 or more is recommended): ")

            password = ''.join(secrets.choice(chars) for _ in range(int(password_len)))
        elif password_type == "passphrase":
            # dictionary method (altered): choose a few words (instead of one) and string 
            # them together with numbers and symbols to make a strong password
            word_count = int(input("Enter number of words in passphrase: "))

            for _ in range(word_count):
                password = password + (random.choice(words).capitalize() + 
                                    secrets.choice(string.digits + string.punctuation))
        elif password_type == "quit":
            break
        else:
            print("Not a password type listed")
    
        print(password)
        password = ""  # clear password stored before make a new one


if __name__ == "__main__":
    password_generator()
