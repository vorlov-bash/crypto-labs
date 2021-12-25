from hashers import generate_md5_pass_set, generate_argon_pass_set
from generators import generate_human_like_random, generate_really_random

from io_files import write_passwords
from config import BASE_PATH

if __name__ == '__main__':
    write_passwords(BASE_PATH / 'weak_hashes.csv', generate_md5_pass_set())
    write_passwords(BASE_PATH / 'strong_hashes.csv', generate_argon_pass_set())
