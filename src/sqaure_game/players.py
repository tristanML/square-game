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
    def __init__(self, display):
        self.display = display
        self.color = (0, 255, 0)
        self.width, self.height = 64, 64
        self.x, self.y = 0, 0
        self.object = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def draw(self, coord_list):
        if type(coord_list[-250]) == tuple:
            self.x = coord_list[-250][0]
            self.y = coord_list[-250][1]
        self.object = pygame.rect.Rect(self.x, self.y, self.width, self.height)
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

        self.goal_list = []
        self.completed_goals = []

        self.safe_area = []
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

                if square_code == 2:
                    global goal_x, goal_y
                    goal_x = x
                    goal_y = y
                    goal = Goal(self.display, goal_x, goal_y)
                    self.goal_list.append(goal)
                    self.completed_goals.append(goal.goal_completed)
                    pygame.draw.rect(self.surface, goal.color, goal.object)

                if square_code == 3:
                    wall_object = pygame.rect.Rect(x, y, 32, 32)
                    self.wall_points.append(wall_object)
                    pygame.draw.rect(self.surface, (128, 128, 128), wall_object)

                if square_code == 4:
                    safe_object = pygame.rect.Rect(x, y, 32, 32)
                    self.safe_area.append(safe_object)

                x += 32
            y += 32

    def level_list_update(self):
        self.completed_goals = []
        for goal in self.goal_list:
            self.completed_goals.append(goal.goal_completed)

    def blit_level(self):
        self.display.blit(self.surface, (0, 0))

    def level_reset(self):
        goal_list_len = len(self.completed_goals)
        temp_list = []
        for _ in range(goal_list_len):
            temp_list.append(False)
        self.completed_goals = temp_list
        for goal in self.goal_list:
            goal.goal_completed = False
