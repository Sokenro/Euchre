# Euchre functions providing background computations for the game
# CS021

import random


def deal(shuffled_deck):
    """Deals out all the different hands from the shuffled cards,
returns a dictionary of player hands and the card on the stack"""
    # dividing the cards into each hand for each player
    player_hands = {}
    player_hands['bot1'] = shuffled_deck[0:5]
    player_hands['bot2'] = shuffled_deck[5:10]
    player_hands['bot3'] = shuffled_deck[10:15]
    player_hands['player'] = shuffled_deck[15:20]
    c_stack = shuffled_deck[20:21]

    return player_hands, c_stack


def shuffle(deck):
    """Take a deck of cards and shuffles them returning the shuffled cards"""
    random.shuffle(deck)
    return deck


def add_card(hand, selected_card):
    """Adds a card to the hand"""
    hand.append(selected_card)
    return hand


def find_jick(suit):
    """Figures out what the jick would be for a specific suit"""
    jick = ''
    # all jicks that go with each suit
    d = 'Jh'
    h = 'Jd'
    c = 'Js'
    s = 'Jc'
    # finding the jick associated with a suit
    if suit == 'd':
        jick = d
    elif suit == 'h':
        jick = h
    elif suit == 'c':
        jick = c
    elif suit == 's':
        jick = s
    return jick


def round_winner(trump, played_cards):
    """Checks who won the round and returns the winning team"""
    # base variables
    highest = -1
    possible_winners = []
    card_precedence = ('9', '1', 'J', 'Q', 'K', 'A')
    d = ('9d', '1d', 'Qd', 'Kd', 'Ad', 'Jh', 'Jd')
    h = ('9h', '1h', 'Qh', 'Kh', 'Ah', 'Jd', 'Jh')
    c = ('9c', '1c', 'Qc', 'Kc', 'Ac', 'Js', 'Jc')
    s = ('9s', '1s', 'Qs', 'Ks', 'As', 'Jc', 'Js')
    # finding which list from above is the correct trump precedence
    if trump == 'd':
        trump_precedence = d
    elif trump == 'h':
        trump_precedence = h
    elif trump == 'c':
        trump_precedence = c
    elif trump == 's':
        trump_precedence = s
    # checking for any trump that was played
    for card in played_cards:
        if card in trump_precedence:
            possible_winners.append(card)

    # checking if there was no trump played
    if possible_winners == []:
        first_card = list(played_cards.keys())[0]
        # checking for all cards played on suit and disregarding others
        for card in played_cards:
            if first_card[1] == card[1]:
                possible_winners.append(card)
        # checking which card wins out of all cards left
        for card in possible_winners:
            card_power = card_precedence.index(card[0])
            # checking which card is most powerful
            if card_power > highest:
                highest = card_power
        # getting the first letter of the card that matters
        winning_power = card_precedence[highest]
        # obtaining the card that won from the list of possible winners
        for card in possible_winners:
            if card[0] == winning_power:
                winning_card = card

    # checking which card is the winner in trump
    else:
        # iterating through all trump cards to find the most powerful
        for card in possible_winners:
            card_power = trump_precedence.index(card)
            # checking which card is most powerful
            if card_power > highest:
                highest = card_power
        # getting the specific card that won
        winning_card = trump_precedence[highest]

    # figuring out who won based on which card won
    winner = played_cards[winning_card]
    return winner


def play_order_round(winner, play_order):
    """Takes the current play order and the winner of the previous round
and returns the new play order"""
    # getting the place of the winner
    winners_place = play_order.index(winner)
    # looping through to switch around the play order
    for i in range(winners_place):
        play_order.append(play_order.pop(0))
    return play_order


def play_order_dealer(dealer_order):
    """Changes the dealer to the player on the left of the dealer"""
    dealer_order.append(dealer_order.pop(0))
    return dealer_order


def give_points(makers, player_tricks):
    """Assigns points based on which team was the makers and how many
tricks were won by the player team and the bot team"""
    player_points = 0
    bot_points = 0
    # checking which team the makers are
    if makers == 'bot2' or makers == 'player':
        makers = True
    else:
        makers = False
    # figuring out how many tricks the bots won
    bot_tricks = 5 - player_tricks
    # assigning points for the player team based on tricks won
    # and who the makers are
    if player_tricks > 2 and makers is False:
        player_points = 2
    elif player_tricks == 5 and makers is True:
        player_points = 2
    elif (player_tricks == 3 or player_tricks == 4) and makers is True:
        player_points = 1

    # assigning points to the bots based on tricks won and makers
    if bot_tricks > 2 and makers is True:
        bot_points = 2
    elif bot_tricks == 5 and makers is False:
        bot_points = 2
    elif (bot_tricks == 3 or bot_tricks == 4) and makers is False:
        bot_points = 1

    return player_points, bot_points
