# Class: CS 021
# Euchre card game main loop, plays all rounds and allows for
# playing several games in a row

import pygame
import Euchre_functions as euf
import Game_Functions as gf

# Initialize pygame
pygame.init()


def main():
    cards = ()
    # create the main display
    screen_height = 800
    screen_width = 1080
    screen = pygame.display.set_mode((screen_width, screen_height))
    # set the screen caption
    pygame.display.set_caption('Euchre')
    # load images
    is_card = False
    icon = euf.load_image('s.png', is_card)
    # set the tab icon
    pygame.display.set_icon(icon)

    # ***PREGAME SETUP***
    # pts required to win
    winning_total = 11
    no_winner = True
    # create the new_game variable
    new_game = True
    play_again = False

    # main game loop
    running = True
    while running:
        # allow the user to x out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # run the main menu if the game tab is not Xed out of
            if no_winner or play_again:
                running, new_game = euf.main_menu(screen)
                # set the dealer order
                dealer_order = ['bot1', 'bot2', 'bot3', 'player']

            # set the team point variables
            player_total = 0
            bot_total = 0

            # determine if you open the main game
            no_winner = True
            # new game is only false if the main menu is exited
            if new_game is False:
                # exit the program if the main menu is exited
                no_winner = False
                running = False

            # ***PLAY GAME LOOP***
            while no_winner:
                # allow player to x out the tab
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # each new game the player starts as the dealer
                if new_game:
                    play_order = dealer_order[:]
                # after each hand the dealer becomes the player to the
                # left of the dealer
                elif new_game is False:
                    dealer_order = gf.play_order_dealer(dealer_order)
                    play_order = dealer_order[:]
                # play one round
                player_pts, bot_pts = euf.round_play(screen, play_order)
                # if the tab is exited early round_play returns 0, 0

                # add team points to the totals
                player_total += player_pts
                bot_total += bot_pts

                # stop play when tab is exited
                if player_pts == 0 and bot_pts == 0:
                    no_winner = False
                    running = False
                    # open the main menu after victory to play again
                    play_again = False
                # determine if there is a winner yet
                # player wins
                if player_total >= winning_total:
                    # return to the main menu if there is a winner
                    no_winner = False
                    # open the main menu after victory to play again
                    play_again = True
                    # display winners screen
                    running = euf.player_wins(screen)
                # bots win
                if bot_total >= winning_total:
                    # return to the main menu if there is a winner
                    no_winner = False
                    play_again = True
                    # display the losers screen
                    running = euf.bots_win(screen)

                # display the current point totals to the screen
                if (player_pts != 0 or bot_pts != 0) and no_winner:
                    running = euf.score_display(screen, player_total, bot_total)

                # make new game false after the first loop
                # cause its not a new game anymore, its old...
                new_game = False

    pygame.quit()


main()
