import random
from os import path, getcwd

def generate_secret():
    module_dir = path.dirname(__file__)
    file_path = path.join(module_dir, 'word_list.txt')
    f = open(file_path, 'r')
    word_list = f.read().splitlines()
    random.seed()
    secret = [word_list[random.randint(0,2047)] for i in range(12)]
    f.close()
    return secret


def get_str_secret(word_list):
    res = ''
    for i in word_list:
        res += f'{i}:'
    return res[0:-1]
