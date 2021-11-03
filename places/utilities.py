"""
Help functions and utilities
"""
import string
import random


def get_random_string(size=12, chars=string.ascii_letters + string.digits):
    """
    Returns random string of length <size> from collection of <chars>.
    """
    return ''.join([random.choice(chars) for _ in range(size)])