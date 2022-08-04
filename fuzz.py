import numpy as np
import pandas as pd
import random
import warnings
import string
import main
import copy
warnings.simplefilter("ignore")

# Crash detection:
## Black box testing - generate random excel file with giberish data
def generate_gibberish():
    base = pd.read_excel("TestGDBExcel.xlsx")
    columns = [i for i in base.columns]

    no_of_rows = 9
    min_len = 0
    max_len = 20
    data = {}

    for i in columns:
        entry = []
        for row in range(no_of_rows):
            length = random.randrange(min_len, max_len)
            fuzz = ''.join(random.choice(string.printable) for _ in range(length))
            entry.append(fuzz)
        data[i] = entry

    df = pd.DataFrame(data, columns = columns)
    df = df.applymap(lambda x: x.encode('unicode_escape').
                    decode('utf-8') if isinstance(x, str) else x)

    filename = "fuzz.xlsx"
    df.to_excel(filename)
    print(f"generated table: \n {df}")
    return filename

## pass through read_xlsx function
def blackbox_testing():
    file = generate_gibberish()
    key = "Unit"
    try:
        header, tables = main.read_xslx(file, key)
        print("No crashes!")
        print(f"header: {header}")
        print(f"Sheets: \n {tables}")
    except Exception as e:
        print(f"Exception thrown! {type(e)} : {e}")

# white box testing
## mutation type - swapping of characters
def key_mutation_swap(key):
    posa = random.randint(0, len(key))
    posb = random.randint(0, len(key))
    while (posb == posa):
        posb = random.randint(0, len(key))
    liststring = list(key)
    liststring[posa], liststring[posb] = liststring[posb], liststring[posa]
    newkey = "".join(liststring)
    return newkey

## generate random dict with same or diff header header:
def gen_dicts():
    gdb_keys = ["Block", "Street", "Level", "Unit"]
    same = bool(random.getrandbits(1))
    gdb_dict = {}
    for k in gdb_keys:
        entry = []
        for row in range(9):
            digit = bool(random.getrandbits(1))
            length = random.randrange(0, 20)
            if (digit):
                fuzz = ''.join(random.choice(random.randint(0,9)) for _ in range(length))
            else:
                fuzz = ''.join(random.choice(string.printable) for _ in range(length))
            entry.append(fuzz)
        gdb_dict[k] = entry
    if (same):
        excel_keys = gdb_keys
        samecontent = bool(random.getrandbits(1))
        if (samecontent):
            excel_dict = copy.deepcopy(gdb_dict)
        else:
            excel_dict = {}
            for k in excel_keys:
                entry = []
                for row in range(9):
                    digit = bool(random.getrandbits(1))
                    length = random.randrange(0, 20)
                    if (digit):
                        fuzz = ''.join(random.choice(random.randint(0,9)) for _ in range(length))
                    else:
                        fuzz = ''.join(random.choice(string.printable) for _ in range(length))
                    entry.append(fuzz)
                excel_dict[k] = entry
    else:
        excel_keys = []
        for key in gdb_keys():
            newkey = key_mutation_swap(key)
            excel_keys.append(newkey)
        excel_dict = {}
        for k in excel_keys:
            entry = []
            for row in range(9):
                digit = bool(random.getrandbits(1))
                length = random.randrange(0, 20)
                if (digit):
                    fuzz = ''.join(random.choice(random.randint(0,9)) for _ in range(length))
                else:
                    fuzz = ''.join(random.choice(string.printable) for _ in range(length))
                entry.append(fuzz)
            excel_dict[k] = entry
    return gdb_dict, excel_dict

## statement coverage for compare_row()
def whitebox_testing(a, b):
    try:
        testInstrument = {0:0, 1:0, 2:1}
        main.compare_row(a,b, testInstrument)
        print(testInstrument)
    except Exception as e:
        print(f"Exception caught!\n {type(e)} : {e}")
## main testing:
def mainTest():
    print("========== Black box testing ==========")
    blackbox_testing()
    print()
    print("========= White box testing ==========")
    whitebox_testing()
    print()
    print("End of test")
mainTest()