# -*- coding: utf-8 -*-
# (C) savsher@yandex.ru 20191203

import os
import sys

mn = 13
Score = 0

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

ACE = [i for i in range(1, 53) if i % mn == 1]
KINGS = [i for i in range(1, 53) if i % mn == 13]

def get_played_cards():
    """
    [ 1,2,3,4,5,6,7,8, 1,2,3,4, 1,2,3,4 ]
            Desk        Buffer    Home
    """
    x = []

    for col in Desk:
        try:
            card = col[-1]
        except IndexError:
            card = 0
        finally:
            x.append(card)
    for card in Buffer:
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


def fit_home(card, home_cards):
    """ Try to put card from Buffer or Desk to Home """
    suit = (card-1)//mn
    if home_cards[suit] == 0:
        # Ace
        if card == (suit * mn + 1):
            return True
    else:
        if home_cards[suit] == (card-1):
            return True
    return False





def initial_deal(random_desk=True):
    if random_desk:
        for s in Suit:
            Home[s] = [i for i in range(1, 52)]


def main():
    global Score
    global Path
    goto_desk_flag = True

    while True:
        played_cards = get_played_cards()
        print(played_cards)
        if sum(played_cards) == 0:
            break
        if len(Path) > 1:
            break
        Path.append(played_cards)
        buffer_idx = len(Desk)
        home_index = len(Desk) + len(Buffer)
        # todo: (?) B fit H
        # todo: (y)  B -> H, Path+=1, final, goto(B fit H)
        # todo: (n) (?) D fit H
        # todo:     (y) D -> H, Path+=1, final, goto(B fit H)
        for card in played_cards[:home_index]:
            suit = (card-1)//mn
            idx = played_cards.index(card)
            if card == 0:
                continue
            if fit_home(card, played_cards[home_index:]):
                if idx < buffer_idx:
                    Desk[idx].pop()
                else:
                    Buffer[Buffer.index(card)] = 0
                Home[suit].append(card)
                Score += 10
                goto_desk_flag = False
                break

        while goto_desk_flag:
            # todo:     (n) (?) D fit D
            # todo:         (y) D -> D, Path+=1, deadlock, goto(D fit H)
            for card in played_cardsl[:home_index]:
                if card == 0:
                    continue
                if idx < buffer_idx:
                    if fit_desk(card, played_cards[:buffer_idx]):
                        pass
                    if fit_buffer(card, played_cards[buffer_idx:home_index]):
                        pass

                # todo:         (n) (?) D fit B
                # todo:             (y) D -> B, Path+=1, deadlock, goto(D fit H)
                # todo:             (n) (?) B fit D
                # todo:                 (y) B -> D, Path+=1, deadlock, goto(D fit H)
                # todo:                 (n) deadlock
                pass

    #print("Desk: {}".format(Desk))
    print("Score: {}".format(Score))
    print("Path: {}".format(len(Path)))


def get_home_cards():
    """ get Home cards   """
    x = []
    for i in range(len(Home)):
        try:
            card = Home[i][-1]
        except IndexError:
            card = 0
        finally:
            x.append(card)
    return tuple(x)


def get_wish_home_cards():
    """ get desirable Home cards """
    x = []
    for i in range(len(Home)):
        try:
            card = Home[i][-1]
            if card != (i * mn + mn):
                card += 1
        except IndexError:
            card = (i * mn + 1)
        finally:
            x.append(card)
    return tuple(x)


def get_desk_cards():
    """ get current Desk cards """
    x = []
    for col in Desk:
        try:
            card = col[-1]
        except IndexError:
            card = 0
        finally:
            x.append(card)
    return tuple(x)


def fit_desk_cards(card, desk_cards):
    """ Try to put card to Desk """
    if card in KINGS:
        return None
    suit = (card-1)//mn
    fit_suit = ((suit+1)%4, (suit+3)%4)
    fit_cards = [i for i in range(1, 53) if (i % mn == (card+1) % mn) and ((i-1)//mn in fit_suit)]
    for i in range(len(desk_cards)):
        if desk_cards[i] in fit_cards:
            return i
    return None

def fit_together(card, card2):
    """ Check two cards for compability """
    if card in KINGS:
        return False
    suit = (card-1)//mn
    fit_suit = ((suit+1)%4, (suit+3)%4)
    fit_cards = [i for i in range(1, 53) if (i % mn == (card+1) % mn) and ((i-1)//mn in fit_suit)]
    if card2 in fit_cards:
        return True
    return False


def buffer_size():
    """ Calculate Total Buffer size
    return: ( free buffer cell, free column in desk, total size)
    """

    fbc = 0
    for i in Buffer:
        if i == 0:
            fbc += 1

    fdc = 0
    for col in Desk:
        if len(col) == 0:
            fdc += 1

    if fbc => 1:
        line_size = 2**fdc+(fbc-1)
    else:
        line_size = 2**(fdc-1)

    total_size = ((fbc+fdc)*(fbc+fdc+1) - fbc*(fbc-1))//2

    return (fbc, fdc, line_size, total_size)


def main2():
    global Score
    start_flag = True
    dh_flag = bh_flag = bd_flag = dd_flag = db_flag = False

    while start_flag:
        start_flag = False
        dh_flag = True
        # todo: DESK to HOME
        while dh_flag:
            dh_flag = False
            home_cards = get_wish_home_cards()
            desk_cards = get_desk_cards()
            print(desk_cards)
            for i in range(len(desk_cards)):
                if desk_cards[i] in home_cards:
                    card = Desk[i].pop()
                    suit = (card-1)//mn
                    Home[suit].append(card)
                    Score += 10
                    Path.append(card)
                    dh_flag = True
                    break
            if not dh_flag:
                bh_flag = True
        # todo: BUFFER to HOME
        while bh_flag:
            bh_flag = False
            home_cards = get_wish_home_cards()
            for i in range(len(Buffer)):
                if Buffer[i] in home_cards:
                    card = Buffer[i]
                    Buffer[i] = 0
                    suit = (card-1)//mn
                    Home[suit].append(card)
                    Score += 10
                    Path.append(card)
                    bh_flag = True
                    break
            if not bh_flag:
                bd_flag = True
        # todo : BUFFER to DESK (only not empty cells)
        while bd_flag:
            bd_flag = False
            desk_cards = get_desk_cards()
            for i in range(len(Buffer)):
                idx = fit_desk_cards(Buffer[i], desk_cards )
                if idx:
                    card = Buffer[i]
                    Buffer[i] = 0
                    Desk[idx].append(card)
                    Score -= 1
                    Path.append(card)
                    bd_flag = True
                    break
            if not bd_flag:
                dd_flag = True
        # todo : DESK to DESK (only not empty cells)
        while dd_flag:
            dd_flag = False
            desk_cards = get_desk_cards()
            # todo: find priority
            wish_cards = get_wish_home_cards()
            wish_idx = []
            tmp = []
            for col in range(len(Desk)):
                for i in range(len(Desk[col])):
                    if Desk[col][i] in wish_cards:
                        tmp.append((col, len(Desk[col])-i+1))
            tmp = sorted(tmp, key=lambda x: x[1])
            for i in tmp:
                if i[0] not in wish_idx:
                    wish_idx.append(i[0])
            tmp = []
            for col in range(len(Desk)):
                try:
                    tmp.append((col, Desk[col][-1] % 13))
                except IndexError:
                    tmp.append((col, 0))
            tmp = sorted(tmp, key=lambda x: x[1], reverse=True)
            for i in tmp:
                if i[0] not in wish_idx:
                    wish_idx.append(i[0])
            print(wish_idx)
            # todo: find move
            for i in wish_idx:
                try:
                    a = [Desk[i][-1]]
                except IndexError:
                    break
                for j in range(len(Desk[i])-2, -1, -1):
                    if fit_together(a[-1], Desk[i][j]):
                        a.append(Desk[i][j])
                    else:
                        break
                total_size = buffer_size()[2]
                if (len(a)-1) <= total_size:
                    idx = fit_desk_cards(a[-1], desk_cards)
                    if idx:
                        while a:
                            Path.append(Desk[i].pop())
                            Score -= 1
                            Desk[idx].append(a.pop())
                            Score -= 1
                        dh_flag = True
                        break
            if not dh_flag:
                db_flag = True
        # todo : DESK to BUFFER or DESK empty columns
        while db_flag:
            db_flag = False
            buf_size, col_size, line_size, total_size,  = buffer_size()
            if col_size ==0:


            else:

                pass


        print('Score: {}'.format(Score))


if __name__ == '__main__':
    #main()
    main2()