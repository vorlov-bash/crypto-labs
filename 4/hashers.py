import hashlib

from generators import generate_passwords_set
from nacl import pwhash


def generate_md5_pass_set():
    p_set = generate_passwords_set()

    return [hashlib.md5(p.encode()).hexdigest() for p in p_set]


def generate_argon_pass_set():
    p_set = generate_passwords_set()

    argon_set = []
    for i, p in enumerate(p_set):
        print(i)
        argon_set.append(pwhash.argon2i.str(p.encode(), memlimit=16384).decode())
    return argon_set
