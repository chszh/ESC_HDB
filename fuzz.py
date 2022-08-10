#!/usr/bin/python3
from ast import Try
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
    print("Generate random excel file to test read_xlsx() function.")
    file = generate_gibberish()
    key = "Unit"
    print()
    try:
        header, tables = main.read_xslx(file, key)
        print("No crashes!")
    except Exception as e:
        print(f"Exception thrown! {type(e)} : {e}")

#White box testing
## statement coverage
## Gen first dict randomly
def gen_random_dict():
    rows = list(random.randint(0,999) for _ in range(6))
    headers = list(random.choice(string.printable) for _ in range(5))
    first_dict = {}
    for r in rows:
        digit = bool(random.getrandbits(1))
        length = random.randrange(0, 20)
        if (digit):
            fuzz = ''.join(str(random.randint(0,9)) for _ in range(length))
        else:
            fuzz = ''.join(random.choice(string.printable) for _ in range(length))
        first_dict[r] = fuzz
    return first_dict

## Gen second dict
def gen_second_dict(first_dict, sameheader, samevalue):
    if (sameheader):
        second_dict = copy.deepcopy(first_dict)
        if (samevalue):
            return second_dict
        else:
            row = random.choice(list(second_dict.keys()))
            ## change the value
            value = second_dict[row]
            newvalue = value + random.choice(string.printable)
            second_dict[row] = newvalue
            return second_dict
    else:
        second_dict = gen_random_dict()
        while set(second_dict.keys()) == set(first_dict.keys()):
            second_dict = gen_random_dict()
        return second_dict

def white_box():
    test = {1: ["Same headers, Same values", (True, True)], 2: ["Same headers, Different values", (True, False)],
            3: ["Different headers", (False, True)]}
    a = gen_random_dict()
    for i in test:
        print(f"Test {i}: {test[i][0]}")
        b = gen_second_dict(a, test[i][1][0], test[i][1][1])
        print(f"First dict: \n {a}")
        print(f"Second dict: \n {b}")
        testInstr = {0:0, 1:0, 2:0}
        try:
            main.compare_row(a,b, False, testInstr)
            print(testInstr, "\n")
        except Exception as e:
            print(f"test {i} Exception caught!\n {type(e)} : {e} \n")

#System testing - logic 
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

##generate new row of ranom values
def gen_new_row(dict):
    head = list(dict.keys())
    headers = list(dict[head[0]].keys())
    newdict = {}
    for h in headers:
        newdict[h] = random.choice(string.printable)
    return newdict

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
    print("========== White box testing ==========")
    white_box()
    print()
    print("========= Data mutation testing ==========")
    system_logic_testing()
    print()
    print("End of test")
mainTest()