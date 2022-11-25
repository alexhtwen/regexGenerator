import sys
import os
import re
import time

import regex_demo_settings

# %%
SETTINGS = regex_demo_settings.settings[sys.argv[1]]
count = 1
chars_written = 0
with open(SETTINGS['file_in'], 'r') as f_in:
    with open(SETTINGS['file_out'], 'w') as f_out:
        # with open(SETTINGS['file_out'], 'wb') as f_out:
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
            # line_adjusted = f'{id}{code}{spaces}{word}\n'.encode('utf8')
            chars_written += f_out.write(line_adjusted)
            # print(line_adjusted, end='')

        # 由於每一行的最後都加上\n換行碼，有些editors(如VS Code)在顯示時
        # 檔尾會多出一行，有些editors則不會。
        # 下面的兩行code是要在關檔前先刪除最後的那個\n。
        # 其實刪不刪大概無所謂，最少不會影響行數的計算。
        # 可以這樣刪除(目前我傾向用這個方法)：
        # bytes_file_out = f_out.seek(0, os.SEEK_END)
        # print(f'輸出檔原先的bytes數: {bytes_file_out}')
        # f_out.seek(bytes_file_out - 1, os.SEEK_SET)
        # f_out.truncate()
        # print()

# 如果想刪除檔案最後那個\n，但關檔前未處理，可以在這裡再開一次檔。
# 注意：在這裡開檔，開檔模式要用'ab', 'ab+', 或'rb+'。
# 錯用：如使用'w', 'w+', 'wb', 或'wb+'模式，前面的code是「做白工」，
#       而且會產生Exception。
# 討論：...
# 經測試，這種寫法和關檔前刪除相比，速度稍快一點，不過差異非常小，可不計。
# 本人比較喜歡在關檔前就處理好，不另外再開一次檔。
# with open(SETTINGS['file_out'], 'ab') as f_out:
#     f_out.seek(-1, os.SEEK_END)
#     # f_out.seek(0, os.SEEK_END)
#     f_out.truncate()

print('SETTINGS:')
print(SETTINGS)
print(f"number of lines: {sum(1 for line in open(SETTINGS['file_out']))}")
print('** The End of regex1_search.py **')
print()
