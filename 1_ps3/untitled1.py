#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 15:52:46 2023

@author: albarh22
"""

def custom_repeat(Ln, L):
    new_dict = {}
    new_list = []
    for i in range(len(Ln)):
        new_dict[L[i]] = Ln[i]
    print(new_dict)

    while len(new_dict) > 0:
        key = list(new_dict.keys())[0]
        index = L.index(key)
        for i in range(new_dict[key] - 1):
            L.insert(index + i, key)
        new_dict.pop(key)

L = ['a','b','c']
custom_repeat([1,2,3], L)
#print(L)

dict1 = {1:'a', 2:'b', 3:'c', 5: 'u' , 4: 'k'}
print(dict1.keys())