from typing import *
from .checksum import isin_check_digit
from .validate import is_cusip, is_isin
from .utils import read_csv


def load_cusip_refdata() -> List:
    """
    Reference data stored in refdata/cusip/cusip_list comes directly from the SEC Cusip list as of Q3 2021
        URL: https://www.sec.gov/divisions/investment/13flists.htm
    """
    data = read_csv("refdata/cusip/cusip_list.csv")
    data = [x for x in data if len(x) >= 4]
    return data

def load_cusip_ticker_map() -> List:
    data = read_csv("refdata/cusip/cusip_ticker_map.csv")
    return data

def load_isin_country_codes() -> List:
    data = read_csv("refdata/isin/country_codes.csv")
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
        self.ticker_ = self.__get_ticker(cusip)

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
    
    def __get_ticker(self, cusip: str) -> str:
        data = load_cusip_ticker_map()
        data = [x for x in data if x[0] == cusip]
        if data:
            return data[0][1]
        return "unk"

    def to_isin(self, country: str) -> str:
        country = country.strip().replace(" ", "") #clean
        assert country in ["US", "CA"], "'country' must be 'US' or 'CA', as cusips are only used in USA and Canada."
        isin = country + self.id_
        isin = isin + str(isin_check_digit(isin))
        return isin


class Isin(object):
    """
    -------------
    Object class representing an ISIN
    -------------
    Reference:
        https://en.wikipedia.org/wiki/International_Securities_Identification_Number
        https://www.isin.net/country-codes/
    -------------
    Structure of an ISIN:
        1. First two digits are the (ISO 3166-1-alpha-2 code) country code
        2. Next 9 digits are the NSIN (National Securities Identifying Number)
        3. Last and final digit is a check digit
    -------------
    """
    def __init__(self, isin: str):
        self.id_ = isin
        self.is_valid = is_isin(isin)
        self.nsin_ = isin[2:-1]
        self.country_code_ = isin[:2].upper()
        self.country_name_ = self.__get_country_name(self.country_code_)
        self.check_digit_ = isin[-1]
        self.ticker_ = self.__get_ticker()

    def __get_ticker(self) -> str:
        if self.country_code_ in ["US", "CA"]: #can only get ticker based on cusip as of this version
            data = load_cusip_ticker_map()
            data = [x for x in data if x[0] == self.nsin_]
            if data:
                return data[0][1]
        return "unk"

    def __get_country_name(self, code: str):
        data = load_isin_country_codes()
        data = [x for x in data if x[0] == code]
        if data:
            return data[0][1]
        return "unk"

    def to_nsin(self):
        """
        Returns the 9 digit NSIN (National Security Identifying Number)
        Note: 
            Depending on the country, the NSIN may be padded to fit the format of the ISIN
            Example: This is the case for SEDOLs (U.K.)
        
        """
        return self.id_[2:-1]
    
    def to_cusip(self):
        if self.country_code_ in ["US", "CA"]:
            return self.to_nsin()
        return None
    
    def to_sedol(self):
        if self.country_code_ == "GB":
            return self.to_nsin()[2:] #sedols will be zero padded to fit ISIN/NSIN format of 9 digits. Take last 7 digits
        return None
    