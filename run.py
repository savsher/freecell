# -*- coding: utf-8 -*-
# (C) savsher@yandex.ru 20191203

import os
import numpy as np

Suit = ('h', 's', 'd', 'c')
Home = dict()
Desk = ([], [], [], [], [], [], [], [])
Buffer = []


def initial_deal():
    for s in Suit:
        Home[s] = [(s, i) for i in range(1, 14)]



def main():
    # todo: home
    print(Desk)

if __name__ == '__main__':
    main()