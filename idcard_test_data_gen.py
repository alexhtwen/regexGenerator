import re
import random as r
from string import ascii_uppercase

AMOUNT = 300

# 產生若干筆不重複的匹配資料，並存成xxx_good.dat檔
tmp_set = set()
count = 0
while True:
    id_card_good = \
        r.choice(ascii_uppercase) + \
        r.choice('1289') + \
        ''.join(r.choices([str(i) for i in range(10)], k=8))
    tmp_set.add(id_card_good + '\n')
    if len(tmp_set) == AMOUNT:
        break

with open('./id_good.dat', 'w') as f:
    for item in tmp_set:
        f.write(item)


# 產生若干筆不重複的不匹配資料，並存成xxx_bad.dat檔。
tmp_set = set()
count = 0
while True:
    id_card_bad = r.choice(r'~QWRTYIOPLGFDXVNertyubvcdoph `~!@#$%^&*()_+-7896542130|}{"?:;></.,\=][') + \
        ''.join(r.choice([str(i) for i in range(3, 8)] + [a for a in 'Alex'])) + \
        ''.join(r.choices([str(i) for i in range(9)], k=r.choices(
            [l for l in range(3, 14)], k=1, weights=[1, 2, 2, 5, 10, 60, 10, 5, 2, 2, 1])[0]))
    match = re.search(
        string=id_card_bad, pattern=r'[A-Z][1289]\d{8}', flags=re.MULTILINE | re.IGNORECASE)
    if match is None:
        continue
    else:
        tmp_set.add(id_card_bad + '\n')
        if len(tmp_set) == AMOUNT:
            break

with open('./id_bad.dat', 'w') as f:
    for item in tmp_set:
        f.write(item)
