from typing import *
import fincheck
from os import listdir
import re
from ast import literal_eval

def txt2list(path: str) -> List:
    """
    Opens a text file and converts to list by splitting on new lines
    """
    with open(path, "r") as f:
        txt = f.read()
    return list(filter(None, txt.split("\n")))

def run_validation_test(data: List, answers: List, validation_fn: Callable):
    for x, y in list(zip(data, answers)):
        assert str(validation_fn(x)) == y

def run_extraction_test(s: str, answers: str):
    parsing_dict = {
        "ABA": fincheck.extract.get_abas,
        "CUSIP": fincheck.extract.get_cusips,
        "ISIN": fincheck.extract.get_isins,
        "SEDOL": fincheck.extract.get_sedols
    }
    for k, v in parsing_dict.items():
        assert answers[k] == v(s)

def test_cusips():
    data = txt2list("Data/cusips.txt")
    answers = txt2list("Data/cusips_answers.txt")
    run_validation_test(data, answers, fincheck.validate.is_cusip)

def test_sedols():
    data = txt2list("Data/sedols.txt")
    answers = txt2list("Data/sedols_answers.txt")
    run_validation_test(data, answers, fincheck.validate.is_sedol)

def test_isins():
    data = txt2list("Data/isins.txt")
    answers = txt2list("Data/isins_answers.txt")
    run_validation_test(data, answers, fincheck.validate.is_isin)

def test_abas():
    data = txt2list("Data/abas.txt")
    answers = txt2list("Data/abas_answers.txt")
    run_validation_test(data, answers, fincheck.validate.is_aba)

def test_extraction():
    template = "extract{}.txt"
    answers_template = "extract{}_answers.txt"
    files = listdir("Data/extraction")
    for fi in files:
        m = re.search(r"extract(\d)\.txt", fi)
        if m:
            with open(f"Data/extraction/{template.format(m.group(1))}") as f:
                x = f.read()
            with open(f"Data/extraction/{answers_template.format(m.group(1))}") as f:
                y = literal_eval(f.read())
            run_extraction_test(x, y)

def test_check_digits():
    files = ["Data/cusips.txt", "Data/isins.txt", "Data/sedols.txt"]
    answer_files = [x.replace(".txt", "_answers.txt") for x in files]
    test_fns = [
        fincheck.checksum.cusip_check_digit, 
        fincheck.checksum.isin_check_digit, 
        fincheck.checksum.sedol_check_digit
        ]
    for fi, ans, fn in list(zip(files, answer_files, test_fns)):
        data = txt2list(fi)
        with open(ans, "r") as f:
            ans = list(filter(None, f.read().split("\n")))
        for d, a in list(zip(data, ans)): #only want to test for the True identifiers
            if a == "True":
                assert fn(d[:-1]) == int(d[-1])

if __name__ == "__main__":
    print("Running tests...")
    test_cusips()
    test_sedols()
    test_isins()
    test_abas()
    print("Validation: PASSED")
    test_extraction()
    print("Extraction: PASSED")
    test_check_digits()
    print("Check Digits: PASSED")
    print("PASSED ALL TESTS.")
    
