settings = {
    '1': {
        'file_in': './dayi_trivial.dat',  # 牛刀小試
        # 'file_in': './dayi_very_short.dat',
        'file_out': './dayi_out1.dat',
        'has_id': False,
        'len_code_padding': 10   # code以及其後空白合計的長度。
    },
    '2': {
        'file_in': './dayi_trivial.dat',
        'file_out': './dayi_out2.dat',
        'has_id': True,
        'len_id': 3,
        'pad_id': '',  # 補足id長度的字元。
        'spaces_after_id': 2,
        'len_code_padding': 12  # code以及其後空白合計的長度。
    },
    '3': {
        'file_in': './dayi_trivial.dat',
        'file_out': './dayi_out3.dat',
        'has_id': True,
        'len_id': 2,
        'pad_id': '0',  # 補足id長度的字元。
        'spaces_after_id': 1,
        'len_code_padding': 9   # code以及其後空白合計的長度。
    },
    '4': {
        'file_in': './dayi_120000.dat',   # 大展神威
        'file_out': './dayi_out4.dat',
        'has_id': True,
        'len_id': 8,
        'pad_id': '0',  # 補足id長度的字元。
        'spaces_after_id': 3,
        'len_code_padding': 11  # code以及其後空白合計的長度。
    },
}
