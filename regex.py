import os
import sys
from settings import general_info, messages
import regex_gen
from datetime import datetime

def parse_argv(params, option_dict: dict):
    # argv_info['err_code']: str = 0

    argv_info = {'err_code': 0, 'more_err_info': ''}

    if len(params) == 1:
        argv_info['err_code'] = 1
        pass
    else:
        option_names = {'bi': ('-g', '-b', '-r', '-o'),
                        'uni': ('-y', '-h', '-v')}
        params = params[1:]
        within_option = False
        for i, param in enumerate(params):
            if param in option_names['bi']:
                if within_option:
                    argv_info['err_code'] = -1
                    break
                else:
                    if param == '-g':
                        option = 'g'
                    elif param == '-b':
                        option = 'b'
                    elif param == '-r':
                        option = 'r'
                    elif param == '-o':
                        option = 'o'
                    else:
                        argv_info['err_code'] = -2
                        break
                    within_option = True
            elif param in option_names['uni']:
                if param == '-y':
                    option_dict['is_overwriting'] = True
                elif param == '-h':
                    # option_dict['show_help'] = True
                    argv_info['err_code'] = 1
                    break
                elif param == '-v':
                    # option_dict['show_version'] = True
                    argv_info['err_code'] = 2
                    break
                else:
                    print(f'param: {param}')
                    argv_info['err_code'] = -3
                    break
            else:  # 不屬於任何option_names，表示為option的「內容」。
                if within_option:
                    if option == 'g':   # good file
                        if not os.path.exists(param):
                            argv_info['err_code'] = -50
                            argv_info['more_err_info'] = param
                            break
                        option_dict['good_file'] = param
                    elif option == 'b':   # bad file
                        if not os.path.exists(param):
                            argv_info['err_code'] = -51
                            argv_info['more_err_info'] = param
                            break
                        option_dict['bad_file'] = param
                    elif option == 'r':
                        if not os.path.exists(param):
                            argv_info['err_code'] = -52
                            argv_info['more_err_info'] = param
                            break
                        option_dict['rules_file'] = param
                    elif option == 'o':
                        option_dict['output_file'] = param
                    else:
                        argv_info['err_code'] = -4
                        break
                    within_option = False
                else:
                    argv_info['more_err_info'] = param
                    argv_info['err_code'] = -5
                    break

        if argv_info['err_code'] == 0:
            if not option_dict['good_file']:
                argv_info['err_code'] = -6
            elif not option_dict['rules_file']:
                argv_info['err_code'] = -7
    return argv_info


if __name__ == '__main__':

    option_dict: dict = {
        'good_file': '',
        'bad_file': '',
        'rules_file': '',
        'output_file': '',
        'is_overwriting': False,
    }

    argv_info = parse_argv(sys.argv, option_dict)
    if argv_info['err_code'] < 0:
        print(
            f'\nerror {argv_info["err_code"]}: {messages["argv errors"][argv_info["err_code"]]}{argv_info["more_err_info"]}\n')
        exit(-1)
    elif argv_info['err_code'] == 1:
        print('Showing help: constructing...')
    elif argv_info['err_code'] == 2:
        print(
            f'version: {general_info["version"]}\ncreator: {general_info["creator"]}')
    else:
        reg = regex_gen.RegexGenerator(option_dict)
        pattern = reg.create_pattern()
        out_file = option_dict['output_file']
        if out_file:
            # print(option_dict['is_overwriting'])
            write_mode = 'w' if option_dict['is_overwriting'] else 'a'
            with open(out_file, write_mode) as f_out:
                content = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n' \
                          f'strict pattern: {pattern["strict"]}\n' \
                          f'loose pattern : {pattern["loose"]}\n\n'
                f_out.write(content)
        # reg.show_self()
