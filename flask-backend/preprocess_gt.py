# -*- coding: utf-8 -*-
# Copyright (c) 2022, Shang Luo
# All rights reserved.
# 
# Author: 罗尚
# Building Time: 2024/1/26
# Reference: None
# Description: None
from utils import read_json, write_json

if __name__ == '__main__':
    aaa = read_json('gt.json')
    # abc = aaa['c3t3'].split('\n')
    processed_gt = {}
    for key in aaa.keys():
        gt_list = aaa[key].split('\n')
        # print(gt_list[317:340])
        processed_gt[key] = {'gt_vocabs': [], 'pho_sym': [], 'meaning': []}
        # print(len(gt_list))
        for i in range(0, len(gt_list), 3):
            # print(i)
            processed_gt[key]['gt_vocabs'].append(gt_list[i])
            processed_gt[key]['pho_sym'].append(gt_list[i+1])
            processed_gt[key]['meaning'].append(gt_list[i+2])
    write_json('processed_gt.json', processed_gt)
    print(processed_gt)
