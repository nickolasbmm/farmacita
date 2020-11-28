import string
import random

def string_generate(size=100, chars = ' ' + string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))