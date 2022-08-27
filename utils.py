"""
utils.py - utility functions for cleaning the data
"""

import re

def rm_consecutive_duplicates(textlist: list) -> list:
    """
    rm_consecutive_duplicates - given a list of strings, remove consecutive duplicates

    :param textlist: list of strings
    """

    newlist = []
    for i in range(len(textlist)):
        if textlist[i] != textlist[i - 1]:
            newlist.append(textlist[i])
    return newlist

def correct_spacing(text:str) -> str:
    """
    correct_spacing - fixes the spacing in a string.

        this consists of 1) removing duplicate spaces, and 2) removing spaces at start/end of strings, and 3) removing spaces that come before a punctuation mark, i.e. police ? -> police? and "we couldn't find it , sir ." -> "we couldn't find it, sir."

    :param text: string to be cleaned
    """

    # remove duplicate spaces
    text = re.sub(r'\s+', ' ', text)
    # remove spaces at start/end of strings
    text = re.sub(r'^\s+|\s+$', '', text)
    # remove spaces that come before a punctuation mark
    text = re.sub(r'\s+(\W)', r'\1', text)
    # remove spaces that come after apostrophes or single quotes. "Here' s a test" -> "Here's a test"
    text = re.sub(r"([\'])\s+", r"\1", text)
    # text = re.sub(r"(\w)'(\w)", r"\1'\2", text)

    return text