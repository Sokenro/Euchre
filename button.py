# This is mostly copied from a YouTube video
# "PyGame Beginner Tutorial in Python - Adding Buttons" by Coding With Russ
# I made some modifications, but I can not take credit for the class
# function as we have not learned about classes in lecture
# and I do not fully understand how they work.
# Class: CS 021

import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # if the mouse is pressed determine if the position is on the button
        if pygame.mouse.get_pressed()[0] == 1:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) and self.clicked == False:
                # to prevent the button from being clicked several
                # times set self.clicked to true
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        # return the action that was applied to the button
        return action
