#!/usr/bin/python3
import numpy as np
import pandas as pd
import random
import warnings
import string
import main
import copy
import openpyxl
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
    print("Generate random excel file to test read_xlsx() function.")
    try:
        header, tables = main.read_xslx(file, key)
        print("No crashes!")
    except Exception as e:
        print(f"Exception thrown! {type(e)} : {e}")

# white box testing
## Gen first dict randomly
def gen_new_row(dict):
    head = list(dict.keys())
    headers = list(dict[head[0]].keys())
    newdict = {}
    for h in headers:
        newdict[h] = random.choice(string.printable)
    return newdict
    # same = bool(random.getrandbits(1))
    # gdb_dict = {}
    # for k in gdb_keys:
    #     entry = []
    #     for row in range(9):
    #         digit = bool(random.getrandbits(1))
    #         length = random.randrange(0, 20)
    #         if (digit):
    #             fuzz = ''.join(random.choice(random.randint(0,9)) for _ in range(length))
    #         else:
    #             fuzz = ''.join(random.choice(string.printable) for _ in range(length))
    #         entry.append(fuzz)
    #     gdb_dict[k] = entry
    # return gdb_dict

## generate random dict with same or diff header header:
def gen_mutated_dict(first_dict, mutation):
    gdb_keys = list(first_dict.keys())
    second_dict = copy.deepcopy(first_dict)
    if (mutation == 1):
        ## select field to change
        row = random.choice(gdb_keys)
        ## select random record to change
        fields = list(second_dict[gdb_keys[0]].keys())
        field = random.choice(fields)
        ## change the value
        value = second_dict[row][field]
        print(f"Original row: {row} : {second_dict[row]}")
        ## swap characters or change characters
        if (len(value) > 1):
            posa = random.randint(0,len(value)-1)
            posb = random.randint(0,len(value)-1)
            while posa == posb:
                posb = random.randint(0,len(value)-1)
            starr = list(value)
            starr[posa],starr[posb] = starr[posb],starr[posa]
            newvalue = "".join(starr)
        else:
            newvalue = chr(ord(value)+random.randint(1,10))
        second_dict[row][field] = newvalue
        print(f"Altered row: {row} : {second_dict[row]}")
        return second_dict, row
    elif (mutation == 2):
        ## add new row:
        newhead = str(random.randint(0,999))
        newdata = gen_new_row(second_dict)
        second_dict[newhead] = newdata
        print(f"Added row: {newhead} : {second_dict[newhead]}")
        return second_dict, newhead
    # elif (mutation == 1):
    #     ## select random row to be removed
    #     row = random.choice(gdb_keys)
    #     print(f"Row removed: {row} : {second_dict[row]}")
    #     second_dict.pop(row)
    #     return second_dict, row

## system testing:
#1. read excel
#2. read gdb
#3. mutate excel
#4. run test
## statement coverage for compare_row()
def system_logic_testing():
    header = ["Block", "Street", "Level", "Unit"]
    gdb_dict = main.read_gdb("testGDB.gdb", "Unit", header)
    excel_dict = main.read_xslx("TestExcel3.xlsx", "Unit")
    tests = {1:"Add a row with random values", 2:"Changed the value of a random cell"}
    for i in range(1,3):
        print(f"Test {i}: {tests[i]}")
        mutated_excel_dict, row = gen_mutated_dict(excel_dict[1], i)
        try:
            mismatch = main.compare_data(mutated_excel_dict, gdb_dict)
            print(F"mismatch: {mismatch}")
            for t in mismatch:
                if (t[1] == row):
                    if (t[0] == i):
                        print("TEST PASSED! \n")
                    else:
                        print("TEST FAILED!")
        except Exception as e:
            print(f"test {i} Exception caught!\n {type(e)} : {e} \n")
## main testing:
def mainTest():
    print("========== Black box testing ==========")
    blackbox_testing()
    print()
    print("========= Data mutation testing ==========")
    system_logic_testing()
    print()
    print("End of test")
mainTest()