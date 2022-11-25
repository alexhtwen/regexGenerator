import sys
import os
import re

import regex_demo_settings

SETTINGS = regex_demo_settings.settings[sys.argv[1]]
count = 1

with open(SETTINGS['file_in'], 'r') as f_in:
    with open(SETTINGS['file_out'], 'wb') as f_out:
        while line := f_in.readline():  # 這列動作： 1)讀取一行文字並存入line； 2)判斷line是否為空字串。
            results = re.search(r'^(.+?)\s+(.*)$', line)
            code = results[1]
            len_code = len(code)
            spaces = ' ' * (SETTINGS['len_code_padding'] - len_code)
            word = results[2]
            if SETTINGS['has_id']:
                id = f"{count:{SETTINGS['pad_id']}{SETTINGS['len_id']}}{' ' * SETTINGS['spaces_after_id']}"
                count += 1
            else:
                id = ''

            line_adjusted = f'{id}{code}{spaces}{word}\n'.encode('utf8')
            chars_written = f_out.write(line_adjusted)

        f_out.seek(-1, os.SEEK_END)
        f_out.truncate()


# with open(settings['file_out'], 'rb+') as f_out:
#     f_out.seek(-1, os.SEEK_END)
#     f_out.truncate()

print(sum(1 for line in open(SETTINGS['file_out'])))
print(SETTINGS)
print('** The End of re**')
