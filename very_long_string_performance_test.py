import time
import re

nums = [f'{str(i):>010}' for i in range(1000000)]
zen_in = '\n'.join(nums)

# ver1: --------------------------
time1 = time.time()
# version 1
zen_out = ''
for id, line in enumerate(zen_in.splitlines(), start=1):
    zen_out += f'{id:>03} {line}.\n'

time2 = time.time()
time_diff = time2 - time1
print(f'ver1: {time_diff:.10f}')


# ver2: --------------------------
time1 = time.time()
# version 2
zen_out = ''
num_lines = len(zen_in.splitlines())   # 後面用得到總行數。

for id, line in enumerate(zen_in.splitlines(), start=1):
    if id == num_lines:   # 最後那行
        tail = '!'
    else:
        tail = '.\n'
    zen_out += f'{id:>03} {line}{tail}'
time2 = time.time()
time_diff = time2 - time1
print(f'ver2: {time_diff:.10f}')

# ver3: --------------------------
time1 = time.time()
# version 3
zen_out = ''
lines = zen_in.splitlines()
if lines:
    id = 1
    zen_out += f'{id:>03} {lines[0]}'
    # 從第2行起迭代。注意是先逗點和換行碼，才是id和內容。
    for id, line in enumerate(lines[1:], start=2):
        zen_out += f'.\n{id:>03} {line}'
    zen_out += '!'

time2 = time.time()
time_diff = time2 - time1
print(f'ver3: {time_diff:.10f}')

# ver4 --------------------------
time1 = time.time()
# version 4
zen_out = ''
lines = zen_in.splitlines()
if lines:
    id = 0
    for id, line in enumerate(lines[:-1], start=1):   # 迭代前n-1行。
        zen_out += f'{id:>03} {line}.\n'
    zen_out += f'{id+1:>03} {lines[-1]}!'   # 最後1行

time2 = time.time()
time_diff = time2 - time1
print(f'ver4: {time_diff:.10f}')

# ver5: --------------------------
time1 = time.time()
# version 5
zen_out = ''
for id, line in enumerate(zen_in.splitlines(), start=1):
    zen_out += f'{id:>03} {line}.\n'
if zen_out:
    zen_out = f"{zen_out[:-2]}!"   # 刪除最後的2個錯誤字元',\n'，再補上正確的'!'。

time2 = time.time()
time_diff = time2 - time1
print(f'ver5: {time_diff:.10f}')

# ver6: --------------------------
time1 = time.time()
# version 6
zen_out = ''.join([f'{id:03} {line}' + ('\n' if id < len(zen_in.splitlines()) else '')
                   for id, line in enumerate((zen_in.replace('\n', '.\n') + ('!' if zen_in else '')).splitlines(), start=1)])

time2 = time.time()
time_diff = time2 - time1
print(f'ver6: {time_diff:.10f}')

# ver7: --------------------------
time1 = time.time()
# version 7
zen_out = ''.join([f'{id:03} {line}' + ('\n' if id < len(zen_in.splitlines()) else '') for id, line in enumerate(
    (re.sub(string=zen_in, pattern=r'(.*)\n', repl=r'\g<1>.\n') + ('!' if zen_in else '')).splitlines(), start=1)])

time2 = time.time()
time_diff = time2 - time1
print(f'ver7: {time_diff:.10f}')

# ver8: --------------------------
time1 = time.time()
# version 8
zen_tmp = re.sub(string=zen_in, pattern=r'(.*)\n',
                 repl=r'\g<1>.\n') + ('!' if zen_in else '')
zen_list_raw = zen_tmp.splitlines()
num_lines = len(zen_list_raw)
zen_list_done = []
for id, line in enumerate(zen_list_raw, start=1):
    if id < num_lines:
        tail = '\n'
    else:
        tail = ''
    zen_list_done.append(f'{id:03} {line}{tail}')
zen_out = ''.join(zen_list_done)

time2 = time.time()
time_diff = time2 - time1
print(f'ver8: {time_diff:.10f}')
