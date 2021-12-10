# Fincheck

### Utilities to work with security identifiers, financial accounts, and other numbers.

Provides the following:
    1. Check digit algorithms for CUSIPs, ISINs, SEDOLs, and ABA numbers.
    2. Luhn's Algorithm
    3. Extraction methods for finding cusips, isins, sedols, and aba numbers within text
    4. Validation methods to check whether a string is a cusip, isin, sedol, or aba number

To install, simply use pip:
```
pip install fincheck
```

Validation Example Usage:
```
>>> from fincheck.validate import *
>>> is_isin("BD0716DELI01")
True
>>> is_cusip("30303M102")
True
>>> is_cusip("30303M103") #change last digit -- should be False
False
```

Extraction Example Usage:
```
>>> from fincheck.extract import *
>>> s = 'This is a test string that contains a cusip, incorrect cusip, isin, aba number, and a\
        sedol M0392N101 M0392N100 US9129091081 122235821 2007849 so we can demo the extraction methods of fincheck.'
>>> get_cusips(s)
['M0392N101']
>>> get_isins(s)
['US9129091081']
>>> get_abas(s)
['122235821']
>>> get_sedols(s)
['2007849']
```

Check Digit Calculation Example:
```
>>> from fincheck.checksum import *
>>> true_isin = "US0231351067"
>>> incomplete_isin = true_isin[:-1] #US023135106
>>> isin_check_digit(incomplete_isin)
7

>>> true_cusip = "931142103"
>>> incomplete_cusip = true_cusip[:-1] #93114210
>>> cusip_check_digit(incomplete_cusip)
3
```

