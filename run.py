# -*- coding: utf-8 -*-
# (C) savsher@yandex.ru 20191203

import os
import sys

mn = 13

Suit = ('h', 's', 'd', 'c')
Home = ([], [], [], [])
Desk = ([44, 43, 14, 47, 26, 52, 13],
        [3, 49, 36, 51, 19, 10, 11],
        [48, 17, 22, 31, 23, 7, 15],
        [12, 25, 21, 37, 5, 32, 16],
        [1, 46, 39, 28, 29, 2],
        [50, 24, 30, 8, 34, 33],
        [40, 42, 18, 45, 38, 4],
        [35, 41, 9, 20, 6, 27])
Buffer = [0, 0, 0, 0]
Path = []
NoPath = []
Score = 0


def game_over():
    if len(Home[0]) == mn:
        if len(Home[1] == mn):
            if len(Home[2] == mn):
                if len(Home[3]) == mn:
                    print('Score: {}'.format(Score))
                    print('Path: {}'.format(Path))
                    sys.exit(0)


def initial_deal(random_desk=True):
    if random_desk:
        for s in Suit:
            Home[s] = [i for i in range(1, 52)]


def move_card_buffer_to_home(suit, card):
    """ move card from buffer to home """
    Home[suit].append(card)
    idx = Buffer.index(card)
    Buffer[idx] = 0
    Path.append({'B': idx, 'H': suit})
    Score += 10
    game_over()

def move():
    # todo: (?) B fit H
    for card in Buffer:
        if card == 0:
            continue
        suit = (card-1)//mn
        if Home[suit]:
            if Home[suit][-1] == (card-1):
                Home[suit].append(card)
                idx = Buffer.index(card)
                Buffer[idx] = 0
                Path.append({'B': idx, 'H': suit})
                Score += 10
                game_over()
                continue
            else:
                if card == (suit*mn+1):
                    Home[suit].append(card)
                    idx = Buffer.index(card)
                    Buffer[idx] = 0



    # todo: (y)  B -> H, Path+=1, final, goto(B fit H)
    # todo: (n) (?) D fit H
    # todo:     (y) D -> H, Path+=1, final, goto(B fit H)
    # todo:     (n) (?) D fit D
    # todo:         (y) D -> D, Path+=1, deadlock, goto(D fit H)
    # todo:         (n) (?) D fit B
    # todo:             (y) D -> B, Path+=1, deadlock, goto(D fit H)
    # todo:             (n) (?) B fit D
    # todo:                 (y) B -> D, Path+=1, deadlock, goto(D fit H)
    # todo:                 (n) deadlock
    print(Path)

def main():
    # todo: Movement
    initial_deal(False)
    # todo: ? B fit H
    for i in Buffer:
        col = (i-1)//mn
        if Home[col]:
            if Home[col][-1] == i-1:
                Home[col].append(i)
                move = {'B': Buffer.index(i), 'H': col}
                Path.append(move)
                Score += 10
                game_over()
                continue
        else:
            if i == (col * mn + 1):
                Home[col].append(i)
                move = {'B': Buffer.index(i), 'H': col}
                Path.append(move)
                Score += 10
                game_over()
                continue
    # todo: ? D fit H
    # todo:     y:
    """
    todo: ? D in H
    """

if __name__ == '__main__':
    main()