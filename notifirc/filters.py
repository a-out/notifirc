import re


def contains(msg, phrase):
    reg = re.compile(r'\s' + re.escape(phrase) + r'\s', re.IGNORECASE)
    return reg.search(msg)

def starts_with(msg, phrase):
    reg = re.compile(r'^' + re.escape(phrase), re.IGNORECASE)
    return reg.match(msg)