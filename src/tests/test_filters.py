from nose.tools import assert_true, assert_false

from notifirc.filters import contains


def test_contains_detects_word_in_middle():
    msg = 'hello everyone, how is it going?'
    assert_true(contains(msg, 'how'))

def test_contains_detects_multiple_words():
    msg = 'hello everyone, how is it going?'
    assert_true(contains(msg, 'how is it'))

def test_contains_detects_word_with_punctuation():
    msg = 'hello everyone, how is it going?'
    assert_true(contains(msg, 'everyone'))

def test_contains_detects_word_in_beginning():
    msg = 'hello everyone, how is it going?'
    assert_true(contains(msg, 'hello'))

def test_contains_doesnt_match_sub_words():
    msg = 'racecar'
    assert_false(contains(msg, 'race'))
