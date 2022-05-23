# -*- coding: utf-8 -*-
# @Time : 5/9/2022 9:18 AM
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
import collections

Card = collections.namedtuple("Card", ['rank', 'suit'])

suit_value = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_value) + suit_value[card.suit]


class FrenchDeck:
    suits = "spades diamonds clubs hearts".split()
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __str__(self):
        return "1"

    def __repr__(self):
        return "just 52 card"

    def __call__(self, *args, **kwargs):
        print(123)

    def __delattr__(self, item):
        del item


if __name__ == '__main__':
    deck = FrenchDeck()
    # for card in sorted(deck, key=spades_high):
    #     print(card)
    # delattr(deck, "_cards")
    deck()
