import pygame
from pygame.locals import *

from .levels import level1grid, level2grid, level3grid, level4grid
from .default_settings import (
    screen_height,
    screen_width,
    black,
    square_width,
    square_height,
    speed,
)
from .players import Level, SquarePlayer, Ghost


def default_run():
    screen = pygame.display.set_mode((screen_width, screen_height))
    running = True
    square_x, square_y = 0, 0

    level1 = Level(screen, level1grid, "level1")
    level2 = Level(screen, level2grid, "level2")
    level3 = Level(screen, level3grid, "level3")
    level4 = Level(screen, level4grid, "level4")

    square = SquarePlayer(screen, black, square_width, square_height, 0, 0)
    player_coords = []
    ghost = Ghost(screen)

    level_dict = {1: level1, 2: level2, 3: level3, 4: level4}

    level_goal_list = []

    level_int = 1
    min_int = 1
    max_int = len(level_dict)

    collision_off = False

    while running:
        # resetting to beginning
        if level_int >= max_int:
            level_int = min_int
            current_level = level_dict[level_int]
            next_level = level_dict[2]
            square_x = 0
            square_y = 0
        else:
            current_level = level_dict[level_int]
            next_level = level_dict[level_int + 1]

        screen.fill((255, 255, 255))
        current_level.blit_level()

        square = SquarePlayer(
            screen, black, square_width, square_height, square_x, square_y
        )
        square.draw()

        previous_x = square_x
        previous_y = square_y
        player_coords.append((square_x, square_y))

        if len(player_coords) > 250:
            ghost.draw(player_coords)

        pygame.display.flip()

        current_level.level_list_update()

        # making a list with the same amount of goals in the level to compare to later
        if len(level_goal_list) == 0:
            for _ in range(len(current_level.completed_goals)):
                level_goal_list.append(True)

        # checking if all goals have been completed
        if current_level.completed_goals == level_goal_list:
            current_level.level_reset()
            player_coords = []
            level_goal_list = []
            level_int += 1
            square_x, square_y = next_level.square_x, next_level.square_y

        # player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            square_y -= speed
            square_direction = "up"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            square_y += speed
            square_direction = "down"
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            square_x -= speed
            square_direction = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            square_x += speed
            square_direction = "right"

        # wall boundreys
        if square_x > screen_width - 64:
            square_x = screen_width - 64
        if square_x < 0:
            square_x = 0
        if square_y > screen_height - 64:
            square_y = screen_height - 64
        if square_y < 0:
            square_y = 0

        square = SquarePlayer(
            screen, black, square_width, square_height, square_x, square_y
        )

        # checking for walls
        for wall in current_level.wall_points:
            if square.object.colliderect(wall) == True:
                square_x = previous_x
                square_y = previous_y

        # checking for goals
        for goal in current_level.goal_list:
            if square.object.colliderect(goal.object) == True:
                goal.goal_completed = True
                current_level.level_list_update()
                collision_off = True

        # checking if the player is in the safe area
        for space_object in current_level.safe_area:
            if (
                square.object.colliderect(space_object) == True
            ):  # and current_level.completed_goals != level_goal_list:
                collision_off = True
            else:
                collision_off = False

        # ghost collision
        if (
            collision_off == False
            and square.object.colliderect(current_level.player_spawn) == False
        ):
            if square.object.colliderect(ghost.object) == True:
                level_int = min_int
                square_x, square_y = 0, 0
                player_coords = []
                current_level.level_reset()
                # current_level = level_dict[level_int]
                print(current_level.name)

        square = SquarePlayer(
            screen, black, square_width, square_height, square_x, square_y
        )

        # game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                square_x = 0
                square_y = 0
                running = False
                collision_off = False

    pygame.quit()
