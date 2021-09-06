import pygame
from pygame.locals import *
import levels

import time
import random


# In[2]:


class SquarePlayer():
    def __init__(self, display, color, width, height, x, y):
        self.display = display
        self.color = color  
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.object = pygame.rect.Rect(x, y, width, height)
        
    def draw(self):
        pygame.draw.rect(self.display, self.color, self.object, 5)


# In[3]:


class Ghost():
    def __init__(self, display):
        self.display = display
        self.color = (0,255,0)
        self.width, self.height = 64, 64
        self.x, self.y = 0, 0
        self.object = pygame.rect.Rect(self.x, self.y, self.width, self.height)
            
    def draw(self, coord_list):
        if type(coord_list[-250]) == tuple:
            self.x = coord_list[-250][0]
            self.y = coord_list[-250][1]
        self.object = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.display, self.color, self.object, 5)


# In[4]:


class Goal():
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


# In[5]:


class Portal():
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


# In[6]:


class Level():
    def __init__(self, display, grid, name):
        x = 0
        y = 0
        self.name = name
        
        self.display = display
        self.grid = grid
        self.surface = pygame.Surface((512, 512))
        self.surface.set_colorkey((0,0,0))
        
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
                    self.player_spawn = pygame.rect.Rect(self.square_x, self.square_y, 64, 64)
                    
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
                    pygame.draw.rect(self.surface, (128,128,128), wall_object)
                    
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
        self.display.blit(self.surface, (0,0))
        
    def level_reset(self):
        goal_list_len = len(self.completed_goals)
        temp_list = []
        for _ in range(goal_list_len):
            temp_list.append(False)
        self.completed_goals = temp_list  
        for goal in self.goal_list:
            goal.goal_completed = False


# In[ ]:





# In[7]:


black = (0,0,0)
speed = 2

square_x, square_y = 0, 0
previous_x, previous_y = 0, 0
x_change, y_change = 0, 0
goal_x, goal_y = 0, 0

screen_width, screen_height = (512, 512)
square_width, square_height = (64, 64)


# In[18]:


screen = pygame.display.set_mode((screen_width, screen_height))
running = True

level1 = Level(screen, levels.level1grid, "level1")
level2 = Level(screen, levels.level2grid, "level2")
level3 = Level(screen, levels.level3grid, "level3")
level4 = Level(screen, levels.level4grid, "level4")

square = SquarePlayer(screen, black, square_width, square_height, square_x, square_y)
player_coords = []
ghost = Ghost(screen)

level_dict = {1: level1,
             2: level2,
             3: level3,
             4: level4}

level_goal_list = []

level_int = 1
min_int = 1
max_int = len(level_dict)

collision_off = False

while running:
    #resetting to beginning
    if level_int >= max_int:
        level_int = min_int
        current_level = level_dict[level_int]
        next_level = level_dict[2]
        square_x = 0
        square_y = 0
    else:
        current_level = level_dict[level_int]
        next_level = level_dict[level_int+1] 
    
    screen.fill((255,255,255))
    current_level.blit_level()
    
    square = SquarePlayer(screen, black, square_width, square_height, square_x, square_y)
    square.draw()
    
    previous_x = square_x
    previous_y = square_y
    player_coords.append((square_x, square_y))
    
    if len(player_coords) > 250:        
        ghost.draw(player_coords)
    
    pygame.display.flip()
    
    current_level.level_list_update()
    
    #making a list with the same amount of goals in the level to compare to later
    if len(level_goal_list) == 0:
        for _ in range(len(current_level.completed_goals)):
            level_goal_list.append(True)
      
    #checking if all goals have been completed
    if current_level.completed_goals == level_goal_list:
        current_level.level_reset()
        player_coords = []
        level_goal_list = []
        level_int += 1
        square_x, square_y = next_level.square_x, next_level.square_y
    
    #player movement
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
    
    #wall boundreys
    if square_x > screen_width-64:
        square_x = screen_width-64
    if square_x < 0:
        square_x = 0
    if square_y > screen_height-64:
        square_y = screen_height-64
    if square_y < 0:
        square_y = 0
    
    square = SquarePlayer(screen, black, square_width, square_height, square_x, square_y)
    
    #checking for walls
    for wall in current_level.wall_points:
        if square.object.colliderect(wall) == True:
            square_x = previous_x
            square_y = previous_y
            
    #checking for goals
    for goal in current_level.goal_list:
        if square.object.colliderect(goal.object) == True:
            goal.goal_completed = True
            current_level.level_list_update()
            collision_off = True
          
    #checking if the player is in the safe area
    for space_object in current_level.safe_area:
        if square.object.colliderect(space_object) == True: #and current_level.completed_goals != level_goal_list:
            collision_off = True
        else:
            collision_off = False
        
    #ghost collision
    if collision_off == False and square.object.colliderect(current_level.player_spawn) == False:
        if square.object.colliderect(ghost.object) == True:
            level_int = min_int
            square_x, square_y = 0, 0
            player_coords = []
            current_level.level_reset()
            #current_level = level_dict[level_int]
            print(current_level.name)
        
    square = SquarePlayer(screen, black, square_width, square_height, square_x, square_y)
        
    #game quit
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            square_x = 0
            square_y = 0
            running = False
            collision_off = False
            
           
            
pygame.quit()


# In[11]:


#         while event.type == pygame.:
#             if event.key == K_w:
#                 square_y -= 10
#                 #square = Square(screen, black, square_width, square_height, square_x, square_y)

#             if event.key == K_s:
#                 square_y += 10
#                 #square = Square(screen, black, square_width, square_height, square_x, square_y)
                
#             if event.key == K_a:
#                 square_x -= 10 
#                 #square = Square(screen, black, square_width, square_height, square_x, square_y)
                
#             if event.key == K_d:
#                 square_x += 10 
#                 #square = Square(screen, black, square_width, square_height, square_x, square_y)


# In[57]:


# for coords in level1.wall_points:
#         if square.object.collidepoint(coords[0], coords[1]) == True:
#             if square_direction == "up":
#                 square_y += 1
#             if square_direction == "down":
#                 square_y -= 1
#             if square_direction == "left":
#                 square_y += 1
#             if square_direction == "right":
#                 square_y -= 1
            
#         if square.object.collidepoint(coords[0]+32, coords[1]) == True:
#             if square_direction == "up":
#                 square_y += 1
#             if square_direction == "down":
#                 square_y -= 1
#             if square_direction == "left":
#                 square_y += 1
#             if square_direction == "right":
#                 square_y -= 1
            
#         if square.object.collidepoint(coords[0], coords[1]+32) == True:
#             if square_direction == "up":
#                 square_y += 1
#             if square_direction == "down":
#                 square_y -= 1
#             if square_direction == "left":
#                 square_y += 1
#             if square_direction == "right":
#                 square_y -= 1
            
#         if square.object.collidepoint(coords[0]+32, coords[1]+32) == True:
#             if square_direction == "up":
#                 square_y += 1
#             if square_direction == "down":
#                 square_y -= 1
#             if square_direction == "left":
#                 square_y += 1
#             if square_direction == "right":
#                 square_y -= 1 


# In[ ]:


# class Game():
#     def __init__(self):
#         self.running = True
#         self.screen_width, self.screen_height = (512, 512)
#         self.square_width, self.square_height = (64, 64)
      
#     def game_loop(self):
#         self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
#         self.level_int = 1
        
#         black = (0,0,0)
#         square_direction = ""
#         speed = 1

#         square_x, square_y = 0, 0
#         previous_x, previous_y = 0, 0
#         x_change, y_change = 0, 0
#         goal_x, goal_y = 0, 0
#         square_width, square_height = 64, 64
        
#         level1 = Level(self.screen, levels.level1grid, 1)
#         level2 = Level(self.screen, levels.level2grid, 2)

#         square = SquarePlayer(self.screen, black, square_width, square_height, square_x, square_y, square_direction)

#         level_dict = {1: level1,
#                      2: level2}
        
#         level_goal_list = []
#         while self.running:
#             self.screen.fill((255,255,255))
#             current_level = level_dict[self.level_int]
#             current_level.blit_level()
#             square = SquarePlayer(self.screen, black, square_width, square_height, square_x, square_y, square_direction)
#             square.draw()
#             pygame.display.flip()

#             previous_x = square_x
#             previous_y = square_y

#             goal_list_len = len(current_level.completed_goals)
#             goal_list_int = 0

#             current_level.level_list_update()

#             for b in range(len(current_level.completed_goals)):
#                 level_goal_list.append(True)
                
#             if current_level.completed_goals == level_goal_list:
#                 print(self.level_int)
#                 self.screen.fill((255,255,255))
#                 level_goal_list = []
#                 self.level_int += 1

#             for goal in level2.goal_list:
#                 if square.object.colliderect(goal.object) == True:
#                     goal.goal_completed = True
#                     level_goal_list.append(goal.goal_completed)
#                     pygame.draw.rect(current_level.surface, (0, 0, 255), goal.object)

#             keys = pygame.key.get_pressed()
#             if keys[pygame.K_w] or keys[pygame.K_UP]:
#                 square_y -= speed
#                 square_direction = "up"
#             if keys[pygame.K_s] or keys[pygame.K_DOWN]:
#                 square_y += speed
#                 square_direction = "down"
#             if keys[pygame.K_a] or keys[pygame.K_LEFT]:
#                 square_x -= speed
#                 square_direction = "left"
#             if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
#                 square_x += speed
#                 square_direction = "right"

#             if square_x > self.screen_width-64:
#                 square_x = self.screen_width-64

#             if square_x < 0:
#                 square_x = 0

#             if square_y > self.screen_height-64:
#                 square_y = self.screen_height-64

#             if square_y < 0:
#                 square_y = 0


#             square = SquarePlayer(self.screen, (0,0,0), square_width, square_height, square_x, square_y, square_direction)

#             for wall in level2.wall_points:
#                 if square.object.colliderect(wall) == True and len(keys) != 2:
#                     square_x = previous_x
#                     square_y = previous_y

#             for event in pygame.event.get(): 
#                 if event.type == pygame.QUIT:
#                     running = False
#                     pygame.quit()

