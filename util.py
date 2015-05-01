import random
import string


def random_string(length=10):
    return u''.join(random.choice(string.ascii_letters) for _ in range(length))
