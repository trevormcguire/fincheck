from .validate import is_cusip, is_isin, is_aba, is_sedol
from .utils import find_and_validate
from typing import *

def get_cusips(s: str) -> List[str]:
    """
    ---------------------------------
    Find and Extract CUSIPs from text
    ---------------------------------
    CUSIP Format:
        > Numeric or Alphanumeric
        > First 6 characters identify the issuer and is called Issuer Code or CUSIP-6
            - The last 3 characters of Issuer Code can be letters
        > 7th and 8th characters identify the exact issue
            - General rule: Numbers for equities and Letters for Fixed Income
            - The letters I and O are not used to avoid confusion with 1 and 0
        > 9th digit is a checksum
    Reference:
        https://www.cusip.com/pdf/CUSIP_Intro_03.14.11.pdf
        https://en.wikipedia.org/wiki/CUSIP
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    #ensure 9th is digit
    pattern = r"((?<=[^\w])|(?<=^))([A-Za-z0-9]{8}[0-9])(?=[^\w]|$)"
    return find_and_validate(s, pattern, validation_fn=is_cusip)


def get_isins(s: str) -> List[str]:
    """
    ---------------------------------
    Find and Extract ISINs from text
    ---------------------------------
    ISIN Format:
        > First two characters are letters and represent country code
            - Country codes are defined in ISO 3166-1 alpha-2 (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
        > The following 9 characeters are alphanumeric
            - These 9 characters are the NSIN (https://en.wikipedia.org/wiki/National_Securities_Identifying_Number)
            - Zero-padded if NSIN is less than 9 characters
        > The 12th and last digit is a check digit
    Reference:
        https://en.wikipedia.org/wiki/International_Securities_Identification_Number
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    pattern = r"((?<=[^\w])|(?<=^))([A-Za-z]{2}[A-Za-z0-9]{9}[0-9])(?=[^\w]|$)"
    return find_and_validate(s, pattern, validation_fn=is_isin)


def get_sedols(s: str) -> List[str]:
    """
    ---------------------------------
    Find and Extract SEDOLs from text
    ---------------------------------
    SEDOL Format:
        - 6 alphanumeric characters and 1 checkdigit
        - Vowels are never used
    Reference:
        https://en.wikipedia.org/wiki/SEDOL
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    pattern = r"((?<=[^\w])|(?<=^))([0-9BCDFGHJKLMNPQRSTVWXYZ]{6}[0-9])(?=[^\w]|$)"
    return find_and_validate(s, pattern, validation_fn=is_sedol)

def find_securities(s: str, include: List = ["CUSIP", "ISIN", "SEDOL"]) -> Dict:
    allowed_types = {
        "CUSIP": get_cusips, 
        "ISIN": get_isins, 
        "SEDOL": get_sedols
        }
    include = [x.upper() for x in include] #ensure upper
    include = [x for x in include if x in allowed_types] #ensure types are valid
    assert len(include) > 0, "Must include at least one of the following: CUSIP, ISIN, or SEDOL"
    res = {}
    for t in include:
        res[t] = allowed_types[t](s)
    return res

def get_abas(s: str) -> List[str]:
    """
    --------------------------------------
    Find and Extract ABA Numbers from text
    --------------------------------------
    ABA Format:
        > 9 digits 
        > XXXXYYYYC
            - XXXX = Federal Reserve Routing Symbol
            - YYYY = ABA Institution Identifier
            - C = Check Digit
        > The first two digits of the nine digit RTN must be in the ranges:
            - 00 - 12 
            - 21 - 32 
            - 61 - 72
            - 80
    Reference:
        https://en.wikipedia.org/wiki/ABA_routing_transit_number
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    pattern = r"((?<=[^\w])|(?<=^))(\d{9})(?=[^\w]|$)"
    return find_and_validate(s, pattern, validation_fn=is_aba)


