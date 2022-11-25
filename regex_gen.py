# import time
import copy
from pprint import pprint


class RegexGenerator():

    def __init__(self, option_dict: dict):
        # print(f'option_dict: {option_dict}')
        self.good_file: str = option_dict['good_file']
        self.bad_file: str = option_dict['bad_file']
        self.rules_file: str = option_dict['rules_file']
        self.output_file: str = option_dict['output_file']
        self.is_overwriting: bool = option_dict['is_overwriting']
        self.good_strs: list = []
        self.bad_strs: list = []
        self.rules: list = []

    def show_self(self):
        print(
            '\n'
            f'self.good_file: {self.good_file}\n\n'
            f'self.bad_file: {self.bad_file}\n\n'
            f'self.rules_file    : {self.rules_file}\n\n'
            f'self.output_file   : {self.output_file}\n\n'
            f'self.is_overwriting: {self.is_overwriting}\n\n'
            f'self.good_strs: {self.good_strs}\n\n'
            f'self.bad_strs: {self.bad_strs}\n\n'
            f'self.rules         : {self.rules}\n'
        )

    def file_to_list(self, file):
        with open(file) as fs:
            lines = fs.read()
        return lines.splitlines()


    def optimize(self, units, optimizer):
        """以optimizer為依據，最佳化chars。

        Args:
            units (list): 元素為代表每一單位的小list，小list的每個元素
                         為代表每一個字元的set。
            optimizer (list): list的元素是dict。用來最佳化chars的模板。

        Returns:
            optimized: 最佳化後的list。
        """
        optimized = []

        # print(f'cols: {cols}')
        for unit in units:
            unit_set = set()
            unit_str = ''
            for char_set in unit:
                char_list = list(char_set)
                char_list.sort()
                chars = ''.join(char_list)  # 這時chars已是sort過的字串。
                for opt_item in optimizer:
                    if chars == opt_item['content']:
                        chars = opt_item['symbol']
                        # print('**********')
                        break
                unit_set.add(chars)
                unit_str += chars

            if len(unit_set) == 1:
                len_unit = len(unit)
                # if len_unit == 1 and (unit_str[0] + unit_str[-1]) != '[]':  # FIXME: and 後面的判斷有bug，萬一真正的字串剛好是'['開頭']'結尾呢？
                if (unit_str[0] + unit_str[-1]) != '[]':  # FIXME: and 後面的判斷有bug，萬一真正的字串剛好是'['開頭']'結尾呢？
                    for char in unit_set:
                        # print('**', char)
                        char = f'[{char}]' if len_unit == 1 else char
                        quantifier = '' if len_unit == 1 else f'{{{len_unit}}}'
                        unit_str = f'{char}{quantifier}'

            # print(chars)
            optimized.append(unit_str)

        # print(f'within: {optimized}')
        return optimized

    def create_pattern(self):
        print('\n\n** ================================= **\n')
        shorthands = {    # 暫時用不到
            'quantifiers': {
                'total': ('*', '+', '?'),
            },
        }

        elements = [  # regex的各種主要元素(未窮盡)
            {
                'name': 'alphabets_upper',
                'symbol': '[A-Z]',
                'content': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'strictness': 500,
            },
            {
                'name': 'alphabets_lower',
                'symbol': '[a-z]',
                'content': 'abcdefghijklmnopqrstuvwxyz',
                'strictness': 500,
            },
            {
                'name': 'alphabets',
                'symbol': '[A-Z]',
                'content': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                'strictness': 400,
            },
            {
                'name': 'numbers',
                'symbol': r'\d',
                'content': '0123456789',
                'strictness': 400,

            },
            {
                'name': 'words',
                'symbol': r'\w',
                'content': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_',
                'strictness': 300,

            },
            {
                'name': 'spaces',
                'symbol': r'\s',
                'content': ' \t\r\n\v\f',
                'strictness': 300,

            },
        ]

        quan_short = {
            '0-n': '*',
            '1-n': '+',
            '0-1': '?'
        }

        pattern = {
            'strict': '',
            'loose': '(未完成，敬請期待...)',

        }

        # print(chars)
        # print(quan_short)
        self.good_strs = self.get_goods()
        self.rules = self.get_rules()
        if self.bad_file:
            self.bad_strs = self.get_bads()

        # try:
        unit_len_pairs = []
        for rule in self.rules:
            rule = rule.strip()   # 字串處理的一個「撇步」，是先砍掉前後的空白。
            if rule.isdigit():
                unit_len_pairs.append((int(rule),))   # 存成tuple用意是rules檔某些列有可能用'1, 3'等描述該欄有1-3字元。
            else:   # TODO: 暫未處理rules檔有非數字情形。
                if rule == '*':
                    unit_len_pairs.append((0, 'n'))
                elif rule == '+':
                    unit_len_pairs.append((1, 'n'))
                elif rule == '?':
                    unit_len_pairs.append((0, 1))
                else:
                    # col_lens.append((-1, -1))
                    pass

        # print(f'col_lens: {unit_lens}')
        # pprint(f'good_strs: {self.good_strs}')
        # print('------------')
        # print()
        # exit()
        start_pos = 0
        symbols_strict = []   # 嚴格pattern
        symbols_loose = []    # 寬鬆pattern
        for unit_len_pair in unit_len_pairs:  # 取出每個單位的長度
            if len(unit_len_pair) == 1:  # rules.dat檔每列只有1個數字，即每欄(單位)長度固定。
                unit_len = unit_len_pair[0]
                unit_list = [set() for _ in range(unit_len)]
                chars_set_strict = set()
                chars_set_loose = set()
                # raw_char = set()
                for good_str in self.good_strs:
                    stop_pos = start_pos + unit_len
                    unit_chars = good_str[start_pos:stop_pos]
                    # this_chars_list = []
                    # unit_char_set = set()
                    # print(len(unit_list))
                    for char_seq, char in enumerate(unit_chars):
                        unit_list[char_seq].add(char)
                # chars_set_strict.add(unit_list)
                symbols_strict.append(unit_list)
                start_pos += unit_len_pair[0]
            else:  # TODO: 暫不處理長度不固定者。
                raise Exception('這個程式目前很笨，rules file不能處理非固定長度的規則唷(夠笨了吧)。')
        # print(symbols_strict)
        symbols_strict = self.optimize(units=symbols_strict, optimizer=elements)
        # print(f'symbols_strict: {symbols_strict}')
        pattern['strict'] = f'^{"".join(symbols_strict)}$'
        print(pattern['strict'])
        return pattern


                        # for char in chars:
                        #     print(f'char: {char}')
                        #     raw_char.add(char)
                        #     for element in elements:
                        #         if char in element['content']:
                        #             # print(element['strictness'], strictness)
                        #             chars_set_strict.add(
                        #                 element['symbol'])
                        #             # strictness = element['strictness']
                        #             # pass
                        #     print(
                        #         f'11 total_symbols: {total_symbols}, this_symbols_strict: {chars_set_strict}')
                        #     # 第0筆時total_symbols是空set，所以將this_symbols_strict的所有元素deepcopy過去。
                        #     if str_seq == 0:
                        #         total_symbols = copy.deepcopy(chars_set_strict)
                        #     # total_symbols有資料時，就和this_symbols_strict做交集運算，目的在取得
                        #     # 每筆資料的共同的elements，例如\w, \d, [A-Z], ...等。
                        #     else:
                        #         total_symbols = total_symbols & chars_set_strict  # Intersection
                        #     print(
                        #         f'22 total_symbols: {total_symbols}, this_symbols_strict: {chars_set_strict}')
                        #     # print(total_symbols)
                        # print(f'\nraw_char: {raw_char}\n')
                    # print(f'len(total_symbols): {len(total_symbols)}')
                    # if len(total_symbols) == 1:  # TODO: 待處理...
                    #     pass
                    # elif len(total_symbols) > 1:
                    #     print('---------------------------')
                    #     symbols = list(total_symbols)  # 跑完匹配檔後得到的各欄symbols。
                    #     print('==============================')
                    #     print(f'symbols at last: {symbols}  {type(symbols)}')
                    #     # exit()

                    #     strictness = elements[0]['strictness']
                    #     print(f'strictness: {strictness}')
                    #     # print(type(strictness))
                    #     for symbol in symbols:
                    #         print(f'--- symbol: {symbol}' )
                    #         for element in elements:  # elements是已建好的regex主要元素表。
                    #             print(f'33: element["symbol"]: {element["symbol"]}  element["strictness"]: {element["strictness"]}  strictness: {strictness}')
                    #             if element['symbol'] == symbol:
                    #                 print()
                    #                 if element['strictness'] < strictness:
                    #                     total_symbols.remove(symbol)
                    #                     print(f'{symbol} removed.')
                    #                     strictness = element['strictness']
                    #         # {'\\d', '\\w'}
                    #         # print(symbol)
                    # else:  # TODO: 沒有任何匹配的symbol？有可能嗎？
                    #     raise Exception('以輸入的匹配檔，發現沒有任何匹配的regex pattern。')

                    # print(f'total_symbols: {total_symbols}')
                    # print()
                    # pattern['strict'] += list(total_symbols)[0]
                    # print(pattern['strict'])

                    # offset += unit_len[0]








            # ------------------------------------
            #         total_symbols = set()
            #         this_symbols_strict = set()
            #         raw_char = set()
            #         for str_seq, good_str in enumerate(self.good_strs):
            #             chars = good_str[offset: offset+unit_len[0]]
            #             print(f'\nchars: {chars}')
            #             this_symbols_strict = set()   # 嚴格pattern
            #             this_symbols_loose = set()    # 寬鬆pattern
            #             for char in chars:
            #                 print(f'char: {char}')
            #                 raw_char.add(char)
            #                 for element in elements:
            #                     if char in element['content']:
            #                         # print(element['strictness'], strictness)
            #                         this_symbols_strict.add(
            #                             element['symbol'])
            #                         # strictness = element['strictness']
            #                         # pass
            #                 print(
            #                     f'11 total_symbols: {total_symbols}, this_symbols_strict: {this_symbols_strict}')
            #                 # 第0筆時total_symbols是空set，所以將this_symbols_strict的所有元素deepcopy過去。
            #                 if str_seq == 0:
            #                     total_symbols = copy.deepcopy(this_symbols_strict)
            #                 # total_symbols有資料時，就和this_symbols_strict做交集運算，目的在取得
            #                 # 每筆資料的共同的elements，例如\w, \d, [A-Z], ...等。
            #                 else:
            #                     total_symbols = total_symbols & this_symbols_strict  # Intersection
            #                 print(
            #                     f'22 total_symbols: {total_symbols}, this_symbols_strict: {this_symbols_strict}')
            #                 # print(total_symbols)
            #             print(f'\nraw_char: {raw_char}\n')
            #         # print(f'len(total_symbols): {len(total_symbols)}')
            #         if len(total_symbols) == 1:  # TODO: 待處理...
            #             pass
            #         elif len(total_symbols) > 1:
            #             print('---------------------------')
            #             symbols = list(total_symbols)  # 跑完匹配檔後得到的各欄symbols。
            #             print('==============================')
            #             print(f'symbols at last: {symbols}  {type(symbols)}')
            #             # exit()

            #             strictness = elements[0]['strictness']
            #             print(f'strictness: {strictness}')
            #             # print(type(strictness))
            #             for symbol in symbols:
            #                 print(f'--- symbol: {symbol}' )
            #                 for element in elements:  # elements是已建好的regex主要元素表。
            #                     print(f'33: element["symbol"]: {element["symbol"]}  element["strictness"]: {element["strictness"]}  strictness: {strictness}')
            #                     if element['symbol'] == symbol:
            #                         print()
            #                         if element['strictness'] < strictness:
            #                             total_symbols.remove(symbol)
            #                             print(f'{symbol} removed.')
            #                             strictness = element['strictness']
            #                 # {'\\d', '\\w'}
            #                 # print(symbol)
            #         else:  # TODO: 沒有任何匹配的symbol？有可能嗎？
            #             raise Exception('以輸入的匹配檔，發現沒有任何匹配的regex pattern。')

            #         print(f'total_symbols: {total_symbols}')
            #         print()
            #         pattern['strict'] += list(total_symbols)[0]
            #         print(pattern['strict'])

            #         offset += unit_len[0]
                # else:  # TODO: 暫不處理長度不固定者。

                #     raise Exception('這個程式目前很笨，rules file不能處理非固定長度的規則唷(夠笨了吧)。')

        # except Exception as e:
        #     print(e)
        # finally:
        #     print(pattern['strict'])
        #     return ''

    def get_goods(self):
        # self.good_strs: list = self.read_file(self.good_file)
        return self.file_to_list(self.good_file)
        # print(f'good_strs: {self.good_strs}\n')

    def get_bads(self):
        # self.bad_strs: list = self.read_file(self.bad_file)
        return self.file_to_list(self.bad_file)
        # print(f'bad_strs: {self.bad_strs}\n')

    def get_rules(self):
        # self.rules: list = self.read_file(self.rules_file)
        return self.file_to_list(self.rules_file)
        # print(f'rules: {self.rules}\n')
