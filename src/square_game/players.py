import pygame
from pygame.locals import *


__all__ = ["SquarePlayer", "Ghost", "Goal", "Portal", "Level"]


class SquarePlayer:
    def __init__(self, display, color, width, height, x, y):
        self.display = display
        self.color = color
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.object = pygame.rect.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(self.display, self.color, self.object, 5)


class Ghost:
    def __init__(self, display, ghost_x, ghost_y):
        self.display = display
        self.color = (0, 255, 0)
        self.width, self.height = 64, 64
        self.x, self.y = ghost_x, ghost_y
        self.object = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.display, self.color, self.object, 5)

    def kill(self,):
        #self.x, self.y = player_Coords
        #self.object = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.display, self.color, self.object, 5)


class Goal:
    def __init__(self, display, x, y):
        self.display = display
        self.color = (255, 0, 0)
        self.x, self.y = x, y
        self.coords = (self.x, self.y)
        self.width, self.height = (64, 64)
        self.object = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.goal_completed = False

    def draw(self):
        pygame.draw.rect(self.display, self.color, self.object)


class Portal:
    def __init__(self, display, x, y):
        self.display = display
        self.color = (255, 0, 0)
        self.x, self.y = x, y
        self.width, self.height = (64, 64)
        self.object = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.goal_completed = False

    def draw(self, color):
        self.color = color
        pygame.draw.rect(self.display, self.color, self.object)


class Level:
    def __init__(self, display, grid, name):
        x = 0
        y = 0
        self.name = name

        self.display = display
        self.grid = grid
        self.surface = pygame.Surface((512, 512))
        self.surface.set_colorkey((0, 0, 0))

        self.wall_points = []

        self.goal = 0

        self.safe_zone = []
        for rows in grid:
            for square_code in rows:
                if x == 512:
                    x = 0
                if square_code == 1:
                    self.square_x = x
                    self.square_y = y
                    self.player_spawn = pygame.rect.Rect(
                        self.square_x, self.square_y, 64, 64
                    )
                    self.safe_zone.append(self.player_spawn)

                if square_code == 2:
                    self.goal = Goal(self.display, x, y)
                    pygame.draw.rect(self.surface, self.goal.color, self.goal.object)

                if square_code == 3:
                    wall_object = pygame.rect.Rect(x, y, 32, 32)
                    self.wall_points.append(wall_object)
                    pygame.draw.rect(self.surface, (128, 128, 128), wall_object)

                if square_code == 4:
                    safe_square = pygame.rect.Rect(x, y, 32, 32)
                    self.safe_zone.append(safe_square)
                    pygame.draw.rect(self.surface, (128, 255, 255), safe_square)

                x += 32
            y += 32

    def blit_level(self):
        self.display.blit(self.surface, (0, 0))

    def level_reset(self):
        self.goal.goal_completed = False