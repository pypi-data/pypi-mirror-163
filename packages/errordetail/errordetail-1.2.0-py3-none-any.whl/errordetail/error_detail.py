# -- coding: utf-8 --
import os
import sys
import time
import traceback


def get_error_detail(filename=None, title=None):
    error_info = sys.exc_info()
    if filename is None:
        filename = str(os.path.basename(sys.argv[0]))[:-3]
    with open(f'{filename}.errlog', 'a', encoding='utf8') as f:
        error_str = f'ERROR OCCURRED，{time.strftime("%Y-%m-%d %H:%M:%S")}：\n {error_info[0]}: {error_info[1]}'
        if title:
            print(f"{title}: \n{error_str}", file=f)
        else:
            print(error_str, file=f)  # 错误类型，错误概述
        traceback.print_tb(error_info[2], file=f)  # 错误细节描述
        f.write(f"{'=' * 50}\n")

