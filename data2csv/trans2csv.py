#!/usr/bin/env python
# encoding: utf-8
'''
@author: _
@time: 2019/4/26 08:30
@desc: 从文本文件转csv
'''

import os
import pandas as pd


def get_all_files(path, suffix):
    '''获取目录及子目录下所有以suffix为后缀名的文件路径'''

    file_list = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            _ = root + '/' + fn
            if _.endswith(suffix):
                print(_)
                file_list.append(_)

    return file_list


def get_data(file, tag):
    '''获取从单个文件中获取,信息转成列表'''

    data_list = list()

    with open(file, mode='r') as f:
        line_l = f.readlines()

    beg_index = None  # 默认标题起始行不存在
    for index, line in enumerate(line_l):

        if line.startswith(tag):
            beg_index = index
            print('头起始行号为:{lineno}\n'.format(lineno=index))
            break

    if beg_index is None:
        print('文件无内容')
    else:
        for item in line_l[beg_index + 1:]:
            data_l = item.strip().split(' ')
            data_list.append(data_l)

    return data_list



if __name__ == '__main__':

    p_list = []
    _dir = './data'  #待处理数据目录
    # xls = './out/s2p.xls'  # 处理后结果文件
    xls = './out/s2p.xlsx'  # 处理后结果文件
    writer = pd.ExcelWriter(xls)

    files = get_all_files(_dir, '.s2p')
    tag = '# Hz S dB R 50'  #标识符号, 真实数据从该标识符下一行开始

    for file in files:
        print('-' * 40)
        print('开始处理文件:{}'.format(file))
        data_list= get_data(file, tag)

        print('处理完毕,数据行数:{}\n'.format(len(data_list)))
        p_list.extend(data_list)

        df = pd.DataFrame(p_list)
        _, filename = os.path.split(file)
        df.to_excel(writer, sheet_name=filename.replace('.s2p', ''))

    writer.save()
    print('恭喜你,数据处理完毕!\n请查看处理结果: {}'.format(xls))