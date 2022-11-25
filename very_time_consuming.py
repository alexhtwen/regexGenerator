import random as r
import math

loop_count = 9999999

number = r.choice(range(1000000))
for i in range(loop_count):
    number = math.tan(number)
    print(f'i:{i:10}  number: {number:.6f}\r')

print(number)
