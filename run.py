# -*- coding: utf-8 -*-
# (C) savsher@yandex.ru 20191203

import os
import sys

mn = 13
Score = 0

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

def cur_cards():
    """ cards that can move """
    x = []
    for card in Buffer:
        x.append(card)
    for col in Desk:
        try:
            card = col[-1]
        except IndexError:
            card = 0
        finally:
            x.append(card)
    for col in Home:
        try:
            card = col[-1]
        except IndexError:
            card = 0
        finally:
            x.append(card)
    x = tuple(x)
    return x


def game_over():
    """ Check end of the game """
    if len(Home[0]) == mn:
        if len(Home[1] == mn):
            if len(Home[2] == mn):
                if len(Home[3]) == mn:
                    print('Score: {}'.format(Score))
                    print('Path: {}'.format(Path))
                    sys.exit(0)


def fit_home(card, cur_cards):
    suit = (card-1)//mn
    if cur_cards[suit+12] == 0:
        # Ace
        if card == (suit * mn + 1):
            idx = cur_cards.index(card)
            if idx < len(Buffer):
                Buffer[idx] = 0
                Home[suit].append[card]
                Path.append(cur_cards)
            else:
                Desk[idx-len(Buffer)].pop()
                Home[suit].append[card]
                Path.append(cur_cards)
            return True
        else:
            if cur_cards[suit+12] == (card + 1):
                return True
    return False


def initial_deal(random_desk=True):
    if random_desk:
        for s in Suit:
            Home[s] = [i for i in range(1, 52)]


def move_card_buffer_to_home(card):
    """ move card from buffer to home """
    global Score
    suit = (card - 1) // mn
    Home[suit].append(card)
    idx = Buffer.index(card)
    Buffer[idx] = 0
    Path.append({'B': idx, 'H': suit})
    Score += 10
    game_over()


def move_lcard_desk_to_home(col, card):
    """ move card from buffer to home """
    global Score
    suit = (card-1)//mn
    Home[suit].append(card)
    Path.append({'D': col, 'H': suit})
    Score += 10
    game_over()






def main():
    # todo: (?) B fit H
    # todo: (y)  B -> H, Path+=1, final, goto(B fit H)
    # todo: (n) (?) D fit H
    # todo:     (y) D -> H, Path+=1, final, goto(B fit H)
    while True:
        mv_cards = cur_cards()
        z = len(Buffer) + len(Desk)
        for card in mv_cards[z]:
            if card == 0:
                continue
            if fit_home(card, mv_cards):
                break
            else:
                # todo:     (n) (?) D fit D
                # todo:         (y) D -> D, Path+=1, deadlock, goto(D fit H)
                # todo:         (n) (?) D fit B
                # todo:             (y) D -> B, Path+=1, deadlock, goto(D fit H)
                # todo:             (n) (?) B fit D
                # todo:                 (y) B -> D, Path+=1, deadlock, goto(D fit H)
                # todo:                 (n) deadlock
                pass









    for card in Buffer:
        if card == 0:
            continue
        suit = (card - 1)//mn
        if Home[suit]:
            if Home[suit][-1] == (card + 1):
                move_card_buffer_to_home(card)
                continue
            else:
                if card == (suit * mn + 1):
                    move_card_buffer_to_home(card)
                    continue



if __name__ == '__main__':
    main()