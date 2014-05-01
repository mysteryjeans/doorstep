import random
import hashlib


def random_digest():
    algo = hashlib.md5()
    algo.update(str(random.randrange(100, 10000000)))
    return algo.hexdigest()