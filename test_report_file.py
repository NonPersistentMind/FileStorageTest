"""
Generate a file with the next structure:
Січень 100 200 300
Лютий 400 500 600
Березень 700 800 900
Операція + - *

Use random numbers for the values and operations.
"""
import random, datetime as dt

operations = ["+", "-", "*", "/"]

today = dt.datetime.today()
timedelta = dt.timedelta(days=1)

COL_NUM = random.randint(10, 40)
ROW_NUM = random.randint(10, 1000)

FLOATING_DOT = False
localize = lambda s: s.replace(".", "." if FLOATING_DOT else ",")

with open("Random report.txt", "w") as f:
    for r in range(ROW_NUM):
        f.write(f"{(today + timedelta*r).date()} ")
        f.write(' '.join(localize("{:20.5f}".format(random.random()*10 + 5)) for _ in range(COL_NUM)) + "\n")
        
    f.write("Операція ")
    f.write(' '.join(str(random.choice(operations)).rjust(20, ' ') for _ in range(COL_NUM)) + "\n")
