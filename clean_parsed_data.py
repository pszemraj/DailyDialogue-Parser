#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean_parsed_data.py - a script to clean the parsed data
"""

__author__ = "Peter Szemraj"

import argparse
import gzip
import logging
from pathlib import Path

from cleantext import clean
from tqdm import tqdm

from utils import correct_spacing, rm_consecutive_duplicates, add_speakers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="LOGFILE_clean_parsed_data.log",
    filemode="w",
)


def clean_parsed_file(
    in_path: str or Path,
    lowercase: bool = False,
) -> list:
    """
    clean_parsed_file - a function to clean the parsed data in the input file and save it in the output file
    """
    in_path = Path(in_path)
    logging.info(f"Cleaning:\t{in_path}")

    if in_path.suffix.split(".")[-1] == "gz":
        with gzip.open(
            in_path,
            "rt",
            encoding="utf-8",
        ) as in_file:
            lines = in_file.read().splitlines()
    else:
        logging.info(f"Assuming {in_path.name} is a text file")
        with open(in_path, "r", encoding="utf-8") as in_file:
            lines = in_file.readlines()

    unique_lines = rm_consecutive_duplicates(lines)
    logging.info(
        f"Removed {len(lines) - len(unique_lines)} duplicate lines, will clean {len(unique_lines)} lines"
    )

    cleaned_lines = []
    for line in unique_lines:
        _line = clean(line.strip(), lower=lowercase)
        _line = correct_spacing(_line)
        cleaned_lines.append(_line + "\n")

    logging.info(f"completed cleaning:\t{in_path.name}")

    return cleaned_lines


def save_clean_list(clean_list: list, write_path: str or Path, out_format="txt"):
    """
    save_clean_list - a function to save the cleaned list to a file
    """
    assert out_format in [
        "txt",
        "gz",
    ], f"{out_format} is not a valid output format, use either 'txt' or 'gz'"
    write_path = Path(write_path)
    write_path = write_path.with_suffix(f".{out_format}")
    write_path = str(write_path.resolve())

    logging.info(f"Saving cleaned list to {write_path} with {out_format} format")
    if out_format == "txt":
        with open(write_path, "w", encoding="utf-8") as out_file:
            for line in clean_list:
                out_file.write(line)
    elif out_format == "gz":
        with gzip.open(write_path, "wt") as out_file:
            for line in clean_list:
                out_file.write(line.encode("utf-8"))

    logging.info(f"Saved cleaned list to {write_path} with {out_format} format")

    return write_path


def get_parser():
    """
    get_parser - a helper function for the argparse module
    """

    parser = argparse.ArgumentParser(
        description="parser.py - a parser for the daily dialog dataset"
    )
    parser.add_argument(
        "-i",
        "--in_dir",
        type=str,
        help='Input directory containing the dialogues as text files. Example: "train/"',
        required=True,
    )
    parser.add_argument(
        "-o",
        "--out_dir",
        type=str,
        required=False,
        default=None,
        help="Output directory for the parsed dialogues",
    )
    parser.add_argument(
        "-l",
        "--lowercase",
        action="store_true",
        default=False,
        help="Lowercase the text",
    )
    parser.add_argument(
        "-f",
        "--out_format",
        type=str,
        default="txt",
        help="Output format for the cleaned dialogues (txt or gz)",
    )
    parser.add_argument(
        "-s",
        "--make-script",
        action="store_true",
        default=False,
        help="Add speakers to the dialogue lines",
    )
    parser.add_argument(
        "-s1",
        "--speaker-one",
        type=str,
        default="Person Alpha",
        required=False,
        help="Speaker one for the script, default: Person Alpha",
    )
    parser.add_argument(
        "-s2",
        "--speaker-two",
        type=str,
        default="Person Beta",
        required=False,
        help="Speaker two for the script, default: Person Beta",
    )
    parser.add_argument(
        "-start",
        "--speaker-start-char",
        type=str,
        default="",
        help="Speaker start char for the script, default: empty string",
    )
    parser.add_argument(
        "-end",
        "--speaker-end-char",
        type=str,
        default=":",
        help="Speaker end char for the script, default: ':'",
    )

    return parser


if __name__ == "__main__":

    args = get_parser().parse_args()
    logging.info(f"Arguments: {args}")

    # standard arguments
    in_path = Path(args.in_dir)
    assert in_path.is_dir(), f"{in_path} is not a valid directory"

    if args.out_dir is None:
        out_path = in_path / "cleaned"
        out_path.mkdir(exist_ok=True)
    else:
        out_path = Path(args.out_dir)
        out_path.mkdir(exist_ok=True)

    assert out_path.is_dir(), f"{out_path} is not a directory"
    lowercase = args.lowercase
    out_format = args.out_format

    # script arguments
    make_script = args.make_script
    speaker_one = args.speaker_one
    speaker_two = args.speaker_two
    speaker_start_char = args.speaker_start_char
    speaker_end_char = args.speaker_end_char

    out_path.mkdir(exist_ok=True)
    FORMATS = [".txt", ".gz"]
    files = [f for f in in_path.iterdir() if f.is_file() and f.suffix in FORMATS]

    for file in tqdm(files, desc="Cleaning"):

        _base = file.stem.split(".")[
            0
        ]  # necessary for the script to work with the gz files
        clean_list = clean_parsed_file(file, lowercase)
        if make_script and "dial" in _base:

            out_list = add_speakers(
                clean_list,
                speaker_one=speaker_one,
                speaker_two=speaker_two,
                speaker_start_char=speaker_start_char,
                speaker_end_char=speaker_end_char,
            )
            _out = out_path / f"cleaned_script_{_base}.{out_format}"
            logging.info(f"added speakers to {file.name}")

        else:
            out_list = clean_list
            _out = out_path / f"cleaned_{_base}.{out_format}"

        _ = save_clean_list(clean_list=out_list, write_path=_out, out_format=out_format)
        logging.info(f"Saved cleaned list to {_out}")

    logging.info(f"Cleaned {len(files)} files, outputs are in:\n\t{out_path}")

    print("Done")
