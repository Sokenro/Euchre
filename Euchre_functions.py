# Class: CS 021
# Functions to create portions of the card game Euchre
# and to assist in the display of those portions

import pygame
import button as b
import Game_Functions as gf
import Bot_functions as bf
import time

# initialize pygame
pygame.init()


def scale_image(image, scale):
    """scales an image to the desired size"""
    width = image.get_width()
    height = image.get_height()
    # multiply the width and height by the scale multiplier
    new_img = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    return new_img


def rotate_image(image, degrees):
    """rotates the image the specified amount of degrees
returns the image"""
    new_img = pygame.transform.rotate(image, degrees)
    return new_img


def height_factor(image, desired_height):
    """returns the correct scale factor to get the image to
the desired height"""
    height = image.get_height()
    return desired_height / height


def load_image(name, is_card):
    """loads an image and returns the loaded image"""
    if is_card:
        path = f'Cards\{name}'
    else:
        path = f'Images\{name}'

    return pygame.image.load(path)


def gather_imgs_load(player_hands, c_stack):
    """adds together all the cards that need to be loaded into a single
dictionary"""
    imgs_to_load = player_hands
    imgs_to_load['c_stack'] = c_stack
    imgs_to_load['back'] = ['cb']
    return imgs_to_load


def array_display_x(surface, image, init_x, y, change_x, count):
    """displays a linear array of the image to screen of the specified count
from left to right on the screen"""
    x = init_x
    for _ in range(count):
        display_image(surface, image, x, y)
        x += change_x


def array_display_y(surface, image, x, init_y, change_y, count):
    """displays a linear array of the image to screen of the specified count
from left to right on the screen"""
    y = init_y
    for _ in range(count):
        display_image(surface, image, x, y)
        y += change_y


def display_image(surface, image, x, y):
    """displays an image to screen at specific coordinates"""
    surface.blit(image, (x, y))


def message_cords(current_player):
    """returns the bots message coordinates depending on which turn it is
format turn_x, turn_y"""
    if current_player == 'bot1':
        turn_x = 170
        turn_y = 375
        return turn_x, turn_y
    elif current_player == 'bot2':
        turn_x = 504
        turn_y = 170
        return turn_x, turn_y
    elif current_player == 'bot3':
        turn_x = 838
        turn_y = 375
        return turn_x, turn_y


def main_menu(surface):
    """Plays the main menu selection for euchre, returns False if
the user selects the quit option, returns True if start is selected
and returns True for new game when start is selected, False otherwise"""
    # load images to be used to variables
    is_card = False
    start = load_image('Start.jpeg', is_card)
    inst = load_image('Instructions.jpeg', is_card)
    exit_img = load_image('Exit.jpeg', is_card)
    title = load_image('Title.png', is_card)
    rules = load_image('Rules.png', is_card)
    back = load_image('Back.jpg', is_card)

    # ***IMAGE HEIGHTS FOR SCALING***
    bttn_h = 100
    # title scale factor
    title_sf = .25

    # scale title image to the correct dims
    title_img = scale_image(title, title_sf)

    # ***IMAGE COORDINATES***
    start_x = 395
    start_y = 341
    # instructions button
    inst_x = 396
    inst_y = 491
    # exit button
    exit_x = 394
    exit_y = 641
    # back button
    back_x = 750
    back_y = 650
    # title image
    title_x = 324
    title_y = 20
    # rules image
    rules_x = 142
    rules_y = 0

    # ***MAKE BUTTONS***
    # Button function takes (x, y, image, scale)
    start_bttn = b.Button(start_x, start_y, start, height_factor(start, bttn_h))
    instructions_bttn = b.Button(inst_x, inst_y, inst, height_factor(inst, bttn_h))
    exit_bttn = b.Button(exit_x, exit_y, exit_img, height_factor(exit_img, bttn_h))
    back_bttn = b.Button(back_x, back_y, back, height_factor(back, 75))

    # screen color
    off_white = (248, 246, 229)

    # ***MENU LOOP***
    rules_page = False
    running = True
    while running:

        # color the screen
        surface.fill(off_white)

        # main menu page
        if not rules_page:
            # display the title image
            display_image(surface, title_img, title_x, title_y)
            # if start is selected exit the loop and do nothing
            if start_bttn.draw(surface):
                new_game = True
                return True, new_game
            # if instructions is selected go to the rules page
            if instructions_bttn.draw(surface):
                rules_page = True
            if exit_bttn.draw(surface):
                new_game = False
                # return false to end the whole program in the main game loop
                return False, new_game

        # when instructions is selected go to the rules tab
        else:
            display_image(surface, rules, rules_x, rules_y)
            if back_bttn.draw(surface):
                rules_page = False

        # update the display every loop
        pygame.display.update()

        # exit the game if the X (close window) is selected
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                new_game = False
                return False, new_game


def round_play(surface, play_order):
    """deals the cards and plays one round of the game; choose trump
and one full hand of tricks, returns the player points and bot points
if the tab is closed returns 0, 0"""
    # there are return statements under the event loops to correctly exit
    # and a return statement at the end to return the score

    # name constants
    player = 'player'
    bot1 = 'bot1'
    bot2 = 'bot2'
    bot3 = 'bot3'

    # define the deck
    deck = ['9d', '1d', 'Jd', 'Qd', 'Kd', 'Ad', '9h', '1h', 'Jh', 'Qh', 'Kh', 'Ah',
            '9c', '1c', 'Jc', 'Qc', 'Kc', 'Ac', '9s', '1s', 'Js', 'Qs', 'Ks', 'As']
    # shuffle the cards
    shuffled_deck = gf.shuffle(deck)

    # deal the cards into the player_hands dictionary and c_stack
    player_hands, c_stack = gf.deal(shuffled_deck)

    # ***LOAD IMAGES***
    # get all card images
    cards_to_load = gather_imgs_load(player_hands, c_stack)

    # card images to dictionary
    is_card = True
    card_imgs = {}
    # go through each item in the list, load the image, add it to dict
    for key in cards_to_load:
        cards = cards_to_load[key]
        for card in cards:
            card_name = card + '.PNG'
            card_image = load_image(card_name, is_card)
            card_imgs[card] = card_image

    # non card images
    is_card = False
    # load suit button images to dictionary
    suits = ['s', 'h', 'c', 'd']
    suit_bttn_imgs = {}
    for suit in suits:
        image_name = suit + '_bttn' + '.jpg'
        suit_image = load_image(image_name, is_card)
        suit_bttn_imgs[suit] = suit_image
    # remove the c_stack card as you will not be able to choose that button
    del suit_bttn_imgs[c_stack[0][1]]
    suits.remove(c_stack[0][1])

    # load the rest of the images
    pick_bttn = load_image('PickUp.jpg', is_card)
    pass_img = load_image('Pass.jpg', is_card)
    trump_img = load_image('Trump.png', is_card)
    or_img = load_image('Or.png', is_card)
    discard_img = load_image('discard.png', is_card)
    b_pass = load_image('b_pass.jpg', is_card)
    b_pickup = load_image('b_pickup.jpg', is_card)
    deal_crown = load_image('Crown.png', is_card)

    # ***IMAGE HEIGHTS FOR SCALING***
    # cards
    card_h = 150
    # bot messages
    msg_h = 50
    # pick, pass, or choose button
    p_bttn_h = 45
    # text height
    txt_h = 80
    # dealer crown
    crown_h = 50
    # suit button
    suit_bttn_h = 50
    # bot card rotation degrees
    rot_deg = 90

    # ***SCALE IMAGES***
    # bot messages
    b_pass = scale_image(b_pass, height_factor(b_pass, msg_h))
    b_pickup = scale_image(b_pickup, height_factor(b_pickup, msg_h))
    # card back scaled and rotated
    scaled_back = scale_image(card_imgs['cb'], height_factor(card_imgs['cb'], card_h))
    roted_back = rotate_image(scaled_back, rot_deg)
    # c_stack card
    c_stack_img = scale_image(card_imgs[c_stack[0]], height_factor(card_imgs[c_stack[0]], card_h))
    # discard a card text
    discard_img = scale_image(discard_img, height_factor(discard_img, txt_h))
    # Or text
    or_img = scale_image(or_img, height_factor(or_img, txt_h))
    # choose trump text
    trump_img = scale_image(trump_img, height_factor(trump_img, txt_h))
    # dealer crown
    deal_crown = scale_image(deal_crown, height_factor(deal_crown, crown_h))

    # ***IMAGE COORDINATES***
    # c_stack image
    c_stack_x = 435
    c_stack_y = 325
    # flipped deck
    deck_x = 545
    deck_y = c_stack_y
    # bot hands starting locations
    # bot 1
    bot1_x = 10
    bot1_y = 130
    # bot 2
    bot2_x = 270
    bot2_y = 10
    # bot 3
    bot3_x = 920
    bot3_y = 130
    # player cards starting location
    x = 270
    y = 640
    # pickup button
    pick_bttn_x = 350
    pick_bttn_y = 558
    # pass button
    pass_bttn_x = 600
    pass_bttn_y = pick_bttn_y
    # c_stack button
    c_bttn_x = 490
    c_bttn_y = 480
    # discard a card text
    dis_x = 339
    dis_y = 410
    # suit button starting location
    s_bttn_x = 418
    s_bttn_y = 430
    # choose trump text
    c_trump_x = 387
    c_trump_y = 350
    # or text
    or_x = 476
    or_y = 505
    # choose trump section pass button
    ct_pass_x = 474
    ct_pass_y = 585
    # dealer crown
    # see PREGAME SETUP for crown coordinates

    # ***ARRAY RATES OF CHANGE***
    # this is the distance between each card in
    bot_y_change = 110
    bot_x_change = 110
    # offset of each player card
    x_change = bot_x_change
    # suit button
    s_bttn_change_x = 85

    # ***MAKE BUTTONS***
    # players cards dictionary
    bttns = {}
    for card in player_hands[player]:
        card_bttn = b.Button(x, y, card_imgs[card], height_factor(card_imgs[card], card_h))
        bttns[card] = card_bttn
        x += x_change
    # choose suit buttons dictionary
    s_bttns = {}
    for suit in suits:
        # shorten below line by assigning variable
        smol_img = suit_bttn_imgs[suit]
        suit_bttn = b.Button(s_bttn_x, s_bttn_y, smol_img, height_factor(smol_img, suit_bttn_h))
        s_bttns[suit] = suit_bttn
        s_bttn_x += s_bttn_change_x
    # other buttons to be used
    pick_bttn = b.Button(pick_bttn_x, pick_bttn_y, pick_bttn, height_factor(pick_bttn, p_bttn_h))
    pass_bttn = b.Button(pass_bttn_x, pass_bttn_y, pass_img, height_factor(pass_img, p_bttn_h))
    c_stack_bttn = b.Button(c_bttn_x, c_bttn_y, c_stack_img, 1)  # card already scaled
    # choose section pass button
    ct_pass_bttn = b.Button(ct_pass_x, ct_pass_y, pass_img, height_factor(pass_img, p_bttn_h))

    # ***PREGAME SETUP***
    # background color
    green = (10, 115, 10)
    # assign the dealer
    dealer = play_order[3]
    # dealer crown coordinates
    if dealer == bot1:
        crown_x = 0
        crown_y = 80
    elif dealer == bot2:
        crown_x = 810
        crown_y = 0
    elif dealer == bot3:
        crown_x = 1017
        crown_y = 670
    elif dealer == player:
        crown_x = 207
        crown_y = 750

    # assign trump to variable for functionality
    trump = 0
    # determining what players turn it is depends on the iteration
    iteration = -1
    # boolean to enter the pickup or pass phase
    pickup = True
    # boolean to enter the choose trump phase
    choose = False
    # boolean to skip the choose phase if the window is closed
    x_out = False
    # some things need to be done if specific cards are selected
    card_clicked = False
    # the c_stack is needs a gate to prevent it from being displayed
    # during the incorrect phase of play
    c_stack_display = True
    # boolean to disallow double selecting items
    mouse_clicked = False
    # wait time after a bot plays
    wait_time = 1.5

    # ***GAME LOOP***
    running = True
    while running:
        # allow the user to exit when the x is hit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                x_out = True
                # returns 0, 0 so the program does not throw an error when exit
                return 0, 0
            # reset mouse clicked to allow the user to select buttons again
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False

        # ***NON CONDITIONAL DISPLAY ITEMS***
        # background color
        surface.fill(green)
        # display bot hands to screen
        # bot 1
        array_display_y(surface, roted_back, bot1_x, bot1_y, bot_y_change, (len(player_hands['bot1'])))
        # bot 2
        array_display_x(surface, scaled_back, bot2_x, bot2_y, bot_x_change, (len(player_hands['bot2'])))
        # bot 3
        array_display_y(surface, roted_back, bot3_x, bot3_y, bot_y_change, (len(player_hands['bot3'])))

        # display players cards on screen
        for card in bttns:
            if bttns[card].draw(surface):
                # allow player to remove card from hand if trump is chosen
                # and they are the dealer (they picked up the card)
                if trump != 0 and dealer == player:
                    if mouse_clicked is False:
                        player_hands[player].remove(card)
                        running = False
                        # if player discards set card_clicked to true
                        card_clicked = True
                        mouse_clicked = True

        if trump != 0 and dealer == player and c_stack_display:
            # draw the discard statement to screen
            display_image(surface, discard_img, dis_x, dis_y)
            # create the c_stack card button if the player picks up the card
            if c_stack_bttn.draw(surface):
                if mouse_clicked is False:
                    # allow the player to discard this card from hand
                    player_hands[player].remove(card)
                    running = False
                    mouse_clicked = True
            # if card in hand was selected for discard remake the card buttons
            # with the new hand
            elif card_clicked:
                # player cards starting location
                x = 270
                y = 640
                # remake the buttons with new hand
                bttns = {}
                for card in player_hands[player]:
                    card_bttn = b.Button(x, y, card_imgs[card], height_factor(card_imgs[card], card_h))
                    bttns[card] = card_bttn
                    x += x_change

        # display the dealer crown on the dealer during the pickup
        # and choose phases
        if pickup or choose:
            display_image(surface, deal_crown, crown_x, crown_y)

        # enter the pickup phase if no one has chosen trump and exit if
        # everyone has passed
        if pickup and iteration <= 3:
            if iteration == -1:
                iteration += 1

            # set current player depending on the iteration
            current_player = play_order[iteration]

            # locate coordinates for bot messages
            if current_player != player:
                turn_x, turn_y = message_cords(current_player)

            # display the c_stack and deck if in pickup or pass phase
            # overturned deck
            display_image(surface, scaled_back, deck_x, deck_y)
            # c_stack card
            display_image(surface, c_stack_img, c_stack_x, c_stack_y)

            # ***PLAYER TURN***
            if current_player == player:
                # if player chooses pickup, the card is added to dealers hand,
                # and trump is chosen
                if pick_bttn.draw(surface):
                    player_hands[dealer] = gf.add_card(player_hands[dealer], c_stack[0])
                    # card chosen exit pickup phase
                    pickup = False
                    trump = c_stack[0][1]
                    mouse_clicked = True

                # if pass is selected do nothing move to next turn
                if pass_bttn.draw(surface):
                    iteration += 1
                    mouse_clicked = True

            # ***BOT TURNS***
            else:
                hand_suits = bf.suits_in_hand(player_hands[current_player], c_stack[0][1])
                # returns True if bot passes, and False if bot picks up
                pickup = bf.bot_pick_up(hand_suits, player_hands[current_player], c_stack[0])
                # if bot passes do nothing move onto the next turn
                if pickup:
                    iteration += 1
                    # display bot pass message and wait 1.5 seconds
                    display_image(surface, b_pass, turn_x, turn_y)
                    pygame.display.update()
                    time.sleep(wait_time)

                # if bot picks up add card to dealer hand and set trump
                if pickup is False:
                    # display bot pickup message and wait 1.5 seconds
                    display_image(surface, b_pickup, turn_x, turn_y)
                    pygame.display.update()
                    time.sleep(wait_time)
                    player_hands[dealer] = gf.add_card(player_hands[dealer], c_stack[0])
                    trump = c_stack[0][1]
            # if dealer is a bot allow them to discard an extra card from hand
            if dealer != player and pickup is False:
                player_hands[dealer] = bf.bot_remove_card(player_hands[dealer], c_stack[0])
                running = False

        # ***CHOOSE TRUMP SECTION***
        # if everyone passes iteration is 4
        if iteration == 4:
            c_stack_display = False
            pickup = False
            choose = True
            iteration = -1
        # enter the choose trump section on correct conditions
        if choose and iteration <= 3:
            if iteration == -1:
                iteration += 1

            # set current player
            current_player = play_order[iteration]

            # set bot message cordinates
            if current_player != player:
                turn_x, turn_y = message_cords(current_player)

            # ***PLAYER TURN***
            if current_player == player:
                # display the choose trump message and the suit buttons
                display_image(surface, trump_img, c_trump_x, c_trump_y)
                for s_bttn in s_bttns:
                    # if a suit button is selected set trump and exit the loop
                    if s_bttns[s_bttn].draw(surface):
                        trump = s_bttn
                        running = False
                # on the last turn do not allow user to pass
                # otherwise display pass button and allow passing
                if iteration < 3:
                    display_image(surface, or_img, or_x, or_y)
                    if ct_pass_bttn.draw(surface):
                        # if pass go to the next turn
                        iteration += 1

            else:
                # find number of suits in bot hand
                hand_suits = bf.hand_suits_choose(player_hands[current_player])
                # decide what to pick based on suits in hand
                trump = bf.bot_pick_suit(hand_suits, c_stack[0], iteration)
                # if bot passes display pass message,
                # wait 1.5 second, and iterate
                if trump == 'pass':
                    # display pass bot message
                    display_image(surface, b_pass, turn_x, turn_y)
                    pygame.display.update()
                    time.sleep(wait_time)
                    iteration += 1
                    # if bot chooses trump display suit,
                    # wait 1.5 seconds and exit loop
                else:
                    # shorten line below by assigning variable
                    shrt_img = suit_bttn_imgs[trump]
                    suit_img = scale_image(shrt_img, height_factor(shrt_img, suit_bttn_h))
                    display_image(surface, suit_img, turn_x, turn_y)
                    pygame.display.update()
                    time.sleep(wait_time)
                    running = False
        # update the display every loop
        pygame.display.update()

    # unless the player has Xed out the tab continue
    if not x_out:
        # ***MAIN GAMEPLAY (TRICKS)***
        # for scoring determine who is the maker
        makers = current_player

        # ***LOAD IMAGES***
        # choose a card to play text
        cardplay = load_image('card_play.png', is_card)
        # trump indicator
        trump_ind = trump + '.png'
        trump_ind = load_image(trump_ind, is_card)

        # ***IMAGE HEIGHTS FOR SCALING***
        # trump indicator
        trump_ind_h = 100
        # degrees rotation bot 1
        b1_degs = 90
        # degrees rotation bot 2
        b3_degs = 270

        # ***SCALE IMAGES***
        cardplay = scale_image(cardplay, height_factor(cardplay, txt_h))
        # trump indicator
        trump_ind = scale_image(trump_ind, height_factor(trump_ind, trump_ind_h))

        # ***IMAGE COORDINATES***
        # player played card
        player_x = 490
        player_y = 455
        # bot 1 played card
        b1_card_x = 335
        b1_card_y = 350
        # bot 2 played card
        b2_card_x = 490
        b2_card_y = 195
        # bot 3 played card
        b3_card_x = 595
        b3_card_y = 350
        # choose a card to play txt
        cardplay_x = 339
        cardplay_y = 550
        # trump indicator
        trump_ind_x = 495
        trump_ind_y = 352

        # ***PRE GAME SETUP***
        # iteration to determine who the current player is
        iteration = -1
        # each trick is one round, we want to play 5
        trick = 0
        # the played cards are the card in the middle of the screen
        played_cards = {}
        # when a card is clicked sometimes we need to do something outside
        # of a loop that the card is in
        card_clicked = False
        # after the last player in a trick we want to wait before
        # the next player goes
        last_wait = False
        # point totals
        player_team_pts = 0
        bot_team_pts = 0
        # the display needs to update one more time after all players finish
        # playing this is to display the last card played before exit
        one_more = True
        one_more_tic = 0

        # ***GAME LOOP HAND***
        run_hand = True
        while run_hand or one_more:
            # allow the user to exit the tab by hitting the x
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_hand = False
                    # return 0, 0 so the program does not throw an error
                    # on exit
                    return 0, 0

            # fill screen
            surface.fill(green)
            # display trump indicator
            display_image(surface, trump_ind, trump_ind_x, trump_ind_y)
            # display bot hands to screen
            # bot 1
            array_display_y(surface, roted_back, bot1_x, bot1_y, bot_y_change, (len(player_hands['bot1'])))
            # bot 2
            array_display_x(surface, scaled_back, bot2_x, bot2_y, bot_x_change, (len(player_hands['bot2'])))
            # bot 3
            array_display_y(surface, roted_back, bot3_x, bot3_y, bot_y_change, (len(player_hands['bot3'])))

            # display the played cards at specified locations for each player
            for card, player_assoc in played_cards.items():
                # player
                if player_assoc == player:
                    playd_img = card_imgs[card]
                    card_factor = height_factor(playd_img, card_h)
                    display_image(surface, scale_image(playd_img, card_factor), player_x, player_y)
                # bot 1 image is rotated
                elif player_assoc == bot1:
                    playd_img = card_imgs[card]
                    card_factor = height_factor(playd_img, card_h)
                    playd_scale = scale_image(playd_img, card_factor)
                    playd_rot = rotate_image(playd_scale, b1_degs)
                    display_image(surface, playd_rot, b1_card_x, b1_card_y)
                # bot 2
                elif player_assoc == bot2:
                    playd_img = card_imgs[card]
                    card_factor = height_factor(playd_img, card_h)
                    display_image(surface, scale_image(playd_img, card_factor), b2_card_x, b2_card_y)
                # bot 3 image is rotated
                elif player_assoc == bot3:
                    playd_img = card_imgs[card]
                    card_factor = height_factor(playd_img, card_h)
                    playd_scale = scale_image(playd_img, card_factor)
                    playd_rot = rotate_image(playd_scale, b3_degs)
                    display_image(surface, playd_rot, b3_card_x, b3_card_y)

            # allow the display to update after the last player plays
            if one_more_tic == 1:
                one_more = False

            # play the tricks (rounds)
            if trick < 5:
                # when each trick is complete
                if iteration == 4:
                    # pause after last card played for comprehension
                    last_wait = True
                    # iterate trick
                    trick += 1
                    # reset to the first player
                    iteration = -1
                    # clear all cards from the center stack
                    played_cards.clear()
                # fix iteration
                if iteration == -1:
                    iteration += 1
                # wait after all bot turns
                if current_player != player:
                    time.sleep(wait_time)
                # set the current player
                current_player = play_order[iteration]

                # ***PLAYER TURN***
                if current_player == player:
                    # dont display for last display update in round
                    if not last_wait:
                        # choose card to play text
                        display_image(surface, cardplay, cardplay_x, cardplay_y)
                # ***DETERMINE PLAYABLE CARDS IN HAND***
                unplayable_cnt = 0
                # are we first to play
                any_playable = False
                if played_cards == {}:
                    any_playable = True
                # if not what is first card
                else:
                    # finding first card and suit
                    first_card = list(played_cards.keys())[0]
                    # checking if the first card is the jick
                    jick = gf.find_jick(trump)
                    # setting the follow suit accordingly
                    if first_card == jick:
                        follow_suit = trump
                    else:
                        follow_suit = first_card[1]
                    # checking if the jick can be played
                    jick_is_playable = False
                    if follow_suit == trump:
                        jick_is_playable = True

                    following_cards = []
                    for card in bttns:
                        # checking if the card is following and if the jick is
                        # playable or not with this suit
                        if card[1] == follow_suit or jick_is_playable:
                            # checking if the card is a jack
                            if card[0] == 'J':
                                # checking if the card is the jick and if the
                                # suit to follow is not trump
                                if first_card[1] == jick[1] and follow_suit != trump:
                                    unplayable_cnt += 1
                                # checking for other jacks and suits
                                elif card[1] == follow_suit:
                                    following_cards.append(card)
                                else:
                                    unplayable_cnt += 1
                            # checking if the card is following suit
                            elif card[1] == follow_suit:
                                following_cards.append(card)
                            else:
                                unplayable_cnt += 1
                        else:
                            # if no card in hand follows the above rules
                            # then it is unplayable add to the count
                            unplayable_cnt += 1

                # display the buttons and logic
                for card in bttns:
                    if bttns[card].draw(surface):
                        # if it is the players turn allow them to play cards
                        if current_player == player:
                            # when all cards are playable allow interaction
                            if any_playable:
                                # when card clicked remove
                                # the card from your hand
                                player_hands[player].remove(card)
                                # add the card to the center stack
                                played_cards[card] = current_player
                                # set variables to remove the card from bttns
                                card_clicked = True
                                last_played_p = card
                                # got to the next turn
                                iteration += 1
                                any_playable = False
                            else:
                                # if not all cards are playable what is
                                if card in following_cards:
                                    # when card clicked remove card from hand
                                    player_hands[player].remove(card)
                                    # add the card to the center stack
                                    played_cards[card] = current_player
                                    # set variables to remove card from bttns
                                    card_clicked = True
                                    last_played_p = card
                                    # got to the next turn
                                    iteration += 1
                                # if no cards are playable allow all cards
                                elif unplayable_cnt == len(bttns):
                                    # when card clicked remove card from hand
                                    player_hands[player].remove(card)
                                    # add the card to the center stack
                                    played_cards[card] = current_player
                                    # set variables to remove card from bttns
                                    card_clicked = True
                                    last_played_p = card
                                    # got to the next turn
                                    iteration += 1

                # if a card was selected by the player remove it from bttns
                if card_clicked:
                    del bttns[last_played_p]
                    # reset the clicked variable
                    card_clicked = False

                # ***BOT TURNS***
                # dont let bot play on players iteration
                if current_player == player or trick == 5:
                    pass
                else:
                    # set bot hand
                    bot_hand = player_hands[current_player]
                    # select a card and remove it from hand
                    selected_card, bot_hand = bf.bot_play_card(trump, bot_hand, played_cards)
                    # add card selected to played cards stack
                    played_cards[selected_card] = current_player
                    # set new bot hand
                    player_hands[current_player] = bot_hand
                    iteration += 1

                # at the end of the round decide the winner
                if iteration == 4:
                    round_winner = gf.round_winner(trump, played_cards)
                    # decide team points player team
                    if round_winner == bot2 or round_winner == player:
                        player_team_pts += 1
                    # team points bot team
                    else:
                        bot_team_pts += 1
                    play_order = gf.play_order_round(round_winner, play_order)

            # the bots play 1 frame ahead of display updates
            # so to display the last card played tick the display update
            # one more time after the round is complete
            if one_more_tic == 1:
                pygame.display.update()
                time.sleep(wait_time)
                one_more_tic -= 10
            if trick == 5:
                # as stated above display once more but close out the
                # loop after
                run_hand = False
                one_more = True
                one_more_tic += 1
                # after one more display update
                # return the scores
                if one_more_tic < 0:
                    player_pts, bot_pts = gf.give_points(makers, player_team_pts)
                    return player_pts, bot_pts

            # after the bot turns wait for comprehension
            if last_wait:
                pygame.display.update()
                time.sleep(wait_time)
                last_wait = False
            # otherwise just update the display
            else:
                pygame.display.update()


def player_wins(surface):
    """displays the win screen for the player
returns False if the tab is Xed out, True otherwise"""
    off_white = (248, 246, 229)
    # load the victory image
    is_card = False
    trophy = load_image('trophy.jpg', is_card)
    # scale the image to fit the screen
    trophy_h = 800
    trophy = scale_image(trophy, height_factor(trophy, trophy_h))
    # image coordinates
    trophy_x = 249
    trophy_y = 0
    # display time seconds
    display_time = 5

    # display the victory screen
    victory = True
    while victory:
        # allow the user to x out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        # display the victory screen
        surface.fill(off_white)
        display_image(surface, trophy, trophy_x, trophy_y)
        # update the display
        pygame.display.update()
        # display for display time
        time.sleep(display_time)
        victory = False
    return True


def bots_win(surface):
    """displays the lose screen for the player
returns False if the tab is Xed out, True otherwise"""
    grey = (190, 190, 190)
    # load the lose image
    is_card = False
    lose = load_image('lose.jpg', is_card)
    # scale the image to fit the screen
    lose_h = 300
    lose = scale_image(lose, height_factor(lose, lose_h))
    # image coordinates
    lose_x = 113
    lose_y = 250
    # display time seconds
    display_time = 5

    # display the loser screen
    fail = True
    while fail:
        # allow user to x out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        # display the lose screen
        surface.fill(grey)
        display_image(surface, lose, lose_x, lose_y)
        # update the display
        pygame.display.update()
        # wait to allow the user to see the screen
        time.sleep(display_time)
        fail = False
    return True


def score_display(surface, player_total, bot_total):
    """displays the player total and the bot total points
returns false if the tab is Xed out, True otherwise"""
    # background color
    off_white = (248, 246, 229)
    # load images
    is_card = False
    tally = load_image('tally.jpg', is_card)
    header = load_image('total_pts.jpg', is_card)
    # scale factors
    header_h = 70
    tally_h = 50
    # scale images
    header = scale_image(header, height_factor(header, header_h))
    tally = scale_image(tally, height_factor(tally, tally_h))
    # image coordinates
    header_x = 10
    header_y = 117
    # initial coordinates for tallys
    player_x = 180
    player_y = 197
    bot_x = 780
    bot_y = player_y
    # change in tally x
    change_x = 15
    # display time
    display_time = 5
    # display screen loop
    running = True
    while running:
        # allow user to x out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        # display the current scores
        surface.fill(off_white)
        display_image(surface, header, header_x, header_y)
        # player tally
        array_display_x(surface, tally, player_x, player_y, change_x, player_total)
        # bot tally
        array_display_x(surface, tally, bot_x, bot_y, change_x, bot_total)
        pygame.display.update()
        time.sleep(display_time)
        running = False
    # returns true when not Xed out
    return True
