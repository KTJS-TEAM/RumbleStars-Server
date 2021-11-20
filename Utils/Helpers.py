import string
import random

def randomStringDigits():
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(40))


def randomID():
    length = 5
    return int(''.join([str(random.randint(0, 10)) for _ in range(length)]))