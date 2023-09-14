import random
import rules


class Deck:
    ranks = [str(n) for n in range(2, 10)] + list('TJQKA')
    suits = ['s', 'd', 'h', 'c']

    def __init__(self):
        self.cards = [(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return str(self.cards)

    def deal_one_card(self):
        return self.cards.pop()

    def pick_one_card(self, card):
        if card not in self.cards:
            return -1
        else:
            self.cards.remove(card)
            return card


class Shoe:
    def __init__(self, num_decks):
        self._shoe = []
        for _ in range(num_decks):
            deck = Deck()
            self._shoe.extend(deck.cards)

    def __str__(self):
        return str(self._shoe)

    def __len__(self):
        return len(self._shoe)

    def deal_one_card(self):
        return self._shoe.pop()

    def pick_one_card(self, card):
        if card not in self._shoe:
            return -1
        else:
            self._shoe.remove(card)
            return card

    def shuffle(self):
        return random.shuffle(self._shoe)


class Rotation:
    def __init__(self):
        self.players = {'s1': None, 's2': None, 's3': None, 's4': None, 's5': None, 's6': None}
        self.players_hands = {}
        self.players_hands_status = {}
        self.dealer_hand = []

    def sit_player(self, player, seat):
        if self.players[seat]:
            return -1

        self.players[seat] = player
        self.players_hands[seat] = []
        self.players_hands_status[seat] = None

        self.players_hands = dict(sorted(self.players_hands.items()))


class Engine:
    def __init__(self):
        self.shoe = Shoe(rules.num_decks)
        self.shoe.shuffle()

    def shuffle(self):
        self.shoe.shuffle()

    def remaining_cards(self):
        return self.shoe

    def deal_rotation(self, rotation):
        for _ in range(2):
            for player_sit in [p for p in rotation.players.keys() if rotation.players[p]]:
                rotation.players_hands[player_sit].append(self.shoe.deal_one_card())

            rotation.dealer_hand.append(self.shoe.deal_one_card())
