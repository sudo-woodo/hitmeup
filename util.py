import random
import string


def random_string(length=10):
    return ''.join(random.choice(string.lowercase + string.uppercase + string.digits) for _ in range(length))
