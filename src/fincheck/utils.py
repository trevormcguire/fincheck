from typing import *
import pkg_resources
import re

def keep_numeric(s: str) -> str:
    """
    Keeps only numeric characters in a string
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    return "".join(c for c in list(s) if c.isnumeric())

def convert_to_n(s: str, return_str: bool = True) -> Union[str, list]:
    """
    Converts a string into a sequence of digits
    ------
    PARAMS
    ------
        1. 's' -> input string
        2. 'return_str' -> If true, returns a string of sequential digits, else returns a list of digits
    """
    char_idxs = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if return_str:
        return "".join(str(char_idxs.index(c)) for c in list(s))
    return [char_idxs.index(c) for c in list(s)]

def ensure_format(s: str, n_chars: int = None) -> str:
    """
    Removes spaces within a string and ensures proper format
    ------
    PARAMS
    ------
        1. 's' -> input string
        2. 'n_chars' -> Num characters the string should consist of. Defaults to None.
    """
    assert isinstance(s, str), "Input must be a string."
    s = s.replace(" ", "") #clean spaces
    if n_chars:
        assert len(s) == n_chars, f"Input must be a payload of {n_chars} characters."
    return s

def split_payload(s: str) -> Tuple[str, int]:
    """
    Splits a string into two groups:
        1. First len(s) - 1 characters which represents the "payload" from which a check digit is calculated from
        2. Last character which represents a check digit
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    payload = s[:-1]
    check_digit = int(s[-1])
    return payload, check_digit

def find_and_validate(s: str, pattern: str, validation_fn: Callable = None) -> List:
    """
    Searches a string and returns every match of a regex pattern. 
    If validation_fn is specified, the matches are kept only if the function's criteria are met.
    ------
    PARAMS
    ------
        1. 's' -> input string
        2. 'pattern' -> regex pattern to search for
        3. 'validation_fn' -> function to call to validate matches. Defaults to None
                              - Note this function should return a boolean
    """
    matches = [m for m in re.finditer(pattern, s)]
    if matches:
        matches = [m.group(0) for m in matches]
        if validation_fn:
            matches = [m for m in matches if validation_fn(m)]
    return matches

def read_csv(path: str, keep_headers: bool = False) -> List:
    """
    Reads a csv file by splitting by "\n" and then "," -- creating a 2d list
    """
    path = pkg_resources.resource_filename(__name__, path)
    with open(path, "r") as f:
        data = f.read()
    data = data.split("\n")
    if not keep_headers:
        data = data[1:]
    data = [x.split(",") for x in data]
    return data

