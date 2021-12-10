from typing import *
from .utils import split_payload
from .checksum import luhn_check_digit, isin_check_digit, cusip_check_digit, sedol_check_digit

def is_luhn(s: str) -> bool:
    """
    Asserts a sequence of characters follows the Luhn Algorithm
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    payload, check_digit = split_payload(s)
    return luhn_check_digit(payload) == check_digit

def is_isin(s: str) -> bool:
    """
    Validates if a string follows the ISIN checksum algorithm and ISIN format
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    s = s.replace(" ", "")
    #ISINs are 12 characters long. First two chars are alpha (country code). Last is numerical (check digit)
    if len(s) == 12 and s[:2].isalpha() and s[-1].isnumeric():   
        payload, check_digit = split_payload(s)
        return isin_check_digit(payload) == check_digit
    return False



def is_cusip(s: str) -> bool:
    """
    Validates if a string follows the CUSIP check digit algorithm and CUSIP format
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    s = s.replace(" ", "")
    if len(s) == 9 and s[-1].isnumeric(): #cusips are 9 characters long and last digit is numerical (Check digit)
        payload, check_digit = split_payload(s)
        return cusip_check_digit(payload) == check_digit
    return False

def is_sedol(s: str) -> bool:
    """
    Determines whether a string follows the SEDOL check digit algorithm and SEDOL format
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    s = s.replace(" ", "")
    if len(s) == 7 and s[-1].isnumeric():
        payload, check_digit = split_payload(s)
        return sedol_check_digit(payload) == check_digit
    return False


def is_aba(s: str) -> bool:
    """
    Determines whether a sequence of characters is an ABA Number

    ABA checksum is performed via a weighted sum of individual digits that comprise it
        > The weights are as follows: 371 371 371
    
    Formula:
        True if 3(d1 + d4 + d7) + 7(d2 + d5 + d8) + (d3 + d6 + d9) mod 10 = 0 else False
    
    Reference:
        https://en.wikipedia.org/wiki/ABA_routing_transit_number
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    s = s.replace(" ", "")
    if len(s) == 9 and s.isnumeric(): #ABA Numbers are 9 digits long
        s = [int(n) for n in list(s)]
        if ((3 * (s[0] + s[3] + s[6])) + (7 * (s[1] + s[4] + s[7])) + (s[2] + s[5] + s[8])) % 10 == 0:
            return True
    return False

