import pygame
from pygame import display
from pygame.locals import *
from pygame.sprite import collide_rect
import time

from .levels import level1grid, level2grid, level3grid, level4grid, level5grid

from .default_settings import (
    screen_height,
    screen_width,
    black,
    square_width,
    square_height,
    speed,
)
from .players import Goal, Level, SquarePlayer, Ghost


def default_run():
    screen = pygame.display.set_mode((screen_width, screen_height))
    running = True

    level1 = Level(screen, level1grid, "level1")
    level2 = Level(screen, level2grid, "level2")
    level3 = Level(screen, level3grid, "level3")
    level4 = Level(screen, level4grid, "level4")
    level5 = Level(screen, level5grid, "level5")

    square = SquarePlayer(screen, black, square_width, square_height, 0, 0)
    player_coords = []
    ghost = Ghost(screen, 0, 0)

    level_dict = {1: level1, 2: level2, 3: level3, 4: level4, 5: level5}

    level_int = 1
    min_int = 1
    max_int = len(level_dict)

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
        if len(player_coords) > 250:
            ghost.x, ghost.y = player_coords[-250]
            #player_coords = []
            
            # print("current level", current_level.name)
            # if level_int > max_int:
            #     level_int = min_int
            #     current_level = level_dict[level_int]
            #     square.x = 0
            #     square.y = 0
            # else:
            #     level_int = level_int
            #     current_level = level_dict[level_int]
            # print("new level", current_level.name)
            # square.x, square.y = current_level.square.x, current_level.square.y

        # player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            square.y -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            square.y += speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            square.x -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            square.x += speed
        if keys[pygame.K_l]:
            print(current_level.name)


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
        # ghost = Ghost(
        #     screen, ghost.x, ghost.y
        # )

        # square.draw()
        # ghost.draw()
        # pygame.display.flip()

        # checking for walls
        for wall in current_level.wall_points:
            if square.object.colliderect(wall) == True:
                square.x = previous_x
                square.y = previous_y

        # checking for goals
        if square.object.colliderect(current_level.goal.object) == True:
            ghost.x, ghost.y = current_level.goal.x, current_level.goal.y
            square.x, square.y = current_level.goal.x, current_level.goal.y
            player_coords = []
            current_level.level_reset()
            level_int += 1
            # collision_off = True

        #ghost collision
        if square.object.colliderect(ghost.object) == True:
            if square.object.colliderect(current_level.player_spawn) == False:
                level_int = min_int
                collision_event = ghost.x, ghost.y
                # if collision_event == (current_level.goal.x, current_level.goal.y):
                #     level_int += 1
                #     print("avoided fake collsion")
                # else:
                # print(current_level.goal.x, current_level.goal.y)
                # print("collision at", collision_event, current_level.goal.goal_completed)
                current_level.level_reset()
                ghost.x, ghost.y = 0,0
                square.x, square.y= 0,0
                player_coords = [(0,0)]

                

        # previous_x = square.x
        # previous_y = square.y
        #player_coords.append((square.x, square.y))

        # if len(player_coords) > 250:
        #     ghost.x, ghost.y = player_coords[-250] 

        # game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                square.x = 0
                square.y = 0
                running = False


    pygame.quit()