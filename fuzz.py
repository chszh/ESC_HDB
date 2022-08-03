import numpy as np
import pandas as pd
import random
import warnings
import string
warnings.simplefilter("ignore")

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

df.to_excel('fuzz.xlsx')

print(df)