"""
Generates a file with the next structure:
2024-04-10 10.3  8.7 14.1
2024-04-11  6.2  5.7 11.3
2024-04-12  6.4  9.8 12.1
Операція      +    -    *

Using random values and operations.
"""
import random, datetime as dt

operations = ["+", "-", "*", "/"]

today = dt.datetime.today()
day = dt.timedelta(days=1)

COL_NUM = random.randint(10, 40)
ROW_NUM = random.randint(10, 1000)

FLOATING_DOT = False
localize = lambda s: s.replace(".", "." if FLOATING_DOT else ",")

with open("Random report.txt", "w") as f:
    for r in range(ROW_NUM):
        f.write(f"{(today + r*day).date()} ")
        f.write(' '.join(localize("{:20.5f}".format(random.random()*10 + 5)) for _ in range(COL_NUM)) + "\n")
        
    f.write("Операція ")
    f.write(' '.join(str(random.choice(operations)).rjust(20, ' ') for _ in range(COL_NUM)) + "\n")
