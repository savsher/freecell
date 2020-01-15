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

def show_desk(new=False):
    """ Show Buffer Desk and Home"""
    res = "::\n"
    def modify(x):
        out = ''
        if x == 0:
            out += ' --'
        elif x in range(1, 10):
            out += ' 0' + str(x)
        else:
            out += ' ' + str(x)
        return out

    for i in Buffer:
        res += modify(i)

    for i in range(len(Home)):
        try:
            card = Home[i][-1]
        except IndexError:
            card = 0
        res += modify(card)
    res += '\n _______________________'

    row = 0
    for i in range(len(Desk)):
        if len(Desk[i]) > row:
            row = len(Desk[i])
    for j in range(row):
        res = res + '\n'
        for i in range(len(Desk)):
            try:
                card = Desk[i][j]
            except IndexError:
                card = 0
            res += modify(card)
    res += '\n'
    if new:
        option = 'w'
    else:
        option = 'a'

    with open('result.log', option) as f:
        f.write(res)
    return res


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


def fit_desk(card, desk_cards):
    """ Try to put card to Desk """
    if card in KINGS:
        return None
    suit = (card - 1) // mn
    fit_suit = ((suit + 1) % 4, (suit + 3) % 4)
    fit_cards = [i for i in range(1, 53) if (i % mn == (card + 1) % mn) and ((i - 1) // mn in fit_suit)]
    for i in range(len(desk_cards)):
        if desk_cards[i] in fit_cards:
            return i
    return None


def move_card_to_buffer(card):
    for i in range(len(Buffer)):
        if Buffer[i] == 0:
            Buffer[i] = card
            return True
    return False


def initial_deal(random_desk=True):
    if random_desk:
        for s in Suit:
            Home[s] = [i for i in range(1, 52)]


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


def get_desk_cards(index=None):
    """ get current Desk cards """
    x = []
    for col in Desk:
        try:
            card = col[-1]
        except IndexError:
            card = 0
        finally:
            x.append(card)
    if index is not None:
        x.insert(index, 0)
    return tuple(x)


def fit_desk_cards(card, desk_cards):
    """ Try to put card to Desk """
    if card in KINGS:
        return None
    suit = (card-1)//mn
    fit_suit = ((suit+1) % 4, (suit+3) % 4)
    fit_cards = [i for i in range(1, 53) if (i % mn == (card+1) % mn) and ((i-1)//mn in fit_suit)]
    for i in range(len(desk_cards)):
        if desk_cards[i] in fit_cards:
            return i
    return None


def fit_two(card, card2):
    """ Check two cards for compability """
    if card in KINGS:
        return False
    suit = (card-1)//mn
    fit_suit = ((suit+1)%4, (suit+3)%4)
    fit_cards = [i for i in range(1, 53) if (i % mn == (card+1) % mn) and ((i-1)//mn in fit_suit)]
    if card2 in fit_cards:
        return True
    return False


def fit_together(cards):
    x = len(cards)-1
    while x > 0:
        if fit_two(cards[x], cards[x-1]):
            x -= 1
        else:
            return False
    return True


def buffer_size(adj_free_cell=0, adj_free_col=0):
    """ Calculate Total Buffer size
    return: ( free buffer cell, free column in desk, total size)
    """

    free_cell = 0
    for i in Buffer:
        if i == 0:
            free_cell += 1
    free_cell += adj_free_cell

    free_col = 0
    for col in Desk:
        if len(col) == 0:
            free_col += 1
    free_col += adj_free_col


    if free_cell >= 1:
        line_size = 2**free_col+(free_cell-1)
    else:
        line_size = 2**(free_col-1)

    total_size = ((free_cell+free_col)*(free_cell+free_col+1) - free_cell*(free_cell-1))//2

    return (free_cell, free_col, line_size, total_size)


def main():
    global Score
    start_flag = True
    dh_flag = bh_flag = bd_flag = dd_flag = db_flag = False
    show_desk(new=True)
    while start_flag:
        dh_flag = True
        Path.append(get_played_cards())
        # todo: DESK to HOME
        while dh_flag:
            dh_flag = False
            home_cards = get_wish_home_cards()
            desk_cards = get_desk_cards()
            for i in range(len(desk_cards)):
                if desk_cards[i] in home_cards:
                    card = Desk[i].pop()
                    suit = (card-1)//mn
                    Home[suit].append(card)
                    Score += 10
                    Path.append(get_played_cards())
                    dh_flag = True
                    show_desk()
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
                    Path.append(get_played_cards())
                    bh_flag = True
                    show_desk()
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
                    Path.append(get_played_cards())
                    bd_flag = True
                    show_desk()
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
            # todo: priority for nearest wish card
            for col in range(len(Desk)):
                for i in range(len(Desk[col])):
                    if Desk[col][i] in wish_cards:
                        tmp.append((col, len(Desk[col])-i+1))
            tmp = sorted(tmp, key=lambda x: x[1])
            for i in tmp:
                if i[0] not in wish_idx:
                    wish_idx.append(i[0])
            tmp = []
            # todo:  priority max cards ( Kings -> 2)
            for col in range(len(Desk)):
                try:
                    tmp.append((col, Desk[col][-1] % 13))
                except IndexError:
                    tmp.append((col, 0))
            tmp = sorted(tmp, key=lambda x: x[1], reverse=True)
            # todo:  complete wish_list
            for i in tmp:
                if i[0] not in wish_idx:
                    wish_idx.append(i[0])
            # todo: find move
            for i in wish_idx:
                # save from empty Desk columns
                try:
                    a = [Desk[i][-1]]
                except IndexError:
                    break
                #
                for j in range(len(Desk[i])-2, -1, -1):
                    if fit_two(a[-1], Desk[i][j]):
                        a.append(Desk[i][j])
                    else:
                        break
                _, _, _, total_size = buffer_size()
                if (len(a)-1) <= total_size:
                    idx = fit_desk_cards(a[-1], desk_cards)
                    if idx:
                        while a:
                            Path.append(get_played_cards())
                            Score -= 1
                            Desk[idx].append(a.pop())
                            Score -= 1
                        dh_flag = True
                        show_desk()
                        break
            if not dh_flag:
                db_flag = True
        # todo : DESK to BUFFER or DESK empty columns
        while db_flag:
            db_flag = False
            buf_size, col_size, line_size, total_size = buffer_size()
            if col_size == 0:
                cur_buf = 1
                nc_fit_home = []
                nc_fit_desk = []
                nc_no = []
                while cur_buf < total_size:
                    for i in range(len(Desk)):
                        if len(Desk[i]) == cur_buf:
                            _, _, _, new_total_size = buffer_size(adj_free_cell=(-1), adj_free_col=1)
                            if new_total_size > total_size:
                                nc_no.append(i)
                        cards = Desk[i][-cur_buf:]
                        if len(cards) == 2:
                            if fit_two(cards[0], cards[1]):
                                continue
                        elif len(cards) == 3:
                            if fit_two(cards[0], cards[1]) and fit_two(cards[1], cards[2]):
                                continue
                        elif len(cards) == 4:
                            if fit_two(cards[0], cards[1]) and fit_two(cards[1], cards[2])\
                                    and fit_two(cards[2], cards[3]):
                                continue
                        elif len(cards) == 5:
                            if fit_two(cards[0], cards[1]) and fit_two(cards[1], cards[2])\
                                    and fit_two(cards[2], cards[3]) and fit_two(cards[3], cards[4]):
                                continue
                        if fit_home(cards[0], get_home_cards()):
                            nc_fit_home.append(i)
                        if fit_desk(cards[0], get_desk_cards(index=i)):
                            nc_fit_desk.append(i)
                    if nc_fit_home:
                        for i in range(1, cur_buf+1):
                            move_card_to_buffer(Desk[nc_fit_home[0]][-i])
                            Path.append(get_played_cards())
                            Score -= 1
                        show_desk()
                        break
                    if nc_no:
                        for i in range(1, cur_buf+1):
                            move_card_to_buffer(Desk[nc_no[0]][-i])
                            Path.append(get_played_cards())
                            Score -= 1
                        show_desk()
                        break
                    if nc_fit_desk:
                        for i in range(1, cur_buf+1):
                            move_card_to_buffer(Desk[nc_fit_desk[0]][-1])
                            Path.append(get_played_cards())
                            Score -= 1
                        show_desk()
                        break
                    cur_buf += 1
                if cur_buf >= total_size:
                    show_desk()
                    print("'Can't move !!!!")
                    sys.exit(1)
            else:
                idx = None
                for i in range(len(Desk)):
                    if len(Desk[i]==0):
                        idx = i
                        break
                while line_size > 0:
                    for i in range(len(Desk)):
                        if len(Desk[i]) > line_size:
                            cards = Desk[i][-line_size:]
                            if fit_together(cards):
                                if fit_two(cards[0], Desk[-(line_size+1)]):
                                    continue
                                else:
                                    for card in cards:
                                        Desk[idx].append(card)
                                        Desk[i].pop()
                                    Score -= len(cards)*2
                                    Path.append(get_played_cards())
                                    show_desk()
                    line_size -= 1
                db_flag = True

    print('Score: {}'.format(Score))
    with open('path.log', 'w') as f:
        for i in Path:
            f.write(str(i)+'\n')


if __name__ == '__main__':
    main()