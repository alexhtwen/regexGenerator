import sys
import os
import re
import time

import regex_demo_settings

SETTINGS = regex_demo_settings.settings[sys.argv[1]]
times = 99
starting_time = time.time()
for _ in range(times):
    count = 1
    with open(SETTINGS['file_in'], 'r') as f_in:
        with open('./dayi_out4_2.dat', 'w') as f_out:
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

                line_adjusted = f'{id}{code}{spaces}{word}\n'
                chars_written = f_out.write(line_adjusted)

            # 由於每一行的最後都加上\n換行碼，有些editors(如VS Code)在顯示時
            # 檔尾會多出一行，有些editors則不會。
            # 下面的兩行code是要在關檔前先刪除最後的那個\n。
            # 其實刪不刪大概無所謂，最少不會影響行數的計算。
            chars_total = f_out.seek(0, os.SEEK_END)
            f_out.seek(chars_total-1, os.SEEK_SET)
            f_out.truncate()

    # 如果想刪除檔案最後那個\n，但關檔前未處理，可以在這裡再開一次檔。
    # 不過，既然要刪，幹嗎關檔前不先做好，要關關開開的浪費時間？
    # 請注意：在這裡開檔，開檔模式不能用'wb'而要用'rb+'，否則前面的code是做白工。
    # with open(SETTINGS['file_out'], 'rb+') as f_out:
    # with open('./dayi_out4_2.dat', 'rb+') as f_out:
    #     f_out.seek(-1, os.SEEK_END)
    #     f_out.truncate()
finished_time = time.time()
print()
print(f'w mode and del before close: {finished_time - starting_time}')
print('------------------------')

starting_time = time.time()
for _ in range(times):
    count = 1
    with open(SETTINGS['file_in'], 'r') as f_in:
        # with open(SETTINGS['file_out'], 'wb') as f_out:
        with open('./dayi_out4_1.dat', 'w') as f_out:
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

                # .encode('utf8')
                line_adjusted = f'{id}{code}{spaces}{word}\n'
                chars_written = f_out.write(line_adjusted)

            # 由於每一行的最後都加上\n換行碼，有些editors(如VS Code)在顯示時
            # 檔尾會多出一行，有些editors則不會。
            # 下面的兩行code是要在關檔前先刪除最後的那個\n。
            # 其實刪不刪大概無所謂，最少不會影響行數的計算。
            # f_out.seek(-1, os.SEEK_END)
            # f_out.truncate()

    # 如果想刪除檔案最後那個\n，但關檔前未處理，可以在這裡再開一次檔。
    # 不過，既然要刪，幹嗎關檔前不先做好，要關關開開的浪費時間？
    # 請注意：在這裡開檔，開檔模式不能用'wb'而要用'rb+'，否則前面的code是做白工。
    with open('./dayi_out4_1.dat', 'rb+') as f_out:
        f_out.seek(-1, os.SEEK_END)
        f_out.truncate()
finished_time = time.time()
print()
print(f'w mode + open() again: {finished_time - starting_time}')


# print('SETTINGS:')
# print(SETTINGS)
# print(f"number of lines: {sum(1 for line in open(SETTINGS['file_out']))}")
# print('** The End of regex1_search.py **')
print()
