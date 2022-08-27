# DailyDialogue-Parser

Parser for the [DailyDialogue Dataset](http://yanran.li/dailydialog). This fork has been created to adapt the syntax, and also to add cleaning features relevant for using DailyDialogue in a text generation framework.

Note that while _this code_ is released under the MIT license, the dataset is not; it is `CC BY-NC-SA 4.0` licensed.
## Installation & Base Usage

This fork adds the following dependencies:

- tqdm
- clean-text

They can be installed by using `pip` after cloning with the below shell script:

```shell
git clone https://github.com/pszemraj/DailyDialogue-Parser.git
cd DailyDialogue-Parser
pip install -r requirements.txt
```

You can then run `parser.py` as detailed in the original README (see bottom of this page).

## cleaning outputs

Once the parser is done, the outputs can be cleaned with the `clean_parsed_data.py` script.

The primary use case is to clean the outputs for use in a text generation framework. The script will remove duplicate lines of dialogue, and normalize whitespace to "standard" whitespace.

Usage:

```shell
python clean_parsed_data.py [-h] [-i IN_DIR] [-o OUT_DIR] [-l] [-f OUT_FORMAT] [--remove_all_duplicates]
```

Call `python clean_parsed_data.py -h` for more information.

**Note: The script will not remove duplicate lines of text in the other two files (emotion and act annotations) by default**. This is because the annotations are simply numbers as strings, and duplication in isolation of the dialogue would lead to a mismatch between the files.

### Dialogue Script: Adding Speaker Pseudo-Labels

An additional added feature is the ability to add speaker "labels" or "identifying tokens" to the dialogue. This allows for the identification of the speaker of each line of dialogue, which is important to have for text generation to extract the response of a given speaker relative to some prompt (_as opposed to a continuation of the prompt, etc._).

Adding speakers to the output dialogue file is done via the `--make-script` flag (`-s`). Argument switches are detailed in the below table.

| Switch               | Shorthand | Function                                                    |
|----------------------|-----------|-------------------------------------------------------------|
| `--make-script`        | `-s`        | Enables generating a dialogue script                        |
| `--speaker-one`        | `-s1`       | Speaker one for the script. default: Person Alpha           |
| `--speaker-two`        | `-s2`       | Speaker two for the script. default: Person Beta            |
| `--speaker-start-char` | `-start`    | Speaker starting char for the script. default: empty string |
| `--speaker-end-char`   | `-end`      | Speaker end char for the script. default: ":"               |

Example:

```shell
python clean_parsed_data.py -i "data\parsed_train" -s -s1 Ola -s2 Jorgen -start "^^^" -end "&&&"
```

Yields the following in the output file (`./data/parsed_train/cleaned/cleaned_script_dial.txt`):

```
^^^Jorgen&&&
Are you all right?

^^^Ola&&&
I will be all right soon. I was terrified when I watched them fall from the wire.

^^^Jorgen&&&
Don't worry.He is an acrobat.

^^^Ola&&&
I see.

(...)
```

Example use cases/training a model on such data can be found in the [ai-msgbot](<https://github.com/pszemraj/ai-msgbot>) repository.

# Original README

---

_Note: everything below this message is verbatim from the original repository._

---

## Reference

Paper: Yanran Li, Hui Su, Xiaoyu Shen, Wenjie Li, Ziqiang Cao, and Shuzi Niu.
DailyDialog: A Manually Labelled Multi-turn Dialogue Dataset. IJCNLP 2017.

Dataset Source: <http://yanran.li/dailydialog>

## Usage

```
python3 parser.py -i <input_dir> -o <output_dir>
```
