from basic_components import Engine, Rotation
import rules


def convert_card(card):
    rank = card[0]

    if rank.isdigit():
        return int(rank)
    elif rank == 'A':
        return 11
    else:
        return 10


def convert_hand(hand):
    hand_values = []
    for card in hand:
        hand_values.append(convert_card(card))

    if sum(hand_values) <= 21:
        return hand_values

    while True:
        if 11 not in hand_values:
            return hand_values

        if sum(hand_values) <= 21:
            return hand_values

        for i in range(len(hand_values)):
            if hand_values[i] == 11:
                hand_values[i] = 1
                break


def get_options(hand):
    options = ['hit', 'stand']
    hand_values = convert_hand(hand)

    if sum(hand_values) > 21:
        return 'bust'

    if len(hand) == 2 and sum(hand_values) == 21:
        return 'blackjack'

    if sum(hand_values) == 21:
        return '21'

    if len(hand) > 2:
        return options

    if rules.double_any or (9 >= sum(hand_values) >= 11):
        options.insert(1, 'double')

    if convert_card(hand[0]) == convert_card(hand[1]):
        options.insert(-2, 'split')

    return options


def get_decision(hand, options, bot=None):
    if bot is not None:
        decision = bot(hand, options)
        return decision

    abbreviation = {'h': 'hit', 's': 'stand', 'sp': 'split', 'd': 'double'}

    decision = input(f"{options}: ")
    if decision in abbreviation:
        decision = abbreviation[decision]

    if decision not in options:
        return -1

    return decision


def dealer(hand, options, hit_soft=False):
    hand_values = convert_hand(hand)

    if sum(hand_values) <= 16:
        return 'hit'

    if hit_soft and sum(hand_values) == 17 and 11 in hand_values:
        return 'hit'

    if sum(hand_values) > 16:
        return 'stand'


def play_hand(engine, hand, bot=None):
    while True:
        print(hand)
        options = get_options(hand)

        if options == 'bust' or options == 'blackjack':
            return options

        if options == '21':
            return hand

        decision = get_decision(hand, options, bot=bot)
        if decision == -1:
            pass
        elif decision == 'stand':
            return hand
        elif decision == 'double':
            hand.append(engine.shoe.deal_one_card())
            return hand
        elif decision == 'hit':
            hand.append(engine.shoe.deal_one_card())
        elif decision == 'split':
            return
        else:
            return -1


def resolve_rotation(rotation):
    pass


def play_rotation(engine, rotation):
    if rules.check_for_bj and get_options(rotation.dealer_hand) == 'blackjack':
        resolve_rotation(rotation)

    for player_seat in [p for p in rotation.players.keys() if rotation.players[p]]:
        rotation.players_hands_status = play_hand(engine, rotation.players_hands[player_seat])

    if not all([status in ['blackjack', 'bust'] for status in rotation.players_hands_status]):
        play_hand(engine, rotation.dealer_hand, dealer)


e = Engine()
r = Rotation()
r.sit_player('david', 's2')
# r.sit_player('jon', 's4')
# r.sit_player('bob', 's1')

e.deal_rotation(r)
play_rotation(e, r)
print(r.players_hands, r.dealer_hand)
