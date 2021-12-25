import os
import random
from string import ascii_letters

from io_files import read_passwords
from config import PASSWORDS_PATH


def generate_random_number(max_num: int):
    return int.from_bytes(os.urandom(5), 'big') % max_num


def generate_random_number_range(min_num: int, max_num: int):
    return random.randint(min_num, max_num)


def generate_25_password(count: int):
    if not 0 <= count <= 24:
        raise Exception('to many passwords to generate')

    top_25 = read_passwords(PASSWORDS_PATH / 'top_25.txt')
    return [top_25[generate_random_number(25)] for _ in range(count)]


def generate_100k_password(count: int):
    if not 0 <= count <= 99999:
        raise Exception('to many passwords to generate')

    top_100k = read_passwords(PASSWORDS_PATH / 'top_100k.txt')
    return [top_100k[generate_random_number(100000)] for _ in range(count)]


def slice_by_half(list_to_slice):
    middle_index = len(list_to_slice) // 2
    return list_to_slice[:middle_index], list_to_slice[middle_index:]


def generate_human_like_random(count: int):
    word_set = read_passwords(PASSWORDS_PATH / 'top_100k.txt')
    passwords = []
    for _ in range(count):
        random_passwords = [word_set[generate_random_number(100000)] for _ in range(2)]

        is_change = bool(generate_random_number(2))
        f_pass = random_passwords[0]

        if is_change:
            f_pass = ''.join(slice_by_half(f_pass)[::-1])

        s_pass = ''.join(
            [str(generate_random_number(10)) if not ch.isdigit() and generate_random_number(2) else ch for ch in
             random_passwords[1]])

        passwords.append(s_pass + f_pass)
    return passwords


def generate_really_random(count: int):
    password = []
    for _ in range(count):
        p = ''
        for _ in range(generate_random_number_range(8, 10)):
            p += ascii_letters[generate_random_number_range(0, 51)]
        p += ''.join(str(generate_random_number(24)) for _ in range(generate_random_number(10)))
        p += ''.join(chr(generate_random_number_range(33, 46)) for _ in range(generate_random_number(3)))
        password.append(p)
    return password


def generate_passwords_set():
    passwords_set = [
        *generate_100k_password(70000),
        *generate_human_like_random(10000),
        *generate_really_random(20000)
    ]
    random.shuffle(passwords_set)
    return passwords_set
