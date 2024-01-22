# All the functions needed to run the bots in a game of Euchre
# CS021

import Game_Functions as gf


# card precedence is used in many functions to determine card powers
CARD_PRECEDENCE = ('9', '1', 'J', 'Q', 'K', 'A')


def hand_suits_choose(bot_hand):
    """Checks how many cards of a suit are in hand if in the
choose trump phase returns a dictionary of suits in hand"""
    diam = ('9d', '1d', 'Jd', 'Qd', 'Kd', 'Ad')
    heart = ('9h', '1h', 'Jh', 'Qh', 'Kh', 'Ah')
    club = ('9c', '1c', 'Jc', 'Qc', 'Kc', 'Ac')
    spade = ('9s', '1s', 'Js', 'Qs', 'Ks', 'As')
    diam_count = 0
    heart_count = 0
    club_count = 0
    spade_count = 0
    # iterate through hand and check cards
    for card in bot_hand:
        if card in diam:
            diam_count += 1
        if card in heart:
            heart_count += 1
        if card in club:
            club_count += 1
        if card in spade:
            spade_count += 1
    # making dictionary of suites in hand
    hand_suits = {}
    hand_suits['d'] = diam_count
    hand_suits['h'] = heart_count
    hand_suits['c'] = club_count
    hand_suits['s'] = spade_count
    return hand_suits


def suits_in_hand(bot_hand, trump):
    """checks how many cards of each suit is in the bots hand and
returns a dictionary of how many of each suit there is"""
    d_cnt = 0
    h_cnt = 0
    c_cnt = 0
    s_cnt = 0
    suits = ['d', 'h', 'c', 's']
    base_cards = ('9', '1', 'J', 'Q', 'K', 'A')
    jick = gf.find_jick(trump)
    # getting a list of all cards in a suit
    for suit in suits:
        # getting base list of cards
        suit_cards = []
        for base in base_cards:
            card = base + suit
            suit_cards.append(card)
        # adding the jick to the trump suit
        if suit == trump:
            suit_cards.append(jick)
        # taking the jick out of its original suit
        if suit == jick[1]:
            suit_cards.remove(jick)
        # checking how many of each suit the hand has
        for card in bot_hand:
            if suit == 'd':
                if card in suit_cards:
                    d_cnt += 1
            elif suit == 'h':
                if card in suit_cards:
                    h_cnt += 1
            elif suit == 'c':
                if card in suit_cards:
                    c_cnt += 1
            elif suit == 's':
                if card in suit_cards:
                    s_cnt += 1

    # making dictionary of how many of each suite in hand
    hand_suits = {}
    hand_suits['d'] = d_cnt
    hand_suits['h'] = h_cnt
    hand_suits['c'] = c_cnt
    hand_suits['s'] = s_cnt
    return hand_suits


def bot_pick_up(hand_suits, bot_hand, c_stack):
    """Checks the cards in the bots hand compared to the card in the stack
and returns the bots decision to pick up or pass as a boolean"""
    # converting the card on stack to the trump suit
    trump = c_stack[1]
    # Picking up the card if the bot has 3 or more cards of trump
    if hand_suits[trump] > 2:
        pick_up = False
    else:
        # evaluating the total power of cards in the bots hand
        hand_power = 0
        for card in bot_hand:
            card_power = CARD_PRECEDENCE.index(card[0])
            hand_power += card_power
        # picking it up if the bot has a greater hand power than the average
        if hand_power > 15 and hand_suits[trump] > 1:
            pick_up = False
        # passing if the hand power is lower than the average
        else:
            pick_up = True
    return pick_up


def bot_pick_suit(bot_hand, c_stack, turn_num):
    """Checks if a bot wants to pick a suit for trump or pass and returns
the picked suit or a string pass"""
    picked_suit = ''
    highest = -1
    lowest = 7
    # possible trump suit precedences
    d = ('9d', '1d', 'Qd', 'Kd', 'Ad', 'Jh', 'Jd')
    h = ('9h', '1h', 'Qh', 'Kh', 'Ah', 'Jd', 'Jh')
    c = ('9c', '1c', 'Qc', 'Kc', 'Ac', 'Js', 'Jc')
    s = ('9s', '1s', 'Qs', 'Ks', 'As', 'Jc', 'Js')
    # list of all suits
    useable_suits = ['d', 'h', 'c', 's']
    # removing the unpickable suit (the suit previously on the stack)
    unusable_suit = useable_suits.index(c_stack[1])
    useable_suits.pop(unusable_suit)
    # picking a suit if there are 3 or more of a pickable suit in hand
    three_of_suit = 0
    suits_of_three = []
    for suit in useable_suits:
        # finding power of the potential trump suit
        if suit == 'd':
            trump_precedence = d
        elif suit == 'h':
            trump_precedence = h
        elif suit == 'c':
            trump_precedence = c
        elif suit == 's':
            trump_precedence = s
        # getting the number of each suit in hand
        hand_suits = suits_in_hand(bot_hand, suit)
        # checking if it has 3 or more of one suit in hand
        for suit in hand_suits:
            if suit in useable_suits and hand_suits[suit] >= 3:
                suits_of_three.append(suit)
                three_of_suit += 1
        # if they have more than one possible set of 3 find highest
        if three_of_suit != 1:
            for suit in suits_of_three:
                # finding power of the potential trump suit
                if suit == 'd':
                    trump_precedence = d
                elif suit == 'h':
                    trump_precedence = h
                elif suit == 'c':
                    trump_precedence = c
                elif suit == 's':
                    trump_precedence = s
                # looking at cards to determine the more powerful set of 3
                total_power = 0
                for card in bot_hand:
                    if card in trump_precedence:
                        card_power = trump_precedence.index(card)
                        total_power += card_power
                # finding the higher set of 3
                if total_power > highest:
                    highest = total_power
                    picked_suit = suit
    # pick suit if they have 2 high power cards and one singleton ace
    # check for 2 high power cards in one suit
    for suit in useable_suits:
        # getting the number of each suit in hand
        hand_suits = suits_in_hand(bot_hand, suit)
        # checking hand suits for 2 or more high trump
        for suit in hand_suits:
            jick = gf.find_jick(suit)
            if hand_suits[suit] == 2:
                # finding power of the potential trump suit
                if suit == 'd':
                    trump_precedence = d
                elif suit == 'h':
                    trump_precedence = h
                elif suit == 'c':
                    trump_precedence = c
                elif suit == 's':
                    trump_precedence = s
                # finding all cards of the suit and their power
                total_power = 0
                for card in bot_hand:
                    if card in trump_precedence:
                        card_power = trump_precedence.index(card)
                        total_power += card_power
                # if they have enough power checking for off suit ace
                if total_power >= 9:
                    for card in bot_hand:
                        if card[0] == 'A' and (card not in trump_precedence):
                            picked_suit = suit

    # checking if they are the last to pick and being forced to pick if so
    if turn_num == 3:
        return useable_suits[0]
    elif picked_suit != '':
        return picked_suit
    # passing if there is no desirable suit to pick
    else:
        return 'pass'


def bot_remove_card(bot_hand, c_stack):
    """Removes the worst card in a bots hand after they are told to pick
it up and returns the new hand"""
    trump = c_stack[1]
    lowest = 6
    # looping through the hand to find the lowest card
    for card in bot_hand:
        # checking if the card is not in the trump suit
        if trump not in card:
            # getting the card number
            card_num = card[0]
            # getting a numeric value for the power of the card
            card_power = CARD_PRECEDENCE.index(card_num)
            # checking if the cards power is lower than any other before it
            if card_power <= lowest:
                lowest = card_power
    # if the hand is entirely trump then checking for the lowest trump
    if lowest == 6:
        # looping through the hand to find lowest card
        for card in bot_hand:
            card_num = card[0]
            card_power = CARD_PRECEDENCE.index(card_num)
            # making the card the new lowest if it's lower than any others
            if card_power <= lowest:
                lowest = card_power
        # getting the number for the lowest card
        lowest_num = CARD_PRECEDENCE[lowest]
        # looping through the hand to choose the lowest card
        for card in bot_hand:
            if card[0] == lowest_num:
                removal_card = bot_hand.index(card)
    # removing lowest card if the hand is not entirely trump
    else:
        lowest_num = CARD_PRECEDENCE[lowest]
        # looping through hand to choose the lowest card not in trump
        for card in bot_hand:
            if trump not in card:
                if card[0] == lowest_num:
                    removal_card = bot_hand.index(card)
    # removing the lowest card
    bot_hand.pop(removal_card)
    return bot_hand


def bot_play_card(trump, bot_hand, played_cards):
    """Chooses a card for the bots to play and returns the card to play
and the new hand"""
    # This function commonly references card power. The card power is
    # the index of the card in the associated card precedence tuple
    # this is used to find the most and least powerful cards in hand
    card_to_play = ''
    highest = -1
    lowest = 7
    # possible trump suit precedences
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

    # ***Bot Plays First***
    # checking if bot is the first to play
    if played_cards == {}:
        # leading off suit aces
        for card in bot_hand:
            if card[0] == 'A' and card[1] != trump:
                card_to_play = card
        # If the bot has the jack of trump playing that first
        if card_to_play == '':
            for card in bot_hand:
                if card == ('J' + trump):
                    card_to_play = card
        # bot tries to throw a low trump to draw out higher ones
        # bot prefers lower cards to throw
        if card_to_play == '':
            for card in bot_hand:
                if card[0] == '9' and card[1] == trump:
                    card_to_play = card
                elif card[0] == '1' and card[1] == trump:
                    card_to_play = card
        # if the bot has no high cards to lead throwing out some trash
        if card_to_play == '':
            for card in bot_hand:
                if (card[0] == '9' or card[0] == '1') and card[1] != trump:
                    card_to_play = card
                elif card[0] == 'Q' and card != trump:
                    card_to_play = card
        # if none of the above is in hand playing a random card
        if card_to_play == '':
            card_to_play = bot_hand[0]

    # ***Bot Not Playing First***
    else:
        # finding the suit that must be followed
        first_card = list(played_cards.keys())[0]
        # finding the jick
        jick = gf.find_jick(trump)
        # making the suit to follow trump if the jick is lead
        if first_card == jick:
            follow_suit = trump
        else:
            follow_suit = first_card[1]

        # ***Finding the Winning Card on the Stack***
        # checking if someone has trumped yet
        played_trump = []
        for card in played_cards:
            if card in trump_precedence:
                played_trump.append(card)

        # ***If the Stack Hasn't Been Trumped***
        if played_trump == []:
            # find the highest card on the stack
            for card in played_cards:
                card_power = CARD_PRECEDENCE.index(card[0])
                if card_power > highest:
                    highest = card_power
            # do we have cards to follow
            following_cards = []
            for card in bot_hand:
                if card[1] == follow_suit:
                    following_cards.append(card)
            # if we have cards on suit
            if following_cards != []:
                # if we have following cards can they beat the stack
                cards_beating_stack = []
                for card in following_cards:
                    card_power = CARD_PRECEDENCE.index(card[0])
                    if card_power > highest:
                        cards_beating_stack.append(card)
                # if not play the lowest
                if cards_beating_stack == []:
                    for card in following_cards:
                        card_power = CARD_PRECEDENCE.index(card[0])
                        if card_power < lowest:
                            lowest = card_power
                            card_to_play = card
                # if so beat it with the lowest to win
                else:
                    for card in cards_beating_stack:
                        card_power = CARD_PRECEDENCE.index(card[0])
                        if card_power < lowest:
                            lowest = card_power
                            card_to_play = card
            # if bot doesn't have cards on suit
            else:
                # can we trump it
                trump_in_hand = []
                for card in bot_hand:
                    if card in trump_precedence:
                        trump_in_hand.append(card)
                # if so play lowest trump
                if trump_in_hand != []:
                    for card in trump_in_hand:
                        card_power = trump_precedence.index(card)
                        if card_power < lowest:
                            lowest = card_power
                            card_to_play = card
                # if not play lowest card
                else:
                    for card in bot_hand:
                        card_power = CARD_PRECEDENCE.index(card[0])
                        if card_power < lowest:
                            lowest = card_power
                            card_to_play = card

        # ***If Trump Was Played on the Stack***
        else:
            # ***Check if Trump was Lead***
            if follow_suit == trump:
                # what is the highest trump on the stack
                for card in played_trump:
                    stack_power = trump_precedence.index(card)
                    if stack_power > highest:
                        highest = stack_power

                # do we have trump
                trump_in_hand = []
                for card in bot_hand:
                    if card in trump_precedence:
                        trump_in_hand.append(card)
                # if we have trump do we have higher
                if trump_in_hand != []:
                    trump_beat_stack = []
                    for card in trump_in_hand:
                        card_power = trump_precedence.index(card)
                        if card_power > highest:
                            trump_beat_stack.append(card)
                    # if so play the lowest to win
                    if trump_beat_stack != []:
                        for card in trump_beat_stack:
                            card_power = trump_precedence.index(card)
                            if card_power < lowest:
                                lowest = card_power
                                card_to_play = card
                    # if not play the lowest trump in hand
                    else:
                        for card in trump_in_hand:
                            card_power = trump_precedence.index(card)
                            if card_power < lowest:
                                lowest = card_power
                                card_to_play = card
                # if no trump play the lowest card in hand
                else:
                    for card in bot_hand:
                        card_power = CARD_PRECEDENCE.index(card[0])
                        if card_power < lowest:
                            lowest = card_power
                            card_to_play = card

            # ***Stack Contains Trump but not Lead***
            else:
                # check if we have cards to follow suit
                following_cards = []
                for card in bot_hand:
                    if card[0] == follow_suit:
                        following_cards.append(card)
                # if so play the lowest non trump
                if following_cards != []:
                    for card in bot_hand:
                        card_power = CARD_PRECEDENCE.index(card[0])
                        if card_power < lowest and card[1] != trump:
                            lowest = card_power
                            card_to_play = card
                # if not can the bot beat trump
                else:
                    # what is the highest trump on the stack
                    for card in played_trump:
                        stack_power = trump_precedence.index(card)
                        if stack_power > highest:
                            highest = stack_power
                    # does the bot have trump
                    trump_in_hand = []
                    for card in bot_hand:
                        if card in trump_precedence:
                            trump_in_hand.append(card)
                    # if the bot has trump is it higher than the stack
                    if trump_in_hand != []:
                        trump_beat_stack = []
                        for card in trump_in_hand:
                            card_power = trump_precedence.index(card)
                            if card_power > highest:
                                trump_beat_stack.append(card)
                        # if so play the lowest to win
                        if trump_beat_stack != []:
                            for card in trump_beat_stack:
                                card_power = trump_precedence.index(card)
                                if card_power < lowest:
                                    lowest = card_power
                                    card_to_play = card
                    # if no higher trump playing the lowest non-trump card
                    else:
                        for card in bot_hand:
                            card_power = CARD_PRECEDENCE.index(card[0])
                            if card_power < lowest and card[1] != trump:
                                lowest = card_power
                                card_to_play = card

        # checking if the bot has selected a card yet
        if card_to_play == '':
            # if not playing the first card in hand
            card_to_play = bot_hand[0]

    # ***Removing the Card***
    # checking the index of the card to remove from hand
    card_removal = bot_hand.index(card_to_play)
    # removing the card from the bots hand
    bot_hand.pop(card_removal)
    return card_to_play, bot_hand
