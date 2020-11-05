#!/usr/bin/env python

import pygame, math, random
from gameVariables import *

""" OO design for key objects and their behaviors in the game """

class Dog:
    # the class for the dog; the x position is always the same, we only
    #update the y position when we fall or jump, based on a formula
    def __init__(self):
        self.dog_x = gameWidth / 2 - dogWidth
        self.dog_y = gameHeight / 2 - dogHeight / 2
        self.steps_to_jump = 0

    # the formula used makes everything to move "smooth"

    # use sin/cosine to allow for natural movement in accordance with gravity
    # even if there is no physics engine(?) to do so
    def update_position(self):
        if self.steps_to_jump > 0:
            self.dog_y -= (1 - math.cos((jumpSteps - self.steps_to_jump) * math.pi)) * jumpPixels
            #self.dog_y -= jumpPixels * (jumpSteps - self.steps_to_jump) / 5 ;
            self.steps_to_jump -= 1
        else:
            self.dog_y += dropPixels

    # when we redraw the dog on the game screen, we draw the wing-up or
    # the wing-down image, to create the "flapping" effect
    def redraw(self, screen, image_1, image_2):
        if pygame.time.get_ticks() % 500 >= 250 :
            screen.blit(image_1, (self.dog_x, self.dog_y))
        else:
            screen.blit(image_2, (self.dog_x, self.dog_y))

    # rotate the dog to create the falling effect
    def redraw_dead(self, screen, image):
        self.dog_y += dropPixels
        dog_rot = pygame.transform.rotate(image, gameHeight / 2 - self.dog_y)
        screen.blit(dog_rot, (self.dog_x, self.dog_y))

class PipePair:
    # the class for the pipes; the original x position is the margin of the
    # game window; the pipes moves pixelsFrame / FPS
    # every time, we generate two heights: one for the upper pipe
    # and one for the lower pipe, with the same exact space between
    # then, pipesSpace
    # score_counted tells us if we passed through the pipes succesfully and
    # we received the points

    # set consistent gap between pipes
    def __init__(self, x, score_counted):
        self.x = gameWidth
        self.toph = random.randint(50, 250) - pipeHeight
        self.bottomh = self.toph + pipeHeight + pipesSpace
        self.score_counted = score_counted

    # check collision with the dog and return 1 or 0 (1 = collision, 0 = no collision)
    def check_collision(self, dog_position):
        bx, by = dog_position
        in_x_range = bx + dogWidth > self.x and bx < self.x + pipeWidth
        in_y_range = by > self.toph + pipeHeight and by + dogHeight < self.toph + pipeHeight + pipesSpace
        return in_x_range and not in_y_range

class Ground:
    # a small class for the ground who seems to roll to the left
    # it's just a image who has twice the gameWidth of the game screen,
    # but when it is reaching its end, we reset it

    def __init__(self, image):
        self.x = 0
        self.y = gameHeight - groundHeight
        self.image = image

    # shift the ground by a few pixels each time to mimic movement
    def move_and_redraw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.x -= pixelsFrame
        if(self.x < - gameWidth):
            self.x = 0