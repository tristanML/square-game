import pygame
from pygame import display
from pygame.locals import *
from pygame.sprite import collide_rect
import time
import os

from .levels import *
from .levels11_20 import *

from .default_settings import (
    screen_height,
    screen_width,
    black,
    square_width,
    square_height,
    speed
)
from .players import Goal, Level, SquarePlayer, Ghost

def default_run():
    screen = pygame.display.set_mode((screen_width, screen_height))
    running = True
    intro_on = True
    
    intro_frame1 = pygame.image.load("src/square_game/IntroFrames/frame1.png")
    intro_frame2 = pygame.image.load("src/square_game/IntroFrames/frame2.png")
    intro_frame3 = pygame.image.load("src/square_game/IntroFrames/frame3.png")
    intro_frame4 = pygame.image.load("src/square_game/IntroFrames/frame4.png")
    intro_frame_list = [intro_frame1, intro_frame2, intro_frame3, intro_frame4]

    doFrame = pygame.image.load("src/square_game/warningFrames/doFrame.png")
    notFrame = pygame.image.load("src/square_game/warningFrames/notFrame.png")
    stopFrame = pygame.image.load("src/square_game/warningFrames/stopFrame.png")
    warning_frame_list = [doFrame, notFrame, stopFrame]

    level1 = Level(screen, level1grid, "level1")
    level2 = Level(screen, level2grid, "level2")
    level3 = Level(screen, level3grid, "level3")
    level4 = Level(screen, level4grid, "level4")
    level5 = Level(screen, level5grid, "level5")
    level6 = Level(screen, level6grid, "level6")
    level7 = Level(screen, level7grid, "level7")
    level8 = Level(screen, level8grid, "level8")
    level9 = Level(screen, level9grid, "level9")
    level10 = Level(screen, level10grid, "level10")
    level11 = Level(screen, level11grid, "level11")
    level12 = Level(screen, level12grid, "level12")
    level13 = Level(screen, level13grid, "level13")

    square = SquarePlayer(screen, black, square_width, square_height, 0, 0)
    player_coords = []
    ghost = Ghost(screen, 0, 0)

    level_dict = {1: level1, 
                2: level2, 
                3: level3, 
                4: level4, 
                5: level5, 
                6: level6, 
                7: level7, 
                8: level8, 
                9: level9, 
                10: level10,
                11: level11,
                12: level12,
                13: level13}

    level_int = 1
    min_int = 1
    max_int = len(level_dict)

    editor_mode_on = False
    setback = 250
    in_zone = True

    while intro_on:
        for intro_frame in intro_frame_list:
            screen.blit(intro_frame, (0,0))
            pygame.display.flip()
            time.sleep(0.5)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        intro_on = False
                    if event.key == K_1:
                        setback = 300
                    if event.key == K_2:
                        setback = 250
                    if event.key == K_3:
                        setback = 200
                    if event.key == K_4:
                        setback = 150
                if event.type == QUIT:
                    intro_on = False
                    running = False

    for warning_frame in warning_frame_list:
        screen.blit(warning_frame, (0,0))
        pygame.display.flip()
        time.sleep(1)

    while running:
        #resetting to beginning
        if level_int > max_int:
            square.x, square.y = 0, 0
            ghost.x, ghost.y = 0, 0
            level_int = min_int
            current_level = level_dict[level_int]
            # for x in level_dict:
            #     level_dict[x].level_reset()

        current_level = level_dict[level_int]

        square = SquarePlayer(
            screen, black, square_width, square_height, square.x, square.y
        )

        ghost = Ghost(
            screen, ghost.x, ghost.y
        )

        previous_x = square.x
        previous_y = square.y

        screen.fill((255, 255, 255))
        current_level.blit_level()
        ghost.draw()
        square.draw()
        pygame.display.flip()

        player_coords.append((square.x, square.y))
        if len(player_coords) > setback:
            ghost.x, ghost.y = player_coords[-setback]

        # player movement
        keys = pygame.key.get_pressed()
        if keys[K_w] or keys[K_UP]:
            square.y -= speed
        if keys[K_s] or keys[K_DOWN]:
            square.y += speed
        if keys[K_a] or keys[K_LEFT]:
            square.x -= speed
        if keys[K_d] or keys[K_RIGHT]:
            square.x += speed
        if keys[K_e] and keys[K_LSHIFT] and keys[K_1]:
            editor_mode_on = True
            setback = 325

        # wall boundrys
        if square.x > screen_width - 64:
            square.x = screen_width - 64
        if square.x < 0:
            square.x = 0
        if square.y > screen_height - 64:
            square.y = screen_height - 64
        if square.y < 0:
            square.y = 0

        square = SquarePlayer(
            screen, black, square_width, square_height, square.x, square.y
        )
        ghost = Ghost(
            screen, ghost.x, ghost.y
        )

        # checking for walls
        for wall in current_level.wall_points:
            if square.object.colliderect(wall) == True:
                square.x = previous_x
                square.y = previous_y

        # checking for goals
        if square.object.colliderect(current_level.goal.object) == True:
            ghost.x, ghost.y = current_level.goal.x, current_level.goal.y
            square.x, square.y = current_level.goal.x, current_level.goal.y
            player_coords = [(current_level.goal.x, current_level.goal.y)]
            current_level.level_reset()
            level_int += 1

        if square.object.collidelist(current_level.safe_zone) == True:
            in_zone = True
        else:
            in_zone = False

        #ghost collision
        if square.object.colliderect(ghost.object) == True:
            if square.object.colliderect(current_level.player_spawn) == False and editor_mode_on == False:
                if in_zone == False:
                    level_int = min_int
                    collision_event = ghost.x, ghost.y
                    current_level.level_reset()
                    ghost.x, ghost.y = 0,0
                    square.x, square.y= 0,0
                    player_coords = [(0,0)]

        square = SquarePlayer(
            screen, black, square_width, square_height, square.x, square.y
        )

        # game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                square.x = 0
                square.y = 0
                running = False


    pygame.quit()