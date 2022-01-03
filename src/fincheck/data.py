from typing import *
from .checksum import isin_check_digit
from .validate import is_cusip

def load_cusip_refdata() -> List:
    #reference data stored in refdata/cusip comes directly from the SEC Cusip list as of Q3 2021
    #   URL: https://www.sec.gov/divisions/investment/13flists.htm
    with open("fincheck/refdata/cusip/cusip_list.csv", "r") as f:
        data = f.read()
    data = data.split("\n")[1:]
    data = [x.split(",") for x in data]
    data = [x for x in data if len(x) >= 4]
    return data


class Cusip(object):
    """
    ----------------------------
    Object describing a CUSIP
    ----------------------------
    Reference: 
        > https://en.wikipedia.org/wiki/CUSIP
        > https://www.cusip.com/pdf/CUSIP_Intro_03.14.11.pdf
    ----------------------------
    Structure of a CUSIP:
        1. First 6 digits is the issuer code (self.issuer_)
        2. 7th and 8th digits are the issue type (self.issue_ and self.issue_type_)
            > If both are numeric, it is an equity issue
            > If there is a letter, it is fixed income
        3. 9th and final digit is a check digit (self.check_digit_)
    ----------------------------
    """
    def __init__(self, cusip: str):
        self.id_ = cusip
        self.is_valid = is_cusip(cusip)
        self.issuer_ = cusip[:6] #first 6 digits is the issuer
        self.issue_ = cusip[-3:-1] #7th and 8th digit is the issue type 
        self.issue_type_ = "equity" if self.issue_.isnumeric() else "fixed income"
        self.check_digit_ = cusip[-1] #last digit
        self.name_, self.type_ = self.__build_metadata(cusip)

    def __build_metadata(self, cusip: str) -> Tuple:
        """
        Uses reference data from the SEC to build additional metadata for the cusip
        --------
        Returns:
            > Tuple of name, asset type
        --------
        """
        refdata = load_cusip_refdata()
        data = [x for x in refdata if len(x) > 3 and x[1] == cusip]
        if data:
            data = data[0]
            return data[2], data[3] 
        return "unk", "unk" #unknown -- not found in reference data

    def to_isin(self, country: str) -> str:
        country = country.strip().replace(" ", "") #clean
        assert country in ["US", "CA"], "'country' must be 'US' or 'CA', as cusips are only used in USA and Canada."
        isin = country + self.id_
        isin = isin + str(isin_check_digit(isin))
        return isin



