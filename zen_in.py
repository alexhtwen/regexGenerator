import time

nums = [f'{str(i):>010}' for i in range(100000000)]
zen_in = '\n'.join(nums)
# print(zen_in)

zen_out = ''
num_lines = len(zen_in.splitlines())   # 後面用得到總行數。

time1 = time.time()
for id, line in enumerate(zen_in.splitlines(), start=1):
    if id == num_lines:   # 最後那行
        tail = '!'
    else:
        tail = ',\n'
    zen_out += f'{id:>03} {line}{tail}'
time2 = time.time()

print(zen_out)
print(time2 - time1)
