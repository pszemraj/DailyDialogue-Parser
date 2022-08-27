"""
utils.py - utility functions for cleaning the data
"""

import logging
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


def correct_spacing(text: str) -> str:
    """
    correct_spacing - fixes the spacing in a string.

        this consists of 1) removing duplicate spaces, and 2) removing spaces at start/end of strings, and 3) removing spaces that come before a punctuation mark, i.e. police ? -> police? and "we couldn't find it , sir ." -> "we couldn't find it, sir."

    :param text: string to be cleaned
    """

    # remove duplicate spaces
    text = re.sub(r"\s+", " ", text)
    # remove spaces at start/end of strings
    text = re.sub(r"^\s+|\s+$", "", text)
    # remove spaces that come before a punctuation mark
    text = re.sub(r"\s+(\W)", r"\1", text)
    # remove spaces that come after apostrophes or single quotes. "Here' s a test" -> "Here's a test"
    text = re.sub(r"([\'])\s+", r"\1", text)
    # text = re.sub(r"(\w)'(\w)", r"\1'\2", text)

    return text


def add_speakers(
    textlist: list,
    speaker_one: str = "Person Alpha",
    speaker_two: str = "Person Beta",
    speaker_start_char="",
    speaker_end_char=":",
) -> list:
    """
    add_speakers - add speakers to a list of strings, forming a "dialogue script".

        The input list of strings is assumed to be in alternating speaker order.
        The resulting list of strings is in alternating speaker order. with the speaker names on one line, and the dialogue on the next line, then the next speaker, etc.
    """

    logging.info(
        f"Adding speakers:\n\tSpeaker 1:{speaker_one}\t\tSpeaker2{speaker_two}\n\tDelimiters:\t<{speaker_start_char}> and <{speaker_end_char}>\n\tTotal dialogue lines: {len(textlist)}"
    )
    newlist = []
    for i in range(len(textlist)):
        if i % 2 == 0:
            newlist.append(f"{speaker_start_char}{speaker_one}{speaker_end_char}\n")
        else:
            newlist.append(f"{speaker_start_char}{speaker_two}{speaker_end_char}\n")
        newlist.append(textlist[i] + "\n")
    return newlist
