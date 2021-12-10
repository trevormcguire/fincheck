from typing import *
from .utils import ensure_format, keep_numeric, convert_to_n

def luhn_check_digit(s: str) -> int:
    """
    Returns the check digit given a string of numbers given the Luhn Algorithm
    Reference: https://en.wikipedia.org/wiki/Luhn_algorithm
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    s = ensure_format(s)
    s = keep_numeric(s)
    if len(s) % 2 == 1:
        s = "0" + s #zero pad so length is even
    sum_ = 0
    for idx in range(len(s), 0, -1):
        digit = int(s[idx-1])
        if idx % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        sum_ += digit
    
    return (10 - (sum_ % 10)) % 10 #using mod operator twice asserts the check digit is < 10


def isin_check_digit(s: str) -> int:
    """
    Luhn Mod N Algorithm
    Returns the check digit for an ISIN
    Reference:
        1. https://en.wikipedia.org/wiki/International_Securities_Identification_Number
        2. https://en.wikipedia.org/wiki/Luhn_mod_N_algorithm
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    s = ensure_format(s, n_chars=11)
    s = convert_to_n(s)
    return luhn_check_digit(s)

def cusip_check_digit(s: str) -> int:
    """
    Luhn Double add Double (mod 10 double add double)
    Reference:
        https://en.wikipedia.org/wiki/CUSIP
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    s = ensure_format(s, n_chars=8)
    s = convert_to_n(s, return_str=False) #returns a list of digits
    sum_ = 0
    for idx in range(len(s)):
        digit = s[idx]
        #algorithm isnt zero-indexed, so we want to consider idx+1 or simply flip the logic of the mod operation
        if idx % 2 != 0:
            digit *= 2
        sum_ += int(digit / 10) + digit % 10
    
    return (10 - (sum_ % 10)) % 10 


def sedol_check_digit(s: str) -> int:
    """
    Returns the Check Digit for a SEDOL
    The Check digit is calculated via a weighted sum followed by a mod operation
    Reference:
        https://en.wikipedia.org/wiki/SEDOL
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    s = ensure_format(s, n_chars=6)
    s = convert_to_n(s, return_str=False)
    weights = [1, 3, 1, 7, 3, 9]
    sum_ = 0
    for w, v in list(zip(weights, s)):
        sum_ += w * v
    return (10 - (sum_ % 10)) % 10 
    


