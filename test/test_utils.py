import sys
import os

sys.path.append(".")

from igor.utils import hidden, slugify

def test_hidden_on_special_paths():
    special_paths = [".", ".."]
    assert(not any([hidden(p) for p in special_paths]))

def test_hidden_on_hidden_paths():
    hidden_paths = [".what", ".ever.html", "..hmpf"]
    assert(all([hidden(p) for p in hidden_paths]))

def test_hidden_on_normal_paths():
    normal_paths = ["what", "ever.html"]
    assert(not any([hidden(p) for p in normal_paths]))

def test_slugify():
    test_string = "This is a title"
    assert(slugify(test_string) == "this_is_a_title")

def test_slugify_special_chars():
    test_string = "This is a title_with-special.chars"
    assert(slugify(test_string) == "this_is_a_title_with-special.chars")
